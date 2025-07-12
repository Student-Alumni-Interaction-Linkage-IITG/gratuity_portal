"""
Custom Azure AD backend with PKCE support for Microsoft authentication
"""
from social_core.backends.azuread import AzureADOAuth2
from social_core.exceptions import AuthForbidden
import secrets
import base64
import hashlib
import logging

logger = logging.getLogger(__name__)


class AzureADOAuth2WithPKCE(AzureADOAuth2):
    """Azure AD OAuth2 backend with PKCE implementation"""
    
    name = 'azuread-oauth2-pkce'
    
    def generate_code_verifier(self):
        """Generate a code verifier for PKCE"""
        return base64.urlsafe_b64encode(
            secrets.token_bytes(32)
        ).decode('utf-8').replace('=', '')
    
    def generate_code_challenge(self, code_verifier):
        """Generate code challenge from verifier"""
        code_sha = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_sha).decode('utf-8')
        return code_challenge.replace('=', '')
    
    def auth_params(self, state=None):
        """Add PKCE parameters to authorization request"""
        params = super().auth_params(state)
        
        # Generate PKCE parameters
        code_verifier = self.generate_code_verifier()
        code_challenge = self.generate_code_challenge(code_verifier)
        
        # Store code verifier in session for later use
        self.strategy.session_set('pkce_code_verifier', code_verifier)
        
        # Add PKCE parameters to authorization request
        params.update({
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        })
        
        return params
    
    def auth_complete_params(self, state=None):
        """Add code verifier to token request"""
        params = super().auth_complete_params(state)
        
        # Retrieve code verifier from session
        code_verifier = self.strategy.session_get('pkce_code_verifier')
        if code_verifier:
            params['code_verifier'] = code_verifier
            # Clean up session
            self.strategy.session_set('pkce_code_verifier', None)
            
        return params
    
    def user_data(self, access_token, *args, **kwargs):
        """Get user data with minimal logging"""
        try:
            data = super().user_data(access_token, *args, **kwargs)
            
            # Debug: temporarily log available fields to understand the data structure
            logger.info(f"Available user data fields: {list(data.keys())}")
            
            # Try multiple possible name fields
            name = (data.get('displayName') or 
                   data.get('name') or 
                   data.get('givenName', '') + ' ' + data.get('surname', '') or
                   data.get('userPrincipalName', '').split('@')[0] or
                   'Unknown User').strip()
            
            logger.info(f"User logged in: {name}")
            return data
        except Exception as e:
            logger.error(f"Error retrieving user data: {e}")
            raise
    
    def auth_allowed(self, response, details):
        """Check if authentication is allowed"""
        # Allow all users - you can add restrictions here later
        return True
    
    def get_user_details(self, response):
        """Get user details"""
        details = super().get_user_details(response)
        return details
