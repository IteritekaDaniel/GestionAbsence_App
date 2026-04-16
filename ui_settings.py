"""
ui_settings.py — Vue "Paramètres"
Gère le thème, le compte admin, et affiche les infos de l'application.
"""

import customtkinter as ctk
from tkinter import messagebox
import services


class SettingsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self._build_ui()

    # ─────────────────────────────────────────────────────────────────
    #   Construction
    # ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        ctk.CTkLabel(self, text="⚙️ Paramètres",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(
            anchor="w", padx=15, pady=(15, 10)
        )

        # Scrollable pour accommoder tous les paramètres
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=15, pady=5)

        # ── Section : Thème ───────────────────────────────────────────
        _section(scroll, "🎨  Thème de l'interface")

        ctk.CTkLabel(scroll, text="Mode d'affichage").pack(
            anchor="w", padx=15, pady=(0, 4)
        )
        self.cmb_theme = ctk.CTkOptionMenu(
            scroll,
            values=["Sombre", "Clair", "Système"],
            command=self._change_theme,
            width=160,
        )
        self.cmb_theme.set("Sombre")
        self.cmb_theme.pack(anchor="w", padx=15, pady=(0, 20))

        # ── Section : Compte admin ────────────────────────────────────
        _section(scroll, "👤  Compte Administrateur")

        grid = ctk.CTkFrame(scroll, fg_color="transparent")
        grid.pack(fill="x", padx=15, pady=(0, 10))

        # Colonne gauche
        left = ctk.CTkFrame(grid, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=(0, 12))

        ctk.CTkLabel(left, text="Nom d'utilisateur").pack(anchor="w", pady=(0, 3))
        self.ent_username = ctk.CTkEntry(left, height=38)
        self.ent_username.pack(fill="x")

        ctk.CTkLabel(left, text="Email").pack(anchor="w", pady=(12, 3))
        self.ent_email = ctk.CTkEntry(left, height=38)
        self.ent_email.pack(fill="x")

        # Colonne droite
        right = ctk.CTkFrame(grid, fg_color="transparent")
        right.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(right, text="Nouveau mot de passe").pack(anchor="w", pady=(0, 3))
        self.ent_pwd = ctk.CTkEntry(right, show="•", height=38)
        self.ent_pwd.pack(fill="x")

        ctk.CTkLabel(right, text="Confirmer le mot de passe").pack(anchor="w", pady=(12, 3))
        self.ent_pwd2 = ctk.CTkEntry(right, show="•", height=38)
        self.ent_pwd2.pack(fill="x")

        ctk.CTkLabel(scroll, text="Laissez le mot de passe vide pour le conserver.",
                     text_color="gray", font=ctk.CTkFont(size=11)).pack(
            anchor="w", padx=15, pady=(4, 6)
        )

        self.lbl_msg = ctk.CTkLabel(scroll, text="", font=ctk.CTkFont(size=12))
        self.lbl_msg.pack(pady=4)

        ctk.CTkButton(scroll, text="💾  Sauvegarder les modifications",
                      height=40, command=self._save_account).pack(pady=(4, 20))

        # ── Section : À propos ────────────────────────────────────────
        _section(scroll, "ℹ️  À propos")
        ctk.CTkLabel(
            scroll,
            text=(
                "AbsencesPro  v1.0\n"
                "Application de gestion des absences scolaires\n"
                "Développé avec  Python · CustomTkinter · SQLite · Matplotlib"
            ),
            text_color="gray",
            justify="left",
        ).pack(anchor="w", padx=15, pady=(0, 20))

    # ─────────────────────────────────────────────────────────────────
    #   Rafraîchissement
    # ─────────────────────────────────────────────────────────────────

    def refresh(self):
        """Recharge les infos admin dans les champs."""
        info = services.get_admin_info()
        self.ent_username.delete(0, "end")
        self.ent_username.insert(0, info.get("username", ""))
        self.ent_email.delete(0, "end")
        self.ent_email.insert(0, info.get("email", ""))
        self.lbl_msg.configure(text="")

    # ─────────────────────────────────────────────────────────────────
    #   Actions
    # ─────────────────────────────────────────────────────────────────

    def _change_theme(self, theme: str):
        mapping = {"Sombre": "dark", "Clair": "light", "Système": "system"}
        ctk.set_appearance_mode(mapping.get(theme, "dark"))

    def _save_account(self):
        username = self.ent_username.get().strip()
        email    = self.ent_email.get().strip()
        pwd      = self.ent_pwd.get()
        pwd2     = self.ent_pwd2.get()

        if not username:
            self.lbl_msg.configure(
                text="⚠  Le nom d'utilisateur est obligatoire",
                text_color="#ff6b6b"
            )
            return

        if pwd and pwd != pwd2:
            self.lbl_msg.configure(
                text="⚠  Les mots de passe ne correspondent pas",
                text_color="#ff6b6b"
            )
            return

        services.update_admin(username, email, pwd if pwd else None)
        self.lbl_msg.configure(text="✅  Modifications enregistrées", text_color="#90ee90")

        # Effacer les champs mot de passe
        self.ent_pwd.delete(0, "end")
        self.ent_pwd2.delete(0, "end")


# ─────────────────────────────────────────────────────────────────────────────
#   Helper
# ─────────────────────────────────────────────────────────────────────────────

def _section(parent, title: str):
    """Ajoute un titre de section + séparateur."""
    ctk.CTkLabel(parent, text=title,
                 font=ctk.CTkFont(size=14, weight="bold")).pack(
        anchor="w", padx=15, pady=(16, 6)
    )
    ctk.CTkFrame(parent, height=1, fg_color="gray30").pack(
        fill="x", padx=15, pady=(0, 12)
    )
