"""
theme.py — Système de thème global (Doré, Bleu, Rose)
Design moderne et élégant pour DanProject
"""

# ═════════════════════════════════════════════════════════════════════════════
#   THÈMES MODERNES
# ═════════════════════════════════════════════════════════════════════════════

LIGHT_THEME = {
    # Couleurs primaires (Bleu & Doré)
    "bg": "#f8f9fc",
    "fg": "#1a1a2e",
    "accent": "#1e40af",  # Bleu royal
    "accent_light": "#e0e7ff",
    "accent_gold": "#d4af37",  # Doré élégant
    "accent_rose": "#ec4899",  # Rose moderne
    
    # Surfaces
    "border": "#e5e7eb",
    "sidebar": "#ffffff",
    "card": "#ffffff",
    
    # Textes
    "text_light": "#6b7280",
    "text_dark": "#1f2937",
    
    # États
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "info": "#3b82f6",
    "hover": "#f3f4f6",
}

DARK_THEME = {
    # Couleurs primaires (Bleu foncé & Doré & Rose)
    "bg": "#0f172a",
    "fg": "#f1f5f9",
    "accent": "#3b82f6",  # Bleu ciel
    "accent_light": "#1e3a8a",
    "accent_gold": "#fbbf24",  # Doré lumineux
    "accent_rose": "#f472b6",  # Rose clair
    
    # Surfaces
    "border": "#1e293b",
    "sidebar": "#0f172a",
    "card": "#1e293b",
    
    # Textes
    "text_light": "#94a3b8",
    "text_dark": "#f1f5f9",
    
    # États
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#f87171",
    "info": "#60a5fa",
    "hover": "#1e293b",
}

class ThemeManager:
    """Gestionnaire global de thème"""
    
    _current_theme = "light"
    _theme = LIGHT_THEME.copy()
    _callbacks = []
    
    @classmethod
    def set_theme(cls, theme_name: str):
        """Change le thème (light/dark)"""
        if theme_name == "light":
            cls._current_theme = "light"
            cls._theme = LIGHT_THEME.copy()
        elif theme_name == "dark":
            cls._current_theme = "dark"
            cls._theme = DARK_THEME.copy()
        
        # Notifier tous les observateurs
        for callback in cls._callbacks:
            callback()
    
    @classmethod
    def get_current(cls) -> str:
        """Retourne le thème actuel"""
        return cls._current_theme
    
    @classmethod
    def get_color(cls, key: str) -> str:
        """Retourne une couleur du thème"""
        return cls._theme.get(key, "#ffffff")
    
    @classmethod
    def get_all(cls) -> dict:
        """Retourne tout le thème"""
        return cls._theme.copy()
    
    @classmethod
    def subscribe(cls, callback):
        """S'abonner aux changements de thème"""
        cls._callbacks.append(callback)
    
    @classmethod
    def unsubscribe(cls, callback):
        """Se désabonner"""
        if callback in cls._callbacks:
            cls._callbacks.remove(callback)
    
    @classmethod
    def toggle(cls):
        """Bascule clair/sombre"""
        new_theme = "dark" if cls._current_theme == "light" else "light"
        cls.set_theme(new_theme)
