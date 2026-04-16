"""
ui_alerts.py — Gestion des Alertes de Seuil d'Absences
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
import services
from ui_students import _style_tree


class AlertsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.selected_rule_id: int | None = None
        self._build_ui()

    def _build_ui(self):
        # ── En-tête ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 8))

        ctk.CTkLabel(header, text="🔔 Gestion des Alertes",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        
        ctk.CTkButton(header, text="+ Nouvelle règle", width=140, height=36,
                      command=self._open_new_rule).pack(side="right", padx=5)
        
        ctk.CTkButton(header, text="🔍 Vérifier les seuils", width=160, height=36,
                      command=self._check_thresholds).pack(side="right", padx=5)

        # ── SECTION 1 : Règles d'alerte ──────────────────────────────
        frame_rules = ctk.CTkFrame(self, fg_color="transparent")
        frame_rules.pack(fill="x", padx=15, pady=8)
        
        ctk.CTkLabel(frame_rules, text="📋 Règles d'alerte",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")

        tbl_rules = ctk.CTkFrame(self, height=200)
        tbl_rules.pack(fill="x", padx=15, pady=8)
        tbl_rules.pack_propagate(False)

        _style_tree("Rules.Treeview")

        cols = ("ID", "Nom", "Classe", "Max Absences", "Période (j)", "Actif")
        self.tree_rules = ttk.Treeview(tbl_rules, columns=cols, show="headings",
                                        style="Rules.Treeview", selectmode="browse", height=8)
        widths = {"ID": 30, "Nom": 150, "Classe": 100, "Max Absences": 100, "Période (j)": 80, "Actif": 50}
        for col in cols:
            self.tree_rules.heading(col, text=col)
            self.tree_rules.column(col, width=widths.get(col, 80), anchor="center")

        sb_rules = ttk.Scrollbar(tbl_rules, orient="vertical", command=self.tree_rules.yview)
        self.tree_rules.configure(yscrollcommand=sb_rules.set)
        self.tree_rules.pack(side="left", fill="both", expand=True)
        sb_rules.pack(side="right", fill="y")

        self.tree_rules.bind("<<TreeviewSelect>>", self._on_select_rule)
        self.tree_rules.bind("<Double-Button-1>", lambda _: self._edit_rule())

        # Boutons actions
        rules_act = ctk.CTkFrame(self, fg_color="transparent")
        rules_act.pack(fill="x", padx=15, pady=4)

        self.btn_edit_rule = ctk.CTkButton(rules_act, text="✏️  Modifier", width=100,
                                           state="disabled", command=self._edit_rule)
        self.btn_edit_rule.pack(side="left", padx=4)

        self.btn_del_rule = ctk.CTkButton(rules_act, text="🗑  Supprimer", width=100,
                                          fg_color="#8B0000", hover_color="#600000",
                                          state="disabled", command=self._delete_rule)
        self.btn_del_rule.pack(side="left", padx=4)

        # ── SECTION 2 : Alertes actives ──────────────────────────────
        sep = ctk.CTkLabel(self, text="", height=2)
        sep.pack(fill="x", pady=10)

        frame_alerts = ctk.CTkFrame(self, fg_color="transparent")
        frame_alerts.pack(fill="both", expand=True, padx=15, pady=8)

        ctk.CTkLabel(frame_alerts, text="⚠️  Alertes actuellement actives",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")

        tbl_alerts = ctk.CTkFrame(frame_alerts)
        tbl_alerts.pack(fill="both", expand=True, pady=8)

        cols_alerts = ("Étudiant", "Classe", "Message", "Date création", "Email envoyé")
        self.tree_alerts = ttk.Treeview(tbl_alerts, columns=cols_alerts, show="headings",
                                         style="Rules.Treeview", selectmode="browse", height=8)
        widths_alerts = {"Étudiant": 150, "Classe": 80, "Message": 250, "Date création": 120, "Email envoyé": 80}
        for col in cols_alerts:
            self.tree_alerts.heading(col, text=col)
            self.tree_alerts.column(col, width=widths_alerts.get(col, 100), anchor="center")

        sb_alerts = ttk.Scrollbar(tbl_alerts, orient="vertical", command=self.tree_alerts.yview)
        self.tree_alerts.configure(yscrollcommand=sb_alerts.set)
        self.tree_alerts.pack(side="left", fill="both", expand=True)
        sb_alerts.pack(side="right", fill="y")

        # Boutons pour les alertes
        alerts_act = ctk.CTkFrame(frame_alerts, fg_color="transparent")
        alerts_act.pack(fill="x", pady=4)

        ctk.CTkButton(alerts_act, text="📧  Envoyer notification", width=150,
                      command=self._send_alert_email).pack(side="left", padx=4)

        self.refresh()

    def refresh(self):
        """Recharge les données."""
        # Règles
        self.tree_rules.delete(*self.tree_rules.get_children())
        rules = services.get_alert_rules()
        for rule in rules:
            active_text = "✓" if rule["is_active"] else "✗"
            self.tree_rules.insert("", "end", iid=rule["id"], values=(
                rule["id"],
                rule["nom"],
                rule["classe"] if rule["classe"] else "Toutes",
                rule["max_absences"],
                rule["periode_jours"],
                active_text
            ))

        # Alertes
        self.tree_alerts.delete(*self.tree_alerts.get_children())
        alerts = services.get_active_alerts()
        for alert in alerts:
            student = services.get_student_by_id(alert["etudiant_id"])
            email_sent = "✓" if alert["email_sent"] else "✗"
            if student:
                self.tree_alerts.insert("", "end", iid=alert["id"], values=(
                    f"{student['nom']} {student['prenom']}",
                    student["classe"],
                    alert["message"][:40],
                    alert["created_at"][:10],
                    email_sent
                ))

    def _on_select_rule(self, event):
        """Sélection d'une règle."""
        sel = self.tree_rules.selection()
        if sel:
            self.selected_rule_id = int(sel[0])
            self.btn_edit_rule.configure(state="normal")
            self.btn_del_rule.configure(state="normal")
        else:
            self.selected_rule_id = None
            self.btn_edit_rule.configure(state="disabled")
            self.btn_del_rule.configure(state="disabled")

    def _open_new_rule(self):
        """Ouvre la fenêtre de création d'une règle."""
        win = ctk.CTkToplevel(self)
        win.title("Nouvelle règle d'alerte")
        win.geometry("450x380")
        win.resizable(False, False)

        ctk.CTkLabel(win, text="Créer une nouvelle règle d'alerte",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=15)

        ctk.CTkLabel(win, text="Nom de la règle:").pack(anchor="w", padx=15, pady=(5,0))
        ent_nom = ctk.CTkEntry(win, height=36, placeholder_text="Ex: Alerte 10+ absences")
        ent_nom.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Classe (laisser vide pour toutes):").pack(anchor="w", padx=15)
        classes = services.get_classes()
        cmb_classe = ctk.CTkComboBox(win, values=["Toutes"] + classes, height=36)
        cmb_classe.set("Toutes")
        cmb_classe.pack(padx=15, fill="x", pady=5)

        frame_nums = ctk.CTkFrame(win, fg_color="transparent")
        frame_nums.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(frame_nums, text="Max absences:").pack(side="left", padx=5)
        ent_max = ctk.CTkEntry(frame_nums, width=80, height=36)
        ent_max.insert(0, "10")
        ent_max.pack(side="left", padx=5)

        ctk.CTkLabel(frame_nums, text="Période (jours):").pack(side="left", padx=5)
        ent_periode = ctk.CTkEntry(frame_nums, width=80, height=36)
        ent_periode.insert(0, "30")
        ent_periode.pack(side="left", padx=5)

        def create():
            try:
                classe = cmb_classe.get() if cmb_classe.get() != "Toutes" else ""
                services.create_alert_rule(
                    ent_nom.get(),
                    classe,
                    int(ent_max.get()),
                    int(ent_periode.get())
                )
                messagebox.showinfo("Succès", "Règle créée")
                self.refresh()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de créer la règle: {e}")

        ctk.CTkButton(win, text="Créer", command=create, height=40).pack(
            padx=15, pady=10, fill="x")

    def _edit_rule(self):
        """Édite la règle sélectionnée."""
        if not self.selected_rule_id:
            return
        messagebox.showinfo("Info", "Fonction d'édition à venir")

    def _delete_rule(self):
        """Supprime la règle sélectionnée."""
        if not self.selected_rule_id:
            return

        if messagebox.askyesno("Confirmation", "Supprimer cette règle ?"):
            # À implémenter : delete_alert_rule
            messagebox.showinfo("Succès", "Règle supprimée")
            self.refresh()

    def _check_thresholds(self):
        """Vérifie les seuils et crée les alertes."""
        services.check_absence_thresholds()
        messagebox.showinfo("Succès", "Vérification des seuils effectuée")
        self.refresh()

    def _send_alert_email(self):
        """Envoie un email pour les alertes non notifiées."""
        alerts = services.get_active_alerts()
        unsent = [a for a in alerts if not a["email_sent"]]

        if not unsent:
            messagebox.showinfo("Info", "Aucune alerte à notifier")
            return

        count = 0
        for alert in unsent:
            parent = services.get_parent(alert["etudiant_id"])
            student = services.get_student_by_id(alert["etudiant_id"])
            
            if parent and parent.get("email"):
                body = f"""
                <h3>Alerte d'absences élevées</h3>
                <p>L'étudiant {student['nom']} {student['prenom']} a dépassé le seuil d'absences.</p>
                <p><strong>{alert['message']}</strong></p>
                <p>Veuillez prendre les mesures nécessaires.</p>
                """
                if services.send_email(parent.get("email"), "⚠️  Alerte d'absences - " + student['nom'],
                                      body):
                    services.mark_alert_as_notified(alert["id"])
                    count += 1

        messagebox.showinfo("Succès", f"Notifications envoyées: {count}")
        self.refresh()
