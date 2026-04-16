"""
notifications.py — Système de notifications temps réel (toasts)
"""

import customtkinter as ctk
from queue import Queue
import threading

class NotificationManager:
    """Gestionnaire centralisé de notifications"""
    
    _queue = Queue()
    _active_notifications = {}
    _root = None
    
    @classmethod
    def set_root(cls, root):
        """Définir la fenêtre racine"""
        cls._root = root
    
    @classmethod
    def info(cls, title: str, message: str, duration: int = 3000):
        """Notification info"""
        cls._show("info", title, message, duration)
    
    @classmethod
    def success(cls, title: str, message: str, duration: int = 3000):
        """Notification succès"""
        cls._show("success", title, message, duration)
    
    @classmethod
    def warning(cls, title: str, message: str, duration: int = 4000):
        """Notification avertissement"""
        cls._show("warning", title, message, duration)
    
    @classmethod
    def error(cls, title: str, message: str, duration: int = 5000):
        """Notification erreur"""
        cls._show("error", title, message, duration)
    
    @classmethod
    def _show(cls, notification_type: str, title: str, message: str, duration: int):
        """Affiche une notification"""
        if cls._root is None:
            print(f"[{notification_type.upper()}] {title}: {message}")
            return
        
        # Config de couleur par type
        colors = {
            "success": ("#2ecc71", "#ffffff"),
            "error": ("#e74c3c", "#ffffff"),
            "warning": ("#f39c12", "#ffffff"),
            "info": ("#3498db", "#ffffff"),
        }
        
        bg_color, fg_color = colors.get(notification_type, ("#3498db", "#ffffff"))
        
        # Créer la notification
        notif = ctk.CTkToplevel(cls._root)
        notif.geometry("350x100")
        notif.attributes("-topmost", True)
        notif.overrideredirect(True)
        notif.configure(fg_color=bg_color)
        
        # Position: coin bas droit
        notif.update_idletasks()
        x = cls._root.winfo_x() + cls._root.winfo_width() - 370
        y = cls._root.winfo_y() + cls._root.winfo_height() - 130
        notif.geometry(f"+{x}+{y}")
        
        # Contenu
        frame = ctk.CTkFrame(notif, fg_color=bg_color)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(frame, text=f"✓ {title}", text_color=fg_color,
                     font=("Arial", 13, "bold")).pack(anchor="w")
        ctk.CTkLabel(frame, text=message, text_color=fg_color,
                     font=("Arial", 11)).pack(anchor="w", pady=(3, 0))
        
        # Auto-fermer après duration ms
        def close():
            notif.destroy()
        
        notif.after(duration, close)
