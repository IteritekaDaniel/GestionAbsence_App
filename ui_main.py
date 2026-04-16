"""
ui_main.py — Fenêtre principale avec sidebar de navigation
Design moderne DanProject - Doré, Bleu, Rose
"""

import customtkinter as ctk
from ui_students  import StudentsView
from ui_absences  import AbsencesView
from ui_stats     import StatsView
from ui_settings  import SettingsView
from ui_parents   import ParentsView
from ui_absence_requests import AbsenceRequestsView
from ui_alerts    import AlertsView
from ui_admins    import AdminsView
from ui_audit     import AuditView
from ui_reports   import ReportsView
from theme import ThemeManager
from notifications import NotificationManager
from shortcuts import ShortcutManager
from i18n import I18nManager, t


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DanProject — Gestion Intelligente")
        self.geometry("1400x850")
        self.minsize(1200, 750)
        
        # Initialiser les managers
        NotificationManager.set_root(self)
        ThemeManager.subscribe(self._on_theme_change)
        
        self._build_layout()
        self._setup_shortcuts()
        self._show_view("etudiants")   # Vue par défaut
        self._center()
        
        # Notification de bienvenue
        NotificationManager.success("Bienvenue!", "Connecté à DanProject")

    def _center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 1200) // 2
        y = (self.winfo_screenheight() - 750)  // 2
        self.geometry(f"1200x750+{x}+{y}")

    def _build_layout(self):
        # ═══════════════════════════════════════════════════════════════
        #   SIDEBAR gauche - Design moderne Bleu/Doré/Rose
        # ═══════════════════════════════════════════════════════════════
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0,
                                   fg_color=ThemeManager.get_color("sidebar"))
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo avec design moderne
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(padx=15, pady=(20, 10), fill="x")
        
        # Logo texte avec dégradé de style
        ctk.CTkLabel(logo_frame, text="✨ DanProject",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=ThemeManager.get_color("accent_gold")).pack(side="left")
        
        # Version
        ver_label = ctk.CTkLabel(logo_frame, text="2.0",
                     text_color=ThemeManager.get_color("accent_rose"),
                     font=ctk.CTkFont(size=9, weight="bold"))
        ver_label.pack(side="right", padx=5)
        
        _separator(self.sidebar)

        # ── Groupe 1 : GESTION ────────────────────────────────
        ctk.CTkLabel(self.sidebar, text="GESTION",
                     text_color=ThemeManager.get_color("text_light"),
                     font=ctk.CTkFont(size=10, weight="bold")).pack(
            anchor="w", padx=15, pady=(15, 8))

        nav_items_gestion = [
            ("👥   Étudiants",    "etudiants"),
            ("👨‍👩‍👧   Parents",      "parents"),
            ("📅   Absences",     "absences"),
        ]

        # ── Groupe 2 : SUIVI ──────────────────────────────────
        nav_items_suivi = [
            ("📋   Demandes",     "demandes"),
            ("🔔   Alertes",      "alertes"),
            ("📊   Statistiques", "statistiques"),
        ]

        # ── Groupe 3 : OUTILS ─────────────────────────────────
        nav_items_outils = [
            ("📈   Rapports",     "rapports"),
            ("🔐   Administrateurs", "admins"),
            ("📋   Audit",        "audit"),
            ("⚙️    Paramètres",  "parametres"),
        ]

        self.nav_btns: dict[str, ctk.CTkButton] = {}

        def _add_group(items):
            for label, key in items:
                btn = ctk.CTkButton(
                    self.sidebar,
                    text=label, anchor="w", height=42,
                    corner_radius=8,
                    fg_color="transparent",
                    hover_color=ThemeManager.get_color("hover"),
                    font=ctk.CTkFont(size=12),
                    command=lambda k=key: self._show_view(k),
                )
                btn.pack(padx=15, pady=2, fill="x")
                self.nav_btns[key] = btn

        _add_group(nav_items_gestion)
        _separator(self.sidebar)

        ctk.CTkLabel(self.sidebar, text="SUIVI",
                     text_color=ThemeManager.get_color("text_light"),
                     font=ctk.CTkFont(size=10, weight="bold")).pack(
            anchor="w", padx=15, pady=(15, 8))
        _add_group(nav_items_suivi)
        _separator(self.sidebar)

        ctk.CTkLabel(self.sidebar, text="ADMINISTRATION",
                     text_color=ThemeManager.get_color("text_light"),
                     font=ctk.CTkFont(size=10, weight="bold")).pack(
            anchor="w", padx=15, pady=(15, 8))
        _add_group(nav_items_outils)

        # ── Boutons en bas (thème + déconnexion) ──────────────────────────────
        _separator(self.sidebar, side="bottom")
        
        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.pack(padx=15, pady=12, fill="x", side="bottom")
        
        # Bouton thème avec couleur doré/rose
        ctk.CTkButton(
            bottom_frame,
            text="🌙   Thème", anchor="w", height=36, width=100,
            corner_radius=8,
            fg_color="transparent",
            hover_color=ThemeManager.get_color("hover"),
            font=ctk.CTkFont(size=11),
            command=self._toggle_theme,
        ).pack(fill="x", pady=(0, 8))
        
        ctk.CTkButton(
            bottom_frame,
            text="🚪   Quitter", anchor="w", height=40,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#4a1010",
            text_color=ThemeManager.get_color("accent_rose"),
            font=ctk.CTkFont(size=12),
            command=self._logout,
        ).pack(fill="x")

        # ═══════════════════════════════════════════════════════════════
        #   ZONE DE CONTENU principale (droite)
        # ═══════════════════════════════════════════════════════════════
        
        # En-tête avec gradient bleu-doré
        self.header = ctk.CTkFrame(self, fg_color=ThemeManager.get_color("card"),
                                   corner_radius=10, height=70)
        self.header.pack(side="top", fill="x", padx=15, pady=15)
        self.header.pack_propagate(False)
        
        header_content = ctk.CTkFrame(self.header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Titre dynamique avec couleur doré
        self.title_label = ctk.CTkLabel(header_content, text="",
                                       font=ctk.CTkFont(size=18, weight="bold"),
                                       text_color=ThemeManager.get_color("accent_gold"))
        self.title_label.pack(side="left", anchor="w")
        
        # Barre de recherche
        self.search_entry = ctk.CTkEntry(header_content, placeholder_text="🔍 Rechercher...",
                                        width=250, height=36)
        self.search_entry.pack(side="left", padx=(20, 0))

        # Zone de contenu
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.pack(side="left", fill="both", expand=True, padx=15, pady=(0, 15))

        # Instancier chaque vue une seule fois
        self.views: dict[str, ctk.CTkFrame] = {
            "etudiants":    StudentsView(self.content),
            "parents":      ParentsView(self.content),
            "absences":     AbsencesView(self.content),
            "demandes":     AbsenceRequestsView(self.content),
            "alertes":      AlertsView(self.content),
            "statistiques": StatsView(self.content),
            "rapports":     ReportsView(self.content),
            "admins":       AdminsView(self.content),
            "audit":        AuditView(self.content),
            "parametres":   SettingsView(self.content),
        }
        for v in self.views.values():
            v.pack_forget()    # toutes cachées au départ

    def _show_view(self, key: str):
        """Affiche la vue demandée, cache les autres, met à jour la sidebar."""
        # Dictionnaire de titres pour chaque vue
        titles = {
            "etudiants": "👥 Gestion des Étudiants",
            "parents": "👨‍👩‍👧 Gestion des Parents",
            "absences": "📅 Gestion des Absences",
            "demandes": "📋 Demandes de Validation",
            "alertes": "🔔 Alertes d'Absences",
            "statistiques": "📊 Statistiques",
            "rapports": "📈 Rapports",
            "admins": "🔐 Gestion des Administrateurs",
            "audit": "📋 Journal d'Audit",
            "parametres": "⚙️ Paramètres",
        }
        
        # Mettre à jour le titre
        self.title_label.configure(text=titles.get(key, ""))
        
        # Mettre en valeur le bouton actif
        for k, btn in self.nav_btns.items():
            if k == key:
                btn.configure(fg_color=("gray75", "gray25"),
                              font=ctk.CTkFont(size=12, weight="bold"))
            else:
                btn.configure(fg_color="transparent",
                              font=ctk.CTkFont(size=12))

        # Afficher / cacher les vues
        for k, view in self.views.items():
            if k == key:
                view.pack(fill="both", expand=True)
                if hasattr(view, "refresh"):
                    view.refresh()    # recharger les données à chaque visite
            else:
                view.pack_forget()
    
    def _setup_shortcuts(self):
        """Configu les raccourcis clavier"""
        shortcuts = [
            ("<Control-1>", lambda: self._show_view("etudiants")),
            ("<Control-2>", lambda: self._show_view("absences")),
            ("<Control-3>", lambda: self._show_view("parents")),
            ("<Control-4>", lambda: self._show_view("demandes")),
            ("<Control-5>", lambda: self._show_view("statistiques")),
            ("<Control-6>", lambda: self._show_view("rapports")),
            ("<Control-7>", lambda: self._show_view("alertes")),
            ("<Control-8>", lambda: self._show_view("audit")),
            ("<Control-Shift-s>", lambda: self._show_view("parametres")),
            ("<Control-Shift-t>", lambda: self._toggle_theme()),
            ("<Control-Shift-q>", lambda: self._logout()),
        ]
        
        for shortcut, callback in shortcuts:
            self.bind(shortcut, lambda e, c=callback: c())
    
    def _toggle_theme(self):
        """Bascule entre thème clair et sombre"""
        ThemeManager.toggle()
        current = ThemeManager.get_current()
        NotificationManager.success("Thème changé", 
                                   f"Mode {'sombre' if current == 'dark' else 'clair'} activé")
    
    def _on_theme_change(self):
        """Callback quand le thème change"""
        # Mettre à jour les couleurs
        colors = ThemeManager.get_all()
        
        # Mettre à jour le sidebar
        self.sidebar.configure(fg_color=colors["sidebar"])
        
        # Mettre à jour le header
        self.header.configure(fg_color=colors["card"])
        self.title_label.configure(text_color=colors["accent"])

    def _logout(self):
        """Déconnexion"""
        self.destroy()
        from ui_login import LoginWindow
        LoginWindow().mainloop()


# ── Helper ────────────────────────────────────────────────────────────────────
def _separator(parent, side=None):
    """Ligne de séparation horizontale dans la sidebar."""
    kw = {"fill": "x", "padx": 15, "pady": 8}
    if side:
        kw["side"] = side
    ctk.CTkFrame(parent, height=1, fg_color="gray30").pack(**kw)
