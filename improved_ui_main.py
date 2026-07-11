"""
improved_ui_main.py — Interface principale améliorée
Support complet du thème système, widgets avancés, symboles modernes
"""

import customtkinter as ctk
from pathlib import Path
import sys

# ═════════════════════════════════════════════════════════════════════════════
# IMPORTS - Nouveaux modules
# ═════════════════════════════════════════════════════════════════════════════

from theme_advanced import advanced_theme_manager as theme
from advanced_widgets import ModernCard, GradientButton, StatCard, ProgressIndicator, InfoBox
from user_preferences import user_preferences
from symbols import Symbols, IconText
from analytics import analytics
from image_manager import image_manager

# ═════════════════════════════════════════════════════════════════════════════
# IMPORTS - Views existantes
# ═════════════════════════════════════════════════════════════════════════════

from ui_students import StudentsView
from ui_absences import AbsencesView
from ui_stats import StatsView
from ui_settings import SettingsView
from ui_parents import ParentsView
from ui_absence_requests import AbsenceRequestsView
from ui_alerts import AlertsView
from ui_admins import AdminsView
from ui_audit import AuditView
from ui_reports import ReportsView
from ui_messages import MessagesView

class ImprovedMainWindow(ctk.CTk):
    """Fenêtre principale améliorée avec support complet du thème système"""
    
    def __init__(self):
        super().__init__()
        
        # Configuration window
        self.title(f"DanProject v2.0 — {Symbols.APP_TAGLINE}")
        
        # Charger la géométrie sauvegardée
        geometry = user_preferences.get_window_geometry()
        self.geometry(f"{geometry[0]}x{geometry[1]}+{geometry[2]}+{geometry[3]}")
        self.minsize(1200, 700)
        
        # Initialiser l'apparence selon les préférences
        theme_pref = user_preferences.get_theme()
        if theme_pref == 'dark':
            theme.set_theme('dark')
        elif theme_pref == 'light':
            theme.set_theme('light')
        else:  # system
            theme.enable_system_theme()
        
        # S'abonner aux changements de thème
        theme.subscribe(self._on_theme_changed)
        
        # Initialiser l'UI
        self._build_layout()
        self._setup_keyboard_shortcuts()
        self._show_view('etudiants')
        
        # Analytics
        analytics.track_page_view('main_window')
        
        # Centrer la fenêtre
        self._center_window()
        
        # Notification de bienvenue
        print(f"✨ DanProject v2.0 - Démarrage réussi")
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.winfo_width()) // 2
        y = (screen_height - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    # ═════════════════════════════════════════════════════════════════════════
    # CONSTRUCTION DE L'INTERFACE
    # ═════════════════════════════════════════════════════════════════════════
    
    def _build_layout(self):
        """Construit la mise en page de l'application"""
        
        # Conteneur principal
        main_container = ctk.CTkFrame(self, fg_color=theme.get_color('bg_main'))
        main_container.pack(fill='both', expand=True)
        
        # ═══════════════════════════════════════════════════════════════════
        # SIDEBAR GAUCHE
        # ═══════════════════════════════════════════════════════════════════
        
        sidebar_width = user_preferences.get('sidebar_width', 250)
        self.sidebar = ctk.CTkFrame(
            main_container,
            width=sidebar_width,
            fg_color=theme.get_color('sidebar_bg'),
            corner_radius=0
        )
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        
        # Logo & Header de sidebar
        self._build_sidebar_header()
        
        # Sections de navigation
        self._build_navigation_sections()
        
        # ═══════════════════════════════════════════════════════════════════
        # CONTENU PRINCIPAL
        # ═══════════════════════════════════════════════════════════════════
        
        self.content_frame = ctk.CTkFrame(
            main_container,
            fg_color=theme.get_color('bg_main')
        )
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        # Content container
        self.view_container = ctk.CTkFrame(
            self.content_frame,
            fg_color=theme.get_color('bg_main')
        )
        self.view_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        self.current_view = None
    
    def _build_sidebar_header(self):
        """Construit l'en-tête de la sidebar avec logo optimisé"""
        
        header_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color='transparent'
        )
        header_frame.pack(fill='x', padx=15, pady=20)
        
        # Logo avec image optimisée
        logo_container = ctk.CTkFrame(header_frame, fg_color='transparent')
        logo_container.pack(fill='x', pady=(0, 10))
        
        # Charger le logo depuis les assets
        logo_img = image_manager.load_image(
            "logos/danproject_logo.png",
            size=(40, 40),
            use_cache=True
        )
        
        if logo_img:
            logo_img_label = ctk.CTkLabel(
                logo_container,
                image=logo_img,
                text=''
            )
            logo_img_label.pack(side='left', padx=(0, 10))
        
        logo_text = ctk.CTkLabel(
            logo_container,
            text="DanProject",
            font=('Segoe UI', 16, 'bold'),
            text_color=theme.get_color('accent_gold_main')
        )
        logo_text.pack(side='left')
        
        version_text = ctk.CTkLabel(
            logo_container,
            text='2.0',
            font=('Segoe UI', 10, 'bold'),
            text_color=theme.get_color('accent_rose_main')
        )
        version_text.pack(side='right')
        
        # Divider
        divider = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=theme.get_color('surface_border')
        )
        divider.pack(fill='x', padx=10, pady=(0, 15))
        divider.configure(height=1)
    
    def _build_navigation_sections(self):
        """Construit les sections de navigation"""
        
        # Section GESTION
        self._create_nav_section(
            'GESTION',
            [
                ('👥', 'Étudiants', 'etudiants'),
                ('👨‍👩‍👧', 'Parents', 'parents'),
                ('📅', 'Absences', 'absences'),
            ]
        )
        
        # Section SUIVI
        self._create_nav_section(
            'SUIVI',
            [
                ('📋', 'Demandes', 'demandes'),
                ('🔔', 'Alertes', 'alertes'),
                ('📊', 'Statistiques', 'statistiques'),
            ]
        )
        
        # Section COMMUNICATIONS
        self._create_nav_section(
            'COMMUNICATIONS',
            [
                ('📧', 'Messages', 'messages'),
                ('📈', 'Rapports', 'rapports'),
            ]
        )
        
        # Section ADMINISTRATION
        self._create_nav_section(
            'ADMINISTRATION',
            [
                ('🔐', 'Admin', 'admins'),
                ('📋', 'Audit', 'audit'),
            ]
        )
        
        # Spacer
        spacer = ctk.CTkFrame(self.sidebar, fg_color='transparent')
        spacer.pack(fill='both', expand=True)
        
        # Bas de la sidebar (Paramètres + Thème + Logout)
        self._create_footer_section()
    
    def _create_nav_section(self, title: str, items: list):
        """Crée une section de navigation"""
        
        # Titre de section
        section_title = ctk.CTkLabel(
            self.sidebar,
            text=title,
            font=('Segoe UI', 9, 'bold'),
            text_color=theme.get_color('text_tertiary')
        )
        section_title.pack(anchor='w', padx=15, pady=(15, 10))
        
        # Items
        for icon, label, view_id in items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon}  {label}",
                fg_color='transparent',
                hover_color=theme.get_color('sidebar_hover'),
                text_color=theme.get_color('text_secondary'),
                font=('Segoe UI', 11),
                anchor='w',
                command=lambda vid=view_id: self._show_view(vid)
            )
            btn.pack(fill='x', padx=10, pady=5)
    
    def _create_footer_section(self):
        """Crée la section inférieure de la sidebar"""
        
        footer = ctk.CTkFrame(self.sidebar, fg_color='transparent')
        footer.pack(fill='x', padx=10, pady=15)
        
        # Divider
        divider = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=theme.get_color('surface_border')
        )
        divider.pack(fill='x', padx=10, pady=(0, 10))
        divider.configure(height=1)
        
        # Bouton thème (Clair/Sombre/Système)
        def toggle_theme_menu():
            theme_window = ctk.CTkToplevel(self)
            theme_window.title("Thème")
            theme_window.geometry("250x150")
            theme_window.resizable(False, False)
            
            ctk.CTkLabel(
                theme_window,
                text="Sélectionnez le thème:",
                font=('Segoe UI', 12, 'bold')
            ).pack(pady=10)
            
            def set_light():
                theme.set_theme('light')
                user_preferences.set_theme('light')
                theme_window.destroy()
            
            def set_dark():
                theme.set_theme('dark')
                user_preferences.set_theme('dark')
                theme_window.destroy()
            
            def set_system():
                theme.enable_system_theme()
                user_preferences.set_theme('system')
                theme_window.destroy()
            
            ctk.CTkButton(theme_window, text="☀️  Clair", command=set_light).pack(fill='x', padx=10, pady=5)
            ctk.CTkButton(theme_window, text="🌙  Sombre", command=set_dark).pack(fill='x', padx=10, pady=5)
            ctk.CTkButton(theme_window, text="🎨  Système", command=set_system).pack(fill='x', padx=10, pady=5)
        
        theme_btn = ctk.CTkButton(
            footer,
            text="🎨  Thème",
            fg_color=theme.get_color('accent_gold_main'),
            text_color='#0F172A',
            font=('Segoe UI', 10, 'bold'),
            command=toggle_theme_menu,
            height=35
        )
        theme_btn.pack(fill='x', pady=5)
        
        # Bouton Paramètres
        settings_btn = ctk.CTkButton(
            footer,
            text="⚙️  Paramètres",
            fg_color=theme.get_color('accent_blue_main'),
            text_color='white',
            font=('Segoe UI', 10, 'bold'),
            command=lambda: self._show_view('parametres'),
            height=35
        )
        settings_btn.pack(fill='x', pady=5)
        
        # Bouton Quitter
        logout_btn = ctk.CTkButton(
            footer,
            text="🚪  Quitter",
            fg_color=theme.get_color('error'),
            text_color='white',
            font=('Segoe UI', 10, 'bold'),
            command=self._quit_application,
            height=35
        )
        logout_btn.pack(fill='x', pady=5)
    
    # ═════════════════════════════════════════════════════════════════════
    # GESTION DES VUES
    # ═════════════════════════════════════════════════════════════════════
    
    def _show_view(self, view_id: str):
        """Affiche une vue spécifique"""
        
        # Effacer la vue actuelle
        if self.current_view:
            self.current_view.destroy()
        
        # Créer la nouvelle vue
        views = {
            'etudiants': StudentsView,
            'parents': ParentsView,
            'absences': AbsencesView,
            'demandes': AbsenceRequestsView,
            'alertes': AlertsView,
            'statistiques': StatsView,
            'rapports': ReportsView,
            'admins': AdminsView,
            'audit': AuditView,
            'messages': MessagesView,
            'parametres': SettingsView,
        }
        
        ViewClass = views.get(view_id)
        if ViewClass:
            self.current_view = ViewClass(self.view_container)
            self.current_view.pack(fill='both', expand=True)
            
            # Track analytics
            analytics.track_page_view(view_id)
    
    # ═════════════════════════════════════════════════════════════════════
    # AFFICHAGE ET GESTION DU THÈME
    # ═════════════════════════════════════════════════════════════════════
    
    def _setup_keyboard_shortcuts(self):
        """Configure les raccourcis clavier"""
        
        shortcuts = {
            '<Control-1>': lambda: self._show_view('etudiants'),
            '<Control-2>': lambda: self._show_view('parents'),
            '<Control-3>': lambda: self._show_view('absences'),
            '<Control-4>': lambda: self._show_view('demandes'),
            '<Control-5>': lambda: self._show_view('alertes'),
            '<Control-6>': lambda: self._show_view('statistiques'),
            '<Control-7>': lambda: self._show_view('rapports'),
            '<Control-8>': lambda: self._show_view('admins'),
            '<Control-Shift-t>': lambda: theme.toggle_theme(),
            '<Control-Shift-q>': lambda: self._quit_application(),
        }
        
        for shortcut, command in shortcuts.items():
            self.bind(shortcut, lambda e, cmd=command: cmd())
    
    def _on_theme_changed(self):
        """Appelé quand le thème change"""
        print(f"Thème changé: {theme.current_theme}")
        # Redessiner si nécessaire
        self.after(100, self._refresh_ui)
    
    def _refresh_ui(self):
        """Actualise l'UI après un changement de thème"""
        # Reconfigure les couleurs
        self.sidebar.configure(fg_color=theme.get_color('sidebar_bg'))
        self.content_frame.configure(fg_color=theme.get_color('bg_main'))
        self.view_container.configure(fg_color=theme.get_color('bg_main'))
    
    def _quit_application(self):
        """Quitte l'application"""
        # Sauvegarder la géométrie
        try:
            geom = self.geometry()
            if geom and '+' in geom:
                parts = geom.split('+')
                if len(parts) >= 3:
                    dims = parts[0].split('x')
                    if len(dims) == 2:
                        width, height = int(dims[0]), int(dims[1])
                        x, y = int(parts[1]), int(parts[2])
                        user_preferences.set_window_geometry(width, height, x, y)
        except (ValueError, IndexError):
            pass
        
        analytics.track_action('quit_application')
        self.quit()

def main():
    """Point d'entrée principal"""
    print(f"✨ {Symbols.APP_NAME} v2.0 - Gestion Intelligente")
    print(f"Thème système: {theme.system_theme}")
    print(f"Mode système activé: {theme.use_system_theme}")
    print("-" * 50)
    
    app = ImprovedMainWindow()
    app.mainloop()

if __name__ == '__main__':
    main()
