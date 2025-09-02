# keys.py

PRODUCTION = True  # flip for dev

SECRET_KEY = "django-insecure-!_h9m$14@*64b)ko3!l!ww4yt36-(1jj0%w6@nn^5x8+7!mosj"

# Database credentials
RDS_DB_NAME = "gratuity"
RDS_USERNAME = "postgres"
RDS_PASSWORD = "post"       # replace with strong password in prod
RDS_HOSTNAME = "localhost"
RDS_PORT = "5432"

# Azure AD credentials
SOCIAL_AUTH_AZUREAD_OAUTH2_PKCE_KEY = "aa4f2840-08d7-458e-992d-6ff67ff0d699"
SOCIAL_AUTH_AZUREAD_OAUTH2_PKCE_SECRET = "APF8Q~J.bD3cXIgyFjH.CAu79wDoQsuNCEYjwcin"
SOCIAL_AUTH_AZUREAD_OAUTH2_PKCE_TENANT_ID = "850aa78d-94e1-4bc6-9cf3-8c11b530701c"
