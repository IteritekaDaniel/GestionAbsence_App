"""
advanced_widgets.py — Widgets personnalisés avancés
Composants UI modernes et réutilisables pour DanProject
"""

import customtkinter as ctk
from theme_advanced import advanced_theme_manager as theme
from typing import Callable, Optional, Any
from datetime import datetime

class ModernCard(ctk.CTkFrame):
    """Carte moderne avec ombre et bordure"""
    
    def __init__(self, parent, title: str = "", **kwargs):
        super().__init__(parent, fg_color=theme.get_color('card_bg'), **kwargs)
        self.title = title
        
        # Bordure
        border_frame = ctk.CTkFrame(
            self, 
            fg_color=theme.get_color('card_border'),
            width=1,
            height=1
        )
        border_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Titre
        if title:
            title_label = ctk.CTkLabel(
                self,
                text=title,
                font=("Segoe UI", 14, "bold"),
                text_color=theme.get_color('text_primary')
            )
            title_label.pack(padx=15, pady=15, anchor="w")

class GradientButton(ctk.CTkButton):
    """Bouton avec effet gradient"""
    
    def __init__(self, parent, text: str, color_scheme: str = "gold", **kwargs):
        colors = {
            'gold': (theme.get_color('accent_gold'), theme.get_color('accent_gold_hover')),
            'blue': (theme.get_color('accent_blue'), theme.get_color('accent_blue_hover')),
            'rose': (theme.get_color('accent_rose'), theme.get_color('accent_rose_hover')),
        }
        
        bg_color, hover_color = colors.get(color_scheme, colors['gold'])
        
        super().__init__(
            parent,
            text=text,
            fg_color=bg_color,
            hover_color=hover_color,
            text_color="white" if color_scheme != 'gold' else "#0F172A",
            font=("Segoe UI", 12, "bold"),
            **kwargs
        )

class AnimatedLabel(ctk.CTkLabel):
    """Label avec animations de couleur"""
    
    def __init__(self, parent, text: str = "", **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.normal_color = theme.get_color('text_primary')
        self.hover_color = theme.get_color('accent_gold')
        self.text_color = self.normal_color
        self.configure(text_color=self.text_color)
        
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
    
    def _on_hover(self, event=None):
        """Changement de couleur au survol"""
        self.configure(text_color=self.hover_color)
    
    def _on_leave(self, event=None):
        """Retour à la couleur normale"""
        self.configure(text_color=self.normal_color)

class StatCard(ctk.CTkFrame):
    """Carte de statistique avec nombre et description"""
    
    def __init__(self, parent, label: str, value: str, icon: str = "📊", **kwargs):
        super().__init__(parent, fg_color=theme.get_color('surface_secondary'), **kwargs)
        
        # Contenu principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Icône et label
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        icon_label = ctk.CTkLabel(
            header,
            text=icon,
            font=("Segoe UI", 24)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        label_text = ctk.CTkLabel(
            header,
            text=label,
            font=("Segoe UI", 11),
            text_color=theme.get_color('text_secondary')
        )
        label_text.pack(side="left")
        
        # Valeur
        value_label = ctk.CTkLabel(
            main_frame,
            text=value,
            font=("Segoe UI", 24, "bold"),
            text_color=theme.get_color('accent_gold')
        )
        value_label.pack(anchor="w", pady=(10, 0))

class ProgressIndicator(ctk.CTkFrame):
    """Indicateur de progrès personnalisé"""
    
    def __init__(self, parent, label: str = "", value: float = 0, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.value = max(0, min(100, value))
        
        # Label
        label_frame = ctk.CTkFrame(self, fg_color="transparent")
        label_frame.pack(fill="x", padx=5, pady=(0, 5))
        
        ctk.CTkLabel(
            label_frame,
            text=label,
            font=("Segoe UI", 11),
            text_color=theme.get_color('text_secondary')
        ).pack(side="left")
        
        value_text = ctk.CTkLabel(
            label_frame,
            text=f"{int(self.value)}%",
            font=("Segoe UI", 11, "bold"),
            text_color=theme.get_color('accent_gold')
        )
        value_text.pack(side="right")
        
        # Barre
        bar_frame = ctk.CTkFrame(
            self,
            height=8,
            fg_color=theme.get_color('surface_tertiary')
        )
        bar_frame.pack(fill="x", padx=5, pady=(0, 10))
        bar_frame.configure(height=8)
        
        # Progression
        progress_frame = ctk.CTkFrame(
            bar_frame,
            fg_color=theme.get_color('accent_gold'),
            height=8
        )
        progress_frame.pack(side="left", fill="y")
        progress_frame.configure(width=int(self.value * 2))  # Approximation

class NotificationBadge(ctk.CTkLabel):
    """Badge de notification"""
    
    def __init__(self, parent, count: int = 0, **kwargs):
        super().__init__(
            parent,
            text=str(count) if count > 0 else "",
            font=("Segoe UI", 10, "bold"),
            text_color="white",
            fg_color=theme.get_color('accent_rose_main'),
            width=24,
            height=24,
            corner_radius=12,
            **kwargs
        )

class TabView(ctk.CTkTabview):
    """Vue par onglets personnalisée"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Styling des onglets
        self.configure(
            fg_color=theme.get_color('surface_bg'),
            segmented_button_fg_color=theme.get_color('surface_secondary'),
            text_color=theme.get_color('text_secondary'),
            text_color_state="disabled"
        )

class InfoBox(ctk.CTkFrame):
    """Boîte d'information avec type (info/success/warning/error)"""
    
    def __init__(self, parent, message: str, msg_type: str = "info", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        colors_map = {
            'info': '#3B82F6',
            'success': '#10B981',
            'warning': '#F59E0B',
            'error': '#EC4899',
        }
        
        color = colors_map.get(msg_type, '#3B82F6')
        icons = {
            'info': 'ℹ️',
            'success': '✔️',
            'warning': '⚠️',
            'error': '❌',
        }
        
        # Barre gauche
        left_bar = ctk.CTkFrame(self, fg_color=color, width=4)
        left_bar.pack(side="left", fill="y", padx=(0, 10))
        left_bar.configure(width=4)
        
        # Contenu
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        icon_text = ctk.CTkLabel(
            content_frame,
            text=icons[msg_type],
            font=("Segoe UI", 14)
        )
        icon_text.pack(side="left", padx=(0, 10))
        
        message_label = ctk.CTkLabel(
            content_frame,
            text=message,
            font=("Segoe UI", 11),
            text_color=theme.get_color('text_primary'),
            wraplength=300
        )
        message_label.pack(side="left", fill="both", expand=True)
