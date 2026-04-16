"""
ui_login.py — Fenêtre de connexion DanProject
Design moderne avec couleurs doré, bleu, rose
"""

import customtkinter as ctk
import services
from theme import ThemeManager


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DanProject — Connexion")
        self.geometry("420x530")
        self.resizable(False, False)
        self._build_ui()
        self._center()

    def _center(self):
        """Centre la fenêtre sur l'écran."""
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 420) // 2
        y = (self.winfo_screenheight() - 530) // 2
        self.geometry(f"420x530+{x}+{y}")

    def _build_ui(self):
        # ── Titre avec design moderne ────────────────────────────────
        ctk.CTkLabel(self, text="DanProject",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=ThemeManager.get_color("accent_gold")).pack(pady=(50, 5))
        ctk.CTkLabel(self, text="Gestion Intelligente",
                     text_color="gray").pack(pady=(4, 25))

        # ── Formulaire ───────────────────────────────────────────────────────
        frame = ctk.CTkFrame(self, corner_radius=12)
        frame.pack(padx=35, fill="x")

        ctk.CTkLabel(frame, text="Nom d'utilisateur",
                     anchor="w").pack(anchor="w", padx=20, pady=(20, 2))
        self.entry_user = ctk.CTkEntry(frame, placeholder_text="admin",
                                       height=42, corner_radius=8)
        self.entry_user.pack(padx=20, fill="x")

        ctk.CTkLabel(frame, text="Mot de passe",
                     anchor="w").pack(anchor="w", padx=20, pady=(14, 2))
        self.entry_pwd = ctk.CTkEntry(frame, placeholder_text="••••••••",
                                      show="•", height=42, corner_radius=8)
        self.entry_pwd.pack(padx=20, fill="x")

        # Message d'erreur (caché par défaut)
        self.lbl_error = ctk.CTkLabel(frame, text="", text_color="#F59E0B",
                                      font=ctk.CTkFont(size=12))
        self.lbl_error.pack(pady=(8, 0))

        ctk.CTkButton(frame, text="Se connecter", height=44, corner_radius=8,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=ThemeManager.get_color("accent"),
                      hover_color=ThemeManager.get_color("accent_gold"),
                      command=self._login).pack(padx=20, pady=18, fill="x")

        # ── Note ─────────────────────────────────────────────────────────────
        ctk.CTkLabel(self, text="Compte par défaut : admin / admin123",
                     text_color="gray", font=ctk.CTkFont(size=11)).pack(pady=12)

        # Touche Entrée → connexion
        self.bind("<Return>", lambda _: self._login())
        self.entry_user.focus()

    def _login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pwd.get()

        if not username or not password:
            self.lbl_error.configure(text="⚠  Remplissez tous les champs")
            return

        if services.verify_login(username, password):
            self.destroy()
            from ui_main import MainWindow
            MainWindow().mainloop()
        else:
            self.lbl_error.configure(text="❌  Identifiants incorrects")
            self.entry_pwd.delete(0, "end")
            self.entry_pwd.focus()
