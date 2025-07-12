"""
Debug pipeline for Azure AD authentication
"""
import logging

logger = logging.getLogger(__name__)


def debug_auth_pipeline(strategy, details, backend, user=None, *args, **kwargs):
    """Debug function to log authentication pipeline details"""
    logger.info("=== AUTHENTICATION PIPELINE DEBUG ===")
    logger.info(f"Backend: {backend}")
    logger.info(f"User: {user}")
    logger.info(f"Details: {details}")
    logger.info(f"Args: {args}")
    logger.info(f"Kwargs: {kwargs}")
    logger.info("=== END DEBUG ===")
    return {'user': user, 'details': details}
