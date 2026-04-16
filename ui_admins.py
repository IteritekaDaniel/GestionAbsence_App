"""
ui_admins.py — Gestion des Administrateurs Multi-rôles
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
import services
from ui_students import _style_tree


class AdminsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.selected_id: int | None = None
        self._build_ui()

    def _build_ui(self):
        # ── En-tête ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 8))

        ctk.CTkLabel(header, text="🔐 Gestion des Administrateurs",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")

        ctk.CTkButton(header, text="+ Ajouter Admin", width=140, height=36,
                      command=self._open_add).pack(side="right")

        # ── Tableau ───────────────────────────────────────────────────
        tbl_frame = ctk.CTkFrame(self)
        tbl_frame.pack(fill="both", expand=True, padx=15, pady=8)

        _style_tree("Admin.Treeview")

        cols = ("ID", "Utilisateur", "Email", "Rôle", "Dernière connexion", "2FA")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
                                  style="Admin.Treeview", selectmode="browse")
        widths = {"ID": 40, "Utilisateur": 130, "Email": 180, "Rôle": 100, 
                  "Dernière connexion": 160, "2FA": 45}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor="center")

        sb = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-Button-1>", lambda _: self._open_edit())

        # ── Boutons d'action ──────────────────────────────────────
        act = ctk.CTkFrame(self, fg_color="transparent")
        act.pack(fill="x", padx=15, pady=(0, 12))

        self.btn_edit = ctk.CTkButton(act, text="✏️  Modifier", width=120,
                                       state="disabled", command=self._open_edit)
        self.btn_edit.pack(side="left", padx=4)

        self.btn_del = ctk.CTkButton(act, text="🗑  Supprimer", width=120,
                                      fg_color="#8B0000", hover_color="#600000",
                                      state="disabled", command=self._delete)
        self.btn_del.pack(side="left", padx=4)

        self.btn_2fa = ctk.CTkButton(act, text="🔑  Gérer 2FA", width=120,
                                      state="disabled", command=self._manage_2fa)
        self.btn_2fa.pack(side="left", padx=4)

        self.btn_pwd = ctk.CTkButton(act, text="🔐  Réinitialiser MDP", width=160,
                                      state="disabled", command=self._reset_password)
        self.btn_pwd.pack(side="left", padx=4)

        self.refresh()

    def refresh(self):
        """Recharge la liste des admins."""
        self.tree.delete(*self.tree.get_children())
        
        admins = services.get_all_admins()
        
        for admin in admins:
            role_display = {
                "admin": "👑 Admin",
                "editor": "✏️  Éditeur",
                "viewer": "👁  Lecteur"
            }.get(admin["role"], admin["role"])

            two_fa_display = "✓" if admin["is_2fa_enabled"] else "✗"
            
            self.tree.insert("", "end", iid=admin["id"], values=(
                admin["id"],
                admin["username"],
                admin["email"],
                role_display,
                admin.get("last_login", "Jan jamais")[:10] if admin.get("last_login") else "Jamais",
                two_fa_display
            ))

    def _on_select(self, event):
        """Sélection d'une ligne."""
        sel = self.tree.selection()
        if sel:
            self.selected_id = int(sel[0])
            self.btn_edit.configure(state="normal")
            self.btn_del.configure(state="normal")
            self.btn_2fa.configure(state="normal")
            self.btn_pwd.configure(state="normal")
        else:
            self.selected_id = None
            self.btn_edit.configure(state="disabled")
            self.btn_del.configure(state="disabled")
            self.btn_2fa.configure(state="disabled")
            self.btn_pwd.configure(state="disabled")

    def _open_add(self):
        """Ouvre la fenêtre d'ajout."""
        win = ctk.CTkToplevel(self)
        win.title("Ajouter un administrateur")
        win.geometry("450x450")
        win.resizable(False, False)

        ctk.CTkLabel(win, text="Nouvel Administrateur",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=15)

        ctk.CTkLabel(win, text="Nom d'utilisateur:").pack(anchor="w", padx=15, pady=(5,0))
        ent_user = ctk.CTkEntry(win, height=36)
        ent_user.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Email:").pack(anchor="w", padx=15)
        ent_email = ctk.CTkEntry(win, height=36)
        ent_email.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Mot de passe:").pack(anchor="w", padx=15)
        ent_pwd = ctk.CTkEntry(win, height=36, show="•")
        ent_pwd.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Confirmer le mot de passe:").pack(anchor="w", padx=15)
        ent_pwd2 = ctk.CTkEntry(win, height=36, show="•")
        ent_pwd2.pack(padx=15, fill="x", pady=5)

        # Vérification de force du mot de passe
        def check_pwd(*args):
            pwd = ent_pwd.get()
            validation = services.validate_password_strength(pwd)
            color = "#28A745" if validation["valid"] else "#FFA500"
            if pwd:
                lbl_strength.configure(
                    text=f"Force: {validation['score']}/5 - {', '.join(validation['errors']) if validation['errors'] else '✓ Bon'}",
                    text_color=color
                )
            else:
                lbl_strength.configure(text="")

        ent_pwd.bind("<KeyRelease>", check_pwd)

        lbl_strength = ctk.CTkLabel(win, text="", text_color="gray", font=ctk.CTkFont(size=10))
        lbl_strength.pack(anchor="w", padx=15)

        ctk.CTkLabel(win, text="Rôle:").pack(anchor="w", padx=15, pady=(10,0))
        cmb_role = ctk.CTkComboBox(win, values=["admin", "editor", "viewer"], height=36)
        cmb_role.set("viewer")
        cmb_role.pack(padx=15, fill="x", pady=5)

        def save():
            if not ent_user.get() or not ent_pwd.get():
                messagebox.showerror("Erreur", "Remplissez tous les champs")
                return

            if ent_pwd.get() != ent_pwd2.get():
                messagebox.showerror("Erreur", "Les mot de passe ne correspondent pas")
                return

            validation = services.validate_password_strength(ent_pwd.get())
            if not validation["valid"]:
                messagebox.showerror("Erreur", "Mot de passe trop faible: " + ", ".join(validation["errors"]))
                return

            try:
                services.add_admin(ent_user.get(), ent_pwd.get(), ent_email.get(), cmb_role.get())
                messagebox.showinfo("Succès", "Admin ajouté")
                self.refresh()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        ctk.CTkButton(win, text="Ajouter", command=save, height=40).pack(
            padx=15, pady=10, fill="x")

    def _open_edit(self):
        """Ouvre la fenêtre de modification."""
        if not self.selected_id:
            return

        admins = services.get_all_admins()
        admin = next((a for a in admins if a["id"] == self.selected_id), None)

        if not admin:
            return

        win = ctk.CTkToplevel(self)
        win.title("Modifier administrateur")
        win.geometry("450x350")
        win.resizable(False, False)

        ctk.CTkLabel(win, text=f"Modifier: {admin['username']}",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)

        ctk.CTkLabel(win, text="Email:").pack(anchor="w", padx=15, pady=(5,0))
        ent_email = ctk.CTkEntry(win, height=36)
        ent_email.insert(0, admin.get("email", ""))
        ent_email.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Rôle:").pack(anchor="w", padx=15)
        cmb_role = ctk.CTkComboBox(win, values=["admin", "editor", "viewer"], height=36)
        cmb_role.set(admin["role"])
        cmb_role.pack(padx=15, fill="x", pady=5)

        def save():
            services.update_admin_role(self.selected_id, cmb_role.get())
            messagebox.showinfo("Succès", "Admin modifié")
            self.refresh()
            win.destroy()

        ctk.CTkButton(win, text="Enregistrer", command=save, height=40).pack(
            padx=15, pady=10, fill="x")

    def _delete(self):
        """Supprime l'admin sélectionné."""
        if not self.selected_id:
            return

        if self.selected_id == 1:
            messagebox.showerror("Erreur", "Impossible de supprimer l'admin principal")
            return

        if messagebox.askyesno("Confirmation", "Supprimer cet admin ?"):
            services.delete_admin(self.selected_id)
            services.log_action(action="DELETE_ADMIN", table_name="admins_extended", record_id=self.selected_id)
            messagebox.showinfo("Succès", "Admin supprimé")
            self.refresh()

    def _manage_2fa(self):
        """Gère 2FA pour l'admin."""
        if not self.selected_id:
            return

        admins = services.get_all_admins()
        admin = next((a for a in admins if a["id"] == self.selected_id), None)

        if not admin:
            return

        if admin["is_2fa_enabled"]:
            if messagebox.askyesno("Confirmation", "Désactiver 2FA pour cet admin ?"):
                services.disable_2fa(self.selected_id)
                messagebox.showinfo("Succès", "2FA désactivé")
                self.refresh()
        else:
            win = ctk.CTkToplevel(self)
            win.title("Activer 2FA")
            win.geometry("500x600")

            ctk.CTkLabel(win, text="Activation de l'Authentification à Deux Facteurs",
                         font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)

            ctk.CTkLabel(win, text="Une clé secrète et des codes de secours vont être générés.",
                         text_color="gray").pack(pady=5)

            result = services.enable_2fa(self.selected_id)

            ctk.CTkLabel(win, text="Clé secrète (pour Google Authenticator):",
                         font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(10,0))
            
            txt_key = ctk.CTkTextbox(win, height=40)
            txt_key.insert("1.0", result["secret_key"])
            txt_key.configure(state="disabled")
            txt_key.pack(padx=15, fill="x", pady=5)

            ctk.CTkLabel(win, text="Codes de secours (gardez-les en lieu sûr):",
                         font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(10,0))
            
            txt_codes = ctk.CTkTextbox(win, height=150)
            txt_codes.insert("1.0", "\n".join(result["backup_codes"]))
            txt_codes.configure(state="disabled")
            txt_codes.pack(padx=15, fill="x", pady=5)

            ctk.CTkLabel(win, text="⚠️  Conservez ces codes dans un endroit sûr.",
                         text_color="#FFA500", font=ctk.CTkFont(size=10)).pack(pady=5)

            ctk.CTkButton(win, text="Fermer", command=win.destroy, height=40).pack(
                padx=15, pady=10, fill="x")

            self.refresh()

    def _reset_password(self):
        """Réinitialise le mot de passe d'un admin."""
        if not self.selected_id:
            return

        win = ctk.CTkToplevel(self)
        win.title("Réinitialiser le mot de passe")
        win.geometry("450x300")

        ctk.CTkLabel(win, text="Nouveau mot de passe:",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)

        ent_pwd = ctk.CTkEntry(win, height=36, show="•")
        ent_pwd.pack(padx=15, fill="x", pady=5)

        ent_pwd2 = ctk.CTkEntry(win, height=36, show="•")
        ent_pwd2.pack(padx=15, fill="x", pady=5)

        def change():
            if not ent_pwd.get():
                messagebox.showerror("Erreur", "Entrez un mot de passe")
                return

            if ent_pwd.get() != ent_pwd2.get():
                messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
                return

            validation = services.validate_password_strength(ent_pwd.get())
            if not validation["valid"]:
                messagebox.showerror("Erreur", "Mot de passe trop faible")
                return

            services.update_admin_password(self.selected_id, ent_pwd.get())
            services.log_action(action="RESET_ADMIN_PASSWORD", table_name="admins_extended", record_id=self.selected_id)
            messagebox.showinfo("Succès", "Mot de passe réinitialisé")
            win.destroy()

        ctk.CTkButton(win, text="Réinitialiser", command=change, height=40).pack(
            padx=15, pady=10, fill="x")
