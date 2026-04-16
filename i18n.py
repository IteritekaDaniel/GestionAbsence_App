"""
i18n.py — Support multi-langue (Français/Anglais)
"""

TRANSLATIONS = {
    "fr": {
        # Général
        "app_title": "AbsencesPro — Système de Gestion des Absences",
        "version": "v2.0 PRO",
        "logout": "Déconnexion",
        
        # Login
        "login_title": "AbsencesPro — Connexion",
        "username": "Nom d'utilisateur",
        "password": "Mot de passe",
        "login": "Se connecter",
        "default_account": "Compte par défaut : admin / admin123",
        "fill_all": "⚠  Remplissez tous les champs",
        "wrong_creds": "❌  Identifiants incorrects",
        
        # Navigation
        "management": "GESTION",
        "students": "Étudiants",
        "absences": "Absences",
        "parents": "Parents",
        "absence_requests": "Demandes",
        
        "tools": "OUTILS",
        "stats": "Statistiques",
        "reports": "Rapports",
        "alerts": "Alertes",
        "audit": "Audit",
        
        "admin": "ADMIN",
        "admins": "Administrateurs",
        "settings": "Paramètres",
        
        # Boutons
        "add": "Ajouter",
        "edit": "Modifier",
        "delete": "Supprimer",
        "save": "Enregistrer",
        "cancel": "Annuler",
        "search": "Rechercher",
        "filter": "Filtrer",
        "export": "Exporter",
        "import": "Importer",
        
        # Messages
        "success": "Succès",
        "error": "Erreur",
        "warning": "Avertissement",
        "confirm": "Confirmer?",
        "deleted": "Supprimé avec succès",
        "saved": "Enregistré avec succès",
        "updated": "Mis à jour avec succès",
    },
    
    "en": {
        # General
        "app_title": "AbsencesPro — Absence Management System",
        "version": "v2.0 PRO",
        "logout": "Logout",
        
        # Login
        "login_title": "AbsencesPro — Login",
        "username": "Username",
        "password": "Password",
        "login": "Sign In",
        "default_account": "Default account: admin / admin123",
        "fill_all": "⚠  Fill all fields",
        "wrong_creds": "❌  Wrong credentials",
        
        # Navigation
        "management": "MANAGEMENT",
        "students": "Students",
        "absences": "Absences",
        "parents": "Parents",
        "absence_requests": "Requests",
        
        "tools": "TOOLS",
        "stats": "Statistics",
        "reports": "Reports",
        "alerts": "Alerts",
        "audit": "Audit",
        
        "admin": "ADMIN",
        "admins": "Administrators",
        "settings": "Settings",
        
        # Buttons
        "add": "Add",
        "edit": "Edit",
        "delete": "Delete",
        "save": "Save",
        "cancel": "Cancel",
        "search": "Search",
        "filter": "Filter",
        "export": "Export",
        "import": "Import",
        
        # Messages
        "success": "Success",
        "error": "Error",
        "warning": "Warning",
        "confirm": "Confirm?",
        "deleted": "Deleted successfully",
        "saved": "Saved successfully",
        "updated": "Updated successfully",
    }
}

class I18nManager:
    """Gestionnaire de traductions"""
    
    _current_lang = "fr"
    _callbacks = []
    
    @classmethod
    def set_language(cls, lang: str):
        """Change la langue"""
        if lang in TRANSLATIONS:
            cls._current_lang = lang
            for callback in cls._callbacks:
                callback()
    
    @classmethod
    def get(cls, key: str) -> str:
        """Récupère une traduction"""
        tree = TRANSLATIONS.get(cls._current_lang, {})
        return tree.get(key, key)
    
    @classmethod
    def current_lang(cls) -> str:
        """Retourne la langue actuelle"""
        return cls._current_lang
    
    @classmethod
    def subscribe(cls, callback):
        """S'abonner aux changements de langue"""
        cls._callbacks.append(callback)
    
    @classmethod
    def unsubscribe(cls, callback):
        """Se désabonner"""
        if callback in cls._callbacks:
            cls._callbacks.remove(callback)

# Alias pour simplifier l'utilisation
def t(key: str) -> str:
    """Traduction rapide"""
    return I18nManager.get(key)
