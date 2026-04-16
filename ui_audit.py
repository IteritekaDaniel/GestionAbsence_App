"""
ui_audit.py — Consultation des Journaux d'Audit
"""

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import services
import csv
from ui_students import _style_tree


class AuditView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self._build_ui()

    def _build_ui(self):
        # ── En-tête ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 8))

        ctk.CTkLabel(header, text="📋 Journaux d'Audit",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")

        ctk.CTkButton(header, text="📥  Export CSV", width=130, height=36,
                      command=self._export_csv).pack(side="right", padx=5)

        ctk.CTkButton(header, text="🔄  Rafraîchir", width=110, height=36,
                      command=self.refresh).pack(side="right", padx=5)

        # ── Filtres ──────────────────────────────────────────────────
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=15, pady=4)

        ctk.CTkLabel(bar, text="Table:").pack(side="left", padx=5)
        self.cmb_table = ctk.CTkComboBox(bar, values=["Toutes", "etudiants", "absences", "parents", 
                                                        "admins_extended", "absence_requests", 
                                                        "alert_notifications"],
                                         width=150, height=36,
                                         command=lambda _: self.refresh())
        self.cmb_table.set("Toutes")
        self.cmb_table.pack(side="left", padx=5)

        ctk.CTkLabel(bar, text="Limite:").pack(side="left", padx=5)
        self.cmb_limit = ctk.CTkComboBox(bar, values=["50", "100", "200", "500", "1000"],
                                         width=80, height=36,
                                         command=lambda _: self.refresh())
        self.cmb_limit.set("100")
        self.cmb_limit.pack(side="left", padx=5)

        self.lbl_count = ctk.CTkLabel(bar, text="", text_color="gray")
        self.lbl_count.pack(side="right")

        # ── Tableau ───────────────────────────────────────────────────
        tbl_frame = ctk.CTkFrame(self)
        tbl_frame.pack(fill="both", expand=True, padx=15, pady=8)

        _style_tree("Audit.Treeview")

        cols = ("Date/Heure", "Admin", "Action", "Table", "ID Record", "Détails")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
                                  style="Audit.Treeview", selectmode="browse")
        widths = {"Date/Heure": 150, "Admin": 100, "Action": 150, "Table": 100, 
                  "ID Record": 80, "Détails": 200}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths.get(col, 100), anchor="w")

        sb = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-Button-1>", lambda _: self._show_details())

        # ── Boutons ──────────────────────────────────────────────────
        act = ctk.CTkFrame(self, fg_color="transparent")
        act.pack(fill="x", padx=15, pady=(0, 12))

        self.btn_details = ctk.CTkButton(act, text="👁  Détails complets", width=150,
                                         state="disabled", command=self._show_details)
        self.btn_details.pack(side="left", padx=4)

        self.refresh()

    def refresh(self):
        """Recharge les logs."""
        self.tree.delete(*self.tree.get_children())

        table_filter = self.cmb_table.get()
        if table_filter == "Toutes":
            table_filter = None

        limit = int(self.cmb_limit.get())

        logs = services.get_audit_logs(limit=limit, table_name=table_filter)

        for log in logs:
            action_color = {
                "ADD": "🟢",
                "UPDATE": "🟡",
                "DELETE": "🔴",
                "LOGIN": "🔵",
            }
            
            icon = "🟢" if "ADD" in log.get("action", "") else (
                "🟡" if "UPDATE" in log.get("action", "") else (
                    "🔴" if "DELETE" in log.get("action", "") else "⚪"
                )
            )

            admin_name = log.get("admin_id", "System") if log.get("admin_id") else "System"

            self.tree.insert("", "end", iid=log["id"], values=(
                log["timestamp"],
                admin_name,
                f"{icon} {log.get('action', 'N/A')}",
                log.get("table_name", "N/A"),
                log.get("record_id", "—"),
                f"{'Old' if log.get('old_values') else 'New'}: {log.get('new_values', '')[:40]}"
            ))

        self.lbl_count.configure(text=f"{len(logs)} log(s)")

    def _on_select(self, event):
        """Sélection d'une ligne."""
        sel = self.tree.selection()
        self.btn_details.configure(state="normal" if sel else "disabled")

    def _show_details(self):
        """Affiche les détails complets d'un log."""
        sel = self.tree.selection()
        if not sel:
            return

        log_id = int(sel[0])
        logs = services.get_audit_logs(limit=10000)
        log = next((l for l in logs if l["id"] == log_id), None)

        if not log:
            messagebox.showerror("Erreur", "Log non trouvé")
            return

        win = ctk.CTkToplevel(self)
        win.title("Détails du log")
        win.geometry("700x500")

        # Info générale
        info_frame = ctk.CTkFrame(win, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(info_frame, text=f"ID: {log['id']}", text_color="gray").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Date/Heure: {log['timestamp']}", text_color="gray").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Admin: {log.get('admin_id', 'System')}", text_color="gray").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Action: {log.get('action', 'N/A')}", text_color="gray").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Table: {log.get('table_name', 'N/A')}", text_color="gray").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Record ID: {log.get('record_id', 'N/A')}", text_color="gray").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"IP: {log.get('ip_address', 'N/A')}", text_color="gray").pack(anchor="w")

        # Anciennes valeurs
        if log.get("old_values"):
            sep = ctk.CTkLabel(win, text="", height=2)
            sep.pack(fill="x", pady=5)

            ctk.CTkLabel(win, text="Anciennes valeurs:", 
                         font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15)
            txt_old = ctk.CTkTextbox(win, height=100)
            txt_old.insert("1.0", log.get("old_values", ""))
            txt_old.configure(state="disabled")
            txt_old.pack(padx=15, fill="both", expand=True, pady=5)

        # Nouvelles valeurs
        if log.get("new_values"):
            ctk.CTkLabel(win, text="Nouvelles valeurs:",
                         font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15)
            txt_new = ctk.CTkTextbox(win, height=100)
            txt_new.insert("1.0", log.get("new_values", ""))
            txt_new.configure(state="disabled")
            txt_new.pack(padx=15, fill="both", expand=True, pady=5)

    def _export_csv(self):
        """Exporte les logs en CSV."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if not filepath:
            return

        limit = int(self.cmb_limit.get())
        table_filter = self.cmb_table.get() if self.cmb_table.get() != "Toutes" else None
        logs = services.get_audit_logs(limit=limit, table_name=table_filter)

        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "admin_id", "action", "table_name",
                                                     "record_id", "old_values", "new_values", "ip_address"])
            writer.writeheader()
            for log in logs:
                writer.writerow({
                    "timestamp": log.get("timestamp", ""),
                    "admin_id": log.get("admin_id", ""),
                    "action": log.get("action", ""),
                    "table_name": log.get("table_name", ""),
                    "record_id": log.get("record_id", ""),
                    "old_values": log.get("old_values", ""),
                    "new_values": log.get("new_values", ""),
                    "ip_address": log.get("ip_address", "")
                })

        messagebox.showinfo("Succès", f"Logs exportés: {filepath}")
