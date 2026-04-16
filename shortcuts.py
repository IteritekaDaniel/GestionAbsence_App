"""
shortcuts.py — Système de raccourcis clavier
"""

class ShortcutManager:
    """Gestionnaire central des raccourcis clavier"""
    
    SHORTCUTS = {
        # Navigation
        "<Control-1>": ("etudiants", "Ver étudiants"),
        "<Control-2>": ("absences", "Voir absences"),
        "<Control-3>": ("parents", "Voir parents"),
        "<Control-4>": ("demandes", "Voir demandes"),
        "<Control-5>": ("stats", "Voir statistiques"),
        "<Control-6>": ("rapports", "Voir rapports"),
        "<Control-7>": ("alertes", "Voir alertes"),
        "<Control-8>": ("audit", "Voir audit"),
        
        # Actions générales
        "<Control-n>": ("new", "Nouveau"),
        "<Control-f>": ("search", "Rechercher"),
        "<Control-e>": ("export", "Exporter"),
        "<Control-p>": ("print", "Imprimer"),
        "<Control-s>": ("save", "Enregistrer"),
        
        # Admin
        "<Control-Shift-s>": ("settings", "Paramètres"),
        "<Control-Shift-a>": ("admins", "Gestion admins"),
        "<Control-Shift-q>": ("logout", "Déconnexion"),
        
        # Interface
        "<Control-Shift-t>": ("toggle_theme", "Basculer thème"),
        "<Control-Shift-l>": ("toggle_lang", "Changer langue"),
        "<Control-h>": ("help", "Aide"),
    }
    
    _callbacks = {}
    
    @classmethod
    def register(cls, shortcut: str, callback):
        """Enregistre un callback pour un raccourci"""
        if shortcut not in cls._callbacks:
            cls._callbacks[shortcut] = []
        cls._callbacks[shortcut].append(callback)
    
    @classmethod
    def unregister(cls, shortcut: str, callback):
        """Désabonne un callback"""
        if shortcut in cls._callbacks:
            cls._callbacks[shortcut].remove(callback)
    
    @classmethod
    def trigger(cls, shortcut: str):
        """Déclenche un raccourci"""
        if shortcut in cls._callbacks:
            for callback in cls._callbacks[shortcut]:
                callback()
    
    @classmethod
    def get_description(cls, shortcut: str) -> str:
        """Récupère la description d'un raccourci"""
        return cls.SHORTCUTS.get(shortcut, ("unknown", "Inconnu"))[1]
    
    @classmethod
    def get_all(cls) -> dict:
        """Retourne tous les raccourcis"""
        return cls.SHORTCUTS.copy()
    
    @classmethod
    def bind_to_widget(cls, widget, shortcut: str, callback):
        """Lie un raccourci à un widget"""
        def wrapper(event):
            callback()
            return "break"
        widget.bind(shortcut, wrapper)
