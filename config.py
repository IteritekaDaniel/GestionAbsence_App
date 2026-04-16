"""
config.py — Configuration centralisée de l'application
"""

# ═════════════════════════════════════════════════════════════════════════════
#   CONFIGURATION GÉNÉRALE
# ═════════════════════════════════════════════════════════════════════════════

# Application
APP_NAME = "DanProject"
APP_VERSION = "2.0"
APP_TITLE = f"{APP_NAME} v{APP_VERSION}"

# Fenêtre
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 750

# ═════════════════════════════════════════════════════════════════════════════
#   THÈME
# ═════════════════════════════════════════════════════════════════════════════

# Thème par défaut au démarrage
DEFAULT_THEME = "light"  # "light" ou "dark"

# ═════════════════════════════════════════════════════════════════════════════
#   LANGUE
# ═════════════════════════════════════════════════════════════════════════════

DEFAULT_LANGUAGE = "fr"  # "fr" ou "en"

# ═════════════════════════════════════════════════════════════════════════════
#   NOTIFICATIONS
# ═════════════════════════════════════════════════════════════════════════════

# Durée affichage des notifications (en ms)
NOTIFICATION_DURATION = {
    "success": 3000,
    "info": 3000,
    "warning": 4000,
    "error": 5000,
}

# ═════════════════════════════════════════════════════════════════════════════
#   2FA (AUTHENTIFICATION DOUBLE FACTEUR)
# ═════════════════════════════════════════════════════════════════════════════

# Activer/désactiver 2FA (admin peut l'activer individuellement)
ENABLE_2FA = True

# Fenêtre temporelle pour validation TOTP (en nombre de périodes)
# Valeurs normales: 1 (strict) à 2 (souple)
OTP_WINDOW = 1

# ═════════════════════════════════════════════════════════════════════════════
#   RACCOURCIS CLAVIER
# ═════════════════════════════════════════════════════════════════════════════

# Activer/désactiver les raccourcis clavier
ENABLE_SHORTCUTS = True

# ═════════════════════════════════════════════════════════════════════════════
#   GRAPHIQUES
# ═════════════════════════════════════════════════════════════════════════════

# Nombre de jours pour la tendance
TREND_DAYS = 30

# Nombre d'étudiants à afficher dans "Top Alertes"
TOP_ALERTS_COUNT = 15

# Style matplotlib
CHART_STYLE = "default"  # Ou "seaborn", "ggplot", etc.

# ═════════════════════════════════════════════════════════════════════════════
#   EXPORTS
# ═════════════════════════════════════════════════════════════════════════════

# Dossier par défaut pour les exports
EXPORT_FOLDER = "./exports"

# Format d'exportation par défaut
DEFAULT_EXPORT_FORMAT = "pdf"  # "pdf", "excel", "csv"

# ═════════════════════════════════════════════════════════════════════════════
#   EMAILS
# ═════════════════════════════════════════════════════════════════════════════

# Activer notifications par email
ENABLE_EMAIL_NOTIFICATIONS = False

# Serveur SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Email de l'application (à configurer)
APP_EMAIL = "absences@school.com"
APP_EMAIL_PASSWORD = ""  # À remplir

# ═════════════════════════════════════════════════════════════════════════════
#   BDD
# ═════════════════════════════════════════════════════════════════════════════

# Type de base de données
DB_TYPE = "sqlite"  # "sqlite" ou "mysql"

# SQLite
SQLITE_DB_FILE = "absences.db"

# MySQL (si DB_TYPE = "mysql")
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DATABASE = "gestion_absences"

# ═════════════════════════════════════════════════════════════════════════════
#   AUDIT & SÉCURITÉ
# ═════════════════════════════════════════════════════════════════════════════

# Enregistrer toutes les actions (audit)
ENABLE_AUDIT = True

# Nombre de jours de conservation des logs d'audit
AUDIT_RETENTION_DAYS = 90

# ═════════════════════════════════════════════════════════════════════════════
#   PERFORMANCES
# ═════════════════════════════════════════════════════════════════════════════

# Nombre d'enregistrements à charger par page
PAGINATION_SIZE = 50

# Cache les données (améliore performance)
ENABLE_CACHE = True

# Durée du cache (en secondes)
CACHE_DURATION = 300

# ═════════════════════════════════════════════════════════════════════════════
#   DÉVELOPPEMENT
# ═════════════════════════════════════════════════════════════════════════════

# Mode debug
DEBUG = False

# Afficher les logs dans la console
VERBOSE_LOGGING = True

# ═════════════════════════════════════════════════════════════════════════════
#   FONCTIONNALITÉS AVANCÉES
# ═════════════════════════════════════════════════════════════════════════════

# Activer les intégrations externes
ENABLE_INTEGRATIONS = False

# Autoriser les imports de données
ENABLE_IMPORT = True

# Autoriser le backup automatique
ENABLE_AUTO_BACKUP = True

# Fréquence du backup automatique (heures)
AUTO_BACKUP_FREQUENCY = 24
