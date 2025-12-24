from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

# Menggunakan HTTPBearer untuk mengekstrak token dari header Authorization
security = HTTPBearer()

def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verifikasi Bearer Token statis.
    Membandingkan token yang dikirim client dengan API_KEY di settings.
    """
    if credentials.credentials != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials"
        )
    return credentials.credentials
