"""
symbols.py — Symboles et icônes professionnels pour DanProject
Remplace tous les symboles IA par des alternatives respectueuses
"""

from typing import Optional

class Symbols:
    """Symboles et émojis professionnels"""
    
    # NAVIGATION & MENUS
    HOME = "🏠"           # Accueil
    DASHBOARD = "📊"      # Tableau de bord
    CHART = "📈"          # Graphiques
    SETTINGS = "⚙️"       # Paramètres
    HELP = "❓"           # Aide
    ABOUT = "ℹ️"          # À propos
    
    # UTILISATEURS & PROFILS
    STUDENT = "👨‍🎓"       # Étudiant
    TEACHER = "👨‍🏫"       # Enseignant
    PARENT = "👨‍👩‍👧"     # Parent
    ADMIN = "👤"           # Admin
    USER = "👥"            # Utilisateurs
    PROFILE = "👨"        # Profil
    
    # ACTIONS PRINCIPALES
    ADD = "➕"             # Ajouter
    DELETE = "🗑️"         # Supprimer
    EDIT = "✏️"            # Éditer
    SAVE = "💾"            # Enregistrer
    CANCEL = "❌"          # Annuler
    SEARCH = "🔍"         # Rechercher
    FILTER = "🔽"         # Filtrer
    EXPORT = "📤"         # Exporter
    IMPORT = "📥"         # Importer
    PRINT = "🖨️"          # Imprimer
    
    # ABSENCES & PRÉSENCES
    ABSENCE = "📝"        # Absence
    PRESENT = "✅"        # Présent
    LATE = "⏰"            # Retard
    JUSTIFIED = "🆗"      # Justifié
    UNJUSTIFIED = "⚠️"    # Non justifié
    PENDING = "⌛"        # En attente
    
    # COMMUNICATIONS
    MESSAGE = "💬"        # Message
    EMAIL = "📧"          # Email
    PHONE = "📱"          # Téléphone
    NOTIFICATION = "🔔"   # Notifications
    ALERT = "🚨"          # Alerte
    BELL = "🔔"           # Cloche
    
    # CLASSIFICATION
    CALENDAR = "📅"       # Calendrier
    CLOCK = "🕐"          # Heure
    HISTORY = "📜"        # Historique
    ARCHIVE = "📦"        # Archive
    FOLDER = "📁"         # Dossier
    FILE = "📄"           # Fichier
    
    # DATABASE & REPORTS
    DATABASE = "🗄️"       # Base de données
    REPORT = "📋"         # Rapport
    STATS = "📊"          # Statistiques
    GRAPH = "📉"          # Graphique
    TABLE = "📑"          # Tableau
    LIST = "📝"           # Liste
    
    # SÉCURITÉ & AUTHENTIFICATION
    LOCK = "🔒"           # Verrouillé
    UNLOCK = "🔓"         # Déverrouillé
    KEY = "🔑"            # Clé
    SECURITY = "🛡️"       # Sécurité
    TWO_FACTOR = "🔐"     # 2FA / Authentification double
    LOGIN = "🚪"          # Connexion
    LOGOUT = "🚪"         # Déconnexion
    PASSWORD = "🔐"       # Mot de passe
    
    # STATUTS & ÉTATS
    SUCCESS = "✔️"        # Succès
    ERROR = "❌"          # Erreur
    WARNING = "⚠️"        # Avertissement
    INFO = "ℹ️"           # Information
    WAIT = "⌛"           # Attente
    LOADING = "⏳"        # Chargement
    
    # UTILITAIRES
    DOWNLOAD = "⬇️"       # Télécharger
    UPLOAD = "⬆️"         # Téléverser
    REFRESH = "🔄"        # Actualiser
    SYNC = "🔄"           # Synchroniser
    BACK = "⬅️"           # Retour
    FORWARD = "➡️"        # Suivant
    CLOSE = "❌"          # Fermer
    
    # THÈME & APPARENCE
    SUN = "☀️"            # Jour
    MOON = "🌙"           # Nuit
    THEME = "🎨"          # Thème
    COLOR = "🎨"          # Couleur
    
    # AUTRES
    STAR = "⭐"           # Étoile/Favori
    HEART = "❤️"          # Cœur
    THUMBS_UP = "👍"      # J'approuve
    CHECK = "✓"           # Coché
    CROSS = "✗"           # Non coché
    EYE = "👁️"           # Visible
    EYE_OFF = "👁️‍🗨️"       # Caché
    
    # APPLICATION BRANDING
    APP_LOGO = "✨"       # Logo DanProject
    APP_NAME = "DanProject"  # Nom de l'app
    APP_TAGLINE = "Gestion Intelligente"  # Slogan
    
    @staticmethod
    def get_all() -> dict:
        """Retourne tous les symboles disponibles"""
        return {key: getattr(Symbols, key) for key in dir(Symbols) 
                if not key.startswith('_') and key.isupper() and not callable(getattr(Symbols, key))}
    
    @staticmethod
    def get_by_category(category: str) -> dict:
        """Retourne les symboles d'une catégorie"""
        categories = {
            'navigation': ['HOME', 'DASHBOARD', 'CHART', 'SETTINGS', 'HELP', 'ABOUT'],
            'users': ['STUDENT', 'TEACHER', 'PARENT', 'ADMIN', 'USER', 'PROFILE'],
            'actions': ['ADD', 'DELETE', 'EDIT', 'SAVE', 'CANCEL', 'SEARCH', 'FILTER', 'EXPORT', 'IMPORT', 'PRINT'],
            'absence': ['ABSENCE', 'PRESENT', 'LATE', 'JUSTIFIED', 'UNJUSTIFIED', 'PENDING'],
            'communication': ['MESSAGE', 'EMAIL', 'PHONE', 'NOTIFICATION', 'ALERT', 'BELL'],
            'data': ['DATABASE', 'REPORT', 'STATS', 'GRAPH', 'TABLE', 'LIST'],
            'security': ['LOCK', 'UNLOCK', 'KEY', 'SECURITY', '2FA', 'LOGIN', 'LOGOUT', 'PASSWORD'],
            'status': ['SUCCESS', 'ERROR', 'WARNING', 'INFO', 'WAIT', 'LOADING'],
            'ui': ['DOWNLOAD', 'UPLOAD', 'REFRESH', 'SYNC', 'BACK', 'FORWARD', 'CLOSE'],
            'theme': ['SUN', 'MOON', 'THEME', 'COLOR'],
        }
        
        result = {}
        if category in categories:
            for symbol_name in categories[category]:
                result[symbol_name] = getattr(Symbols, symbol_name, '')
        return result

class IconText:
    """Textes d'icônes personnalisés"""
    
    @staticmethod
    def add_icon(text: str, symbol: str) -> str:
        """Ajoute une icône à un texte"""
        return f"{symbol} {text}"
    
    @staticmethod
    def button_text(label: str, symbol: Optional[str] = None) -> str:
        """Formate le texte d'un bouton avec icône"""
        if symbol:
            return f"{symbol} {label}"
        return label
    
    @staticmethod
    def menu_item(label: str, symbol: str) -> str:
        """Formate l'élément d'un menu"""
        return f"{symbol} {label}"
    
    @staticmethod
    def section_title(title: str, symbol: Optional[str] = None) -> str:
        """Formate le titre d'une section"""
        if symbol:
            return f"{symbol} {title}"
        return title
    
    @staticmethod
    def notification(message: str, symbol: Optional[str] = None) -> str:
        """Formate une notification"""
        if symbol:
            return f"{symbol} {message}"
        return message

# Instance pour utilisation facilitée
symbols = Symbols()
