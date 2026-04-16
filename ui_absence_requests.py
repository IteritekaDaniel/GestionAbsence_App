"""
ui_absence_requests.py — Gestion des Demandes de Validation d'Absence
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import date
import services
from ui_students import _style_tree


class AbsenceRequestsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.selected_id: int | None = None
        self._build_ui()

    def _build_ui(self):
        # ── En-tête ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 8))

        ctk.CTkLabel(header, text="📋 Demandes de Validation d'Absence",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")

        # ── Filtres ──────────────────────────────────────────────────
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=15, pady=4)

        ctk.CTkLabel(bar, text="Statut:").pack(side="left")
        self.cmb_statut = ctk.CTkComboBox(bar, values=["Toutes", "pending", "approved", "rejected"],
                                          width=130, height=36,
                                          command=lambda _: self.refresh())
        self.cmb_statut.set("pending")
        self.cmb_statut.pack(side="left", padx=5)

        self.lbl_count = ctk.CTkLabel(bar, text="", text_color="gray")
        self.lbl_count.pack(side="right")

        # ── Tableau ───────────────────────────────────────────────────
        tbl_frame = ctk.CTkFrame(self)
        tbl_frame.pack(fill="both", expand=True, padx=15, pady=8)

        _style_tree("Request.Treeview")

        cols = ("ID", "Étudiant", "Date", "Raison", "Statut", "Demandé le")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
                                  style="Request.Treeview", selectmode="browse")
        widths = {"ID": 40, "Étudiant": 150, "Date": 100, "Raison": 200, 
                  "Statut": 100, "Demandé le": 130}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths.get(col, 100), anchor="center")

        sb = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-Button-1>", lambda _: self._view_details())

        # ── Boutons d'action ──────────────────────────────────────
        act = ctk.CTkFrame(self, fg_color="transparent")
        act.pack(fill="x", padx=15, pady=(0, 12))

        self.btn_approve = ctk.CTkButton(act, text="✅  Approuver", width=120,
                                         fg_color="#1a6b2a", hover_color="#155222",
                                         state="disabled", command=self._approve)
        self.btn_approve.pack(side="left", padx=4)

        self.btn_reject = ctk.CTkButton(act, text="❌  Rejeter", width=120,
                                        fg_color="#6b1a1a", hover_color="#521515",
                                        state="disabled", command=self._reject)
        self.btn_reject.pack(side="left", padx=4)

        self.btn_details = ctk.CTkButton(act, text="👁  Détails", width=120,
                                         state="disabled", command=self._view_details)
        self.btn_details.pack(side="left", padx=4)

        self.refresh()

    def refresh(self):
        """Recharge la liste des demandes."""
        self.tree.delete(*self.tree.get_children())
        
        statut_filter = self.cmb_statut.get()
        if statut_filter == "Toutes":
            statut_filter = None

        requests = services.get_absence_requests(statut=statut_filter)
        
        for req in requests:
            statut_display = {
                "pending": "🟡 En attente",
                "approved": "🟢 Approuvé",
                "rejected": "🔴 Rejeté"
            }.get(req["statut"], req["statut"])

            self.tree.insert("", "end", iid=req["id"], values=(
                req["id"],
                f"{req['nom']} {req['prenom']}",
                req["date"],
                req["raison"][:40],
                statut_display,
                req["created_at"][:10]
            ))
        
        self.lbl_count.configure(text=f"{len(requests)} demande(s)")

    def _on_select(self, event):
        """Sélection d'une ligne."""
        sel = self.tree.selection()
        if sel:
            self.selected_id = int(sel[0])
            self.btn_approve.configure(state="normal")
            self.btn_reject.configure(state="normal")
            self.btn_details.configure(state="normal")
        else:
            self.selected_id = None
            self.btn_approve.configure(state="disabled")
            self.btn_reject.configure(state="disabled")
            self.btn_details.configure(state="disabled")

    def _view_details(self):
        """Affiche les détails d'une demande."""
        if not self.selected_id:
            return

        requests = services.get_absence_requests()
        req = next((r for r in requests if r["id"] == self.selected_id), None)

        if not req:
            messagebox.showerror("Erreur", "Demande non trouvée")
            return

        win = ctk.CTkToplevel(self)
        win.title("Détails de la demande")
        win.geometry("600x500")

        # Infos basiques
        ctk.CTkLabel(win, text=f"Étudiant: {req['nom']} {req['prenom']}",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)

        frame = ctk.CTkFrame(win, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(frame, text=f"Date: {req['date']}", text_color="gray").pack(anchor="w")
        ctk.CTkLabel(frame, text=f"Raison: {req['raison']}", text_color="gray").pack(anchor="w", pady=2)
        ctk.CTkLabel(frame, text=f"Demandé le: {req['created_at']}", text_color="gray").pack(anchor="w")

        if req.get("reviewed_at"):
            ctk.CTkLabel(frame, text=f"Examiné le: {req.get('reviewed_at', '')}", 
                         text_color="gray").pack(anchor="w", pady=2)

        # Documents (si uploadés)
        if req.get("documents"):
            ctk.CTkLabel(win, text="Documents:", font=ctk.CTkFont(size=12, weight="bold")).pack(
                anchor="w", padx=15, pady=(10, 5))
            for doc in req["documents"].split(","):
                if doc.strip():
                    ctk.CTkLabel(win, text=f"📄 {doc.strip()}", text_color="gray").pack(
                        anchor="w", padx=30)

        # Statut
        statut_colors = {
            "pending": ("#FFA500", "En attente d'examen"),
            "approved": ("#28A745", "Approuvée"),
            "rejected": ("#DC3545", "Rejetée")
        }
        color, status_text = statut_colors.get(req["statut"], ("gray", req["statut"]))
        ctk.CTkLabel(win, text=f"Statut: {status_text}", text_color=color,
                     font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)

        # Boutons d'action (si en attente)
        if req["statut"] == "pending":
            actions = ctk.CTkFrame(win, fg_color="transparent")
            actions.pack(fill="x", padx=15, pady=10)

            ctk.CTkButton(actions, text="✅ Approuver et Marquer Présent", height=36,
                         fg_color="#1a6b2a", hover_color="#155222",
                         command=lambda: self._do_approve(True, win)).pack(side="left", padx=5, fill="x", expand=True)

            ctk.CTkButton(actions, text="❌ Rejeter", height=36,
                         fg_color="#6b1a1a", hover_color="#521515",
                         command=lambda: self._do_reject(win)).pack(side="left", padx=5, fill="x", expand=True)

    def _approve(self):
        """Approuve la demande sélectionnée."""
        if not self.selected_id:
            return

        if messagebox.askyesno("Confirmation", "Approuver cette demande ?\nL'étudiant sera marqué présent."):
            services.approve_request(self.selected_id, admin_id=1, mark_as_present=True)
            services.log_action(action="APPROVE_ABSENCE_REQUEST", table_name="absence_requests", 
                              record_id=self.selected_id)
            messagebox.showinfo("Succès", "Demande approuvée")
            self.refresh()

    def _do_approve(self, mark_present: bool, win):
        """Approuve depuis la fenêtre de détails."""
        services.approve_request(self.selected_id, admin_id=1, mark_as_present=mark_present)
        services.log_action(action="APPROVE_ABSENCE_REQUEST", table_name="absence_requests",
                          record_id=self.selected_id)
        messagebox.showinfo("Succès", "Demande approuvée")
        self.refresh()
        win.destroy()

    def _reject(self):
        """Rejette la demande sélectionnée."""
        if not self.selected_id:
            return

        if messagebox.askyesno("Confirmation", "Rejeter cette demande ?"):
            services.reject_request(self.selected_id, admin_id=1)
            services.log_action(action="REJECT_ABSENCE_REQUEST", table_name="absence_requests",
                              record_id=self.selected_id)
            messagebox.showinfo("Succès", "Demande rejetée")
            self.refresh()

    def _do_reject(self, win):
        """Rejette depuis la fenêtre de détails."""
        services.reject_request(self.selected_id, admin_id=1)
        services.log_action(action="REJECT_ABSENCE_REQUEST", table_name="absence_requests",
                          record_id=self.selected_id)
        messagebox.showinfo("Succès", "Demande rejetée")
        self.refresh()
        win.destroy()


class AbsenceRequestDialog(ctk.CTkToplevel):
    """Fenêtre pour créer une demande d'absence par l'étudiant."""
    
    def __init__(self, parent, etudiant_id: int):
        super().__init__(parent)
        self.title("Demander une validation d'absence")
        self.geometry("450x400")
        self.resizable(False, False)
        self.etudiant_id = etudiant_id
        self.result = None
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Demande de Validation d'Absence",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=15)

        ctk.CTkLabel(self, text="Date de l'absence:").pack(anchor="w", padx=15, pady=(5,0))
        self.ent_date = ctk.CTkEntry(self, height=36, placeholder_text="YYYY-MM-DD")
        self.ent_date.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(self, text="Raison:").pack(anchor="w", padx=15, pady=(10,0))
        self.txt_raison = ctk.CTkTextbox(self, height=150)
        self.txt_raison.pack(padx=15, fill="both", expand=True, pady=5)

        ctk.CTkLabel(self, text="Documents (optionnel):", text_color="gray",
                     font=ctk.CTkFont(size=10)).pack(anchor="w", padx=15)
        self.ent_docs = ctk.CTkEntry(self, height=36, placeholder_text="Nom du fichier ou URL")
        self.ent_docs.pack(padx=15, fill="x", pady=5)

        def submit():
            raison = self.txt_raison.get("1.0", "end").strip()
            date_val = self.ent_date.get().strip()

            if not raison or not date_val:
                messagebox.showerror("Erreur", "Remplissez tous les champs")
                return

            try:
                services.create_absence_request(
                    self.etudiant_id,
                    date_val,
                    raison,
                    self.ent_docs.get().strip()
                )
                messagebox.showinfo("Succès", "Demande envoyée aux responsables")
                self.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de créer la demande: {e}")

        ctk.CTkButton(self, text="Envoyer la demande", command=submit, height=40).pack(
            padx=15, pady=10, fill="x")
