"""
auth_2fa.py — Authentification 2FA avec QR code et TOTP
Sécurité avancée pour DanProject
"""

import qrcode
import pyotp
import hashlib
from typing import Optional
from datetime import datetime
from database import get_conn

class TwoFactorAuth:
    """Gestion du 2FA avec TOTP (Google Authenticator)"""
    
    @staticmethod
    def generate_secret() -> str:
        """Génère un secret 2FA unique"""
        return pyotp.random_base32()
    
    @staticmethod
    def get_qr_code(secret: str, email: str):
        """Génère le QR code pour scanner"""
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(email, issuer_name='DanProject')
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image()
        return img
    
    @staticmethod
    def verify_token(secret: str, token: str) -> bool:
        """Vérifie un token TOTP"""
        try:
            totp = pyotp.TOTP(secret)
            # Accepter le token actuel et les 2 précédents/suivants
            return totp.verify(token, valid_window=1)
        except:
            return False
    
    @staticmethod
    def enable_2fa(admin_id: int, secret: str):
        """Active 2FA pour un admin"""
        conn = get_conn()
        conn.execute(
            "UPDATE admin SET 2fa_secret = ?, 2fa_enabled = 1 WHERE id = ?",
            (secret, admin_id)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def disable_2fa(admin_id: int):
        """Désactive 2FA"""
        conn = get_conn()
        conn.execute(
            "UPDATE admin SET 2fa_secret = NULL, 2fa_enabled = 0 WHERE id = ?",
            (admin_id,)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def is_2fa_enabled(admin_id: int) -> bool:
        """Vérifie si 2FA est activé"""
        conn = get_conn()
        row = conn.execute(
            "SELECT 2fa_enabled FROM admin WHERE id = ?",
            (admin_id,)
        ).fetchone()
        conn.close()
        return row[0] == 1 if row else False
    
    @staticmethod
    def get_secret(admin_id: int) -> Optional[str]:
        """Récupère le secret 2FA"""
        conn = get_conn()
        row = conn.execute(
            "SELECT 2fa_secret FROM admin WHERE id = ?",
            (admin_id,)
        ).fetchone()
        conn.close()
        return row[0] if row and row[0] else None
