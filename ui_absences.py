"""
ui_absences.py — Vue "Gestion des Absences"
Permet de marquer présence/absence par date, avec sauvegarde groupée.
"""

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import services
from ui_students import _style_tree     # helper partagé


class AbsencesView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.current_date = date.today().isoformat()
        self._build_ui()

    # ─────────────────────────────────────────────────────────────────
    #   Construction
    # ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── En-tête + sélection de date ───────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 8))

        ctk.CTkLabel(header, text="📅 Gestion des Absences",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")

        # Sélection date (YYYY-MM-DD)
        date_frame = ctk.CTkFrame(header, fg_color="transparent")
        date_frame.pack(side="right")

        ctk.CTkLabel(date_frame, text="Date :").pack(side="left", padx=5)
        self.ent_date = ctk.CTkEntry(date_frame, width=120, height=36)
        self.ent_date.insert(0, self.current_date)
        self.ent_date.pack(side="left")
        ctk.CTkButton(date_frame, text="Charger", width=80, height=36,
                      command=self._load).pack(side="left", padx=5)

        # ── Filtre classe ─────────────────────────────────────────────
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=15, pady=4)

        ctk.CTkLabel(bar, text="Classe :").pack(side="left")
        self.cmb_classe = ctk.CTkComboBox(bar, width=130, height=36,
                                          command=lambda _: self._load())
        self.cmb_classe.pack(side="left", padx=5)

        self.lbl_status = ctk.CTkLabel(bar, text="", text_color="gray")
        self.lbl_status.pack(side="right")

        # ── Actions rapides ───────────────────────────────────────────
        acts = ctk.CTkFrame(self, fg_color="transparent")
        acts.pack(fill="x", padx=15, pady=4)

        ctk.CTkButton(acts, text="✅  Tous présents", width=145, height=34,
                      fg_color="#1a6b2a", hover_color="#155222",
                      command=lambda: self._mark_all("present")).pack(side="left", padx=4)
        ctk.CTkButton(acts, text="❌  Tous absents", width=145, height=34,
                      fg_color="#6b1a1a", hover_color="#521515",
                      command=lambda: self._mark_all("absent")).pack(side="left", padx=4)

        ctk.CTkButton(acts, text="📄  Export PDF", width=130, height=34,
                      command=self._export_pdf).pack(side="right", padx=4)
        ctk.CTkButton(acts, text="💾  Tout enregistrer", width=155, height=34,
                      command=self._save_all).pack(side="right", padx=4)

        # ── Tableau ───────────────────────────────────────────────────
        tbl_frame = ctk.CTkFrame(self)
        tbl_frame.pack(fill="both", expand=True, padx=15, pady=8)

        _style_tree("Abs.Treeview")

        cols = ("ID", "Nom", "Prénom", "Classe", "Statut", "Justification")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
                                  style="Abs.Treeview", selectmode="browse")
        widths = {"ID": 50, "Nom": 155, "Prénom": 155,
                  "Classe": 110, "Statut": 130, "Justification": 220}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor="center")

        sb = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Double-clic → modifier le statut
        self.tree.bind("<Double-Button-1>", self._on_dbl_click)

        # ── Légende ───────────────────────────────────────────────────
        ctk.CTkLabel(self,
                     text="🟢 Présent   🔴 Absent   ⬜ Non marqué   |   Double-clic pour modifier",
                     text_color="gray", font=ctk.CTkFont(size=11)).pack(
            anchor="w", padx=20, pady=(0, 10)
        )

    # ─────────────────────────────────────────────────────────────────
    #   Données
    # ─────────────────────────────────────────────────────────────────

    def refresh(self):
        """Appelé à chaque fois qu'on revient sur l'onglet."""
        classes = ["Toutes"] + services.get_classes()
        cur = self.cmb_classe.get()
        self.cmb_classe.configure(values=classes)
        if cur not in classes:
            self.cmb_classe.set("Toutes")
        self._load()

    def _load(self):
        """Charge les étudiants pour la date saisie."""
        date_str = self.ent_date.get().strip()

        # Valider le format de date
        import re
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            messagebox.showerror("Erreur", "Format de date invalide.\nUtilisez YYYY-MM-DD")
            return

        self.current_date = date_str
        classe = self.cmb_classe.get()
        if classe in ("Toutes", ""):
            classe = ""

        rows = services.get_absences_for_date(date_str, classe)
        self._populate_table(rows)

    def _populate_table(self, rows: list[dict]):
        """Remplit le tableau avec les données."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        nb_pres = nb_abs = 0
        for row in rows:
            statut = row["statut"]
            if statut == "present":
                display = "🟢 Présent"
                tag = "present"
                nb_pres += 1
            elif statut == "absent":
                display = "🔴 Absent"
                tag = "absent"
                nb_abs += 1
            else:
                display = "⬜ Non marqué"
                tag = "unmarked"

            self.tree.insert("", "end", iid=str(row["id"]),
                             values=(row["id"], row["nom"], row["prenom"],
                                     row["classe"], display, row["justification"]),
                             tags=(tag,))

        self.tree.tag_configure("present",  foreground="#90ee90")
        self.tree.tag_configure("absent",   foreground="#ff9090")
        self.tree.tag_configure("unmarked", foreground="#888888")

        total = len(rows)
        self.lbl_status.configure(
            text=f"{total} étudiant(s)  |  🟢 {nb_pres}  🔴 {nb_abs}"
        )

    # ─────────────────────────────────────────────────────────────────
    #   Modification d'une ligne
    # ─────────────────────────────────────────────────────────────────

    def _on_dbl_click(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        vals = self.tree.item(iid)["values"]
        nom_complet = f"{vals[1]} {vals[2]}"
        cur_statut  = "present" if "Présent" in str(vals[4]) else "absent"
        cur_just    = str(vals[5]) if vals[5] else ""

        AbsenceEditDialog(
            self,
            etudiant_id=int(iid),
            nom=nom_complet,
            cur_statut=cur_statut,
            cur_just=cur_just,
            on_save=self._update_row,
        )

    def _update_row(self, etudiant_id: int, statut: str, just: str):
        """Met à jour visuellement une ligne (sans encore écrire en BDD)."""
        iid = str(etudiant_id)
        vals = list(self.tree.item(iid)["values"])

        if statut == "present":
            vals[4] = "🟢 Présent"
            tag = "present"
        else:
            vals[4] = "🔴 Absent"
            tag = "absent"
        vals[5] = just

        self.tree.item(iid, values=vals, tags=(tag,))
        self.tree.tag_configure("present", foreground="#90ee90")
        self.tree.tag_configure("absent",  foreground="#ff9090")

    def _mark_all(self, statut: str):
        """Marque tous les étudiants visibles avec le même statut."""
        for iid in self.tree.get_children():
            self._update_row(int(iid), statut, "")

    # ─────────────────────────────────────────────────────────────────
    #   Sauvegarde
    # ─────────────────────────────────────────────────────────────────

    def _save_all(self):
        """Enregistre en BDD tous les statuts visibles dans le tableau."""
        saved = 0
        for iid in self.tree.get_children():
            vals = self.tree.item(iid)["values"]
            statut_disp = str(vals[4])
            if "Présent" in statut_disp:
                statut = "present"
            elif "Absent" in statut_disp:
                statut = "absent"
            else:
                continue   # "Non marqué" = pas de sauvegarde
            just = str(vals[5]) if vals[5] else ""
            services.mark_absence(int(iid), self.current_date, statut, just)
            saved += 1

        messagebox.showinfo("Succès", f"✅ {saved} enregistrement(s) sauvegardé(s) !")
        self._load()    # recharger pour confirmer

    # ─────────────────────────────────────────────────────────────────
    #   Export PDF
    # ─────────────────────────────────────────────────────────────────

    def _export_pdf(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            title="Exporter en PDF"
        )
        if not path:
            return

        classe = self.cmb_classe.get()
        if classe in ("Toutes", ""):
            classe = ""

        ok = services.export_pdf(path, self.current_date, classe)
        if ok:
            messagebox.showinfo("Export réussi", f"✅ PDF créé :\n{path}")
        else:
            messagebox.showwarning(
                "reportlab manquant",
                "Installez reportlab pour activer l'export PDF :\n\n  pip install reportlab"
            )


# ─────────────────────────────────────────────────────────────────────────────
#   Dialogue de modification d'un statut
# ─────────────────────────────────────────────────────────────────────────────

class AbsenceEditDialog(ctk.CTkToplevel):
    def __init__(self, parent, etudiant_id, nom, cur_statut, cur_just, on_save):
        super().__init__(parent)
        self.title("Modifier le statut")
        self.geometry("380x290")
        self.resizable(False, False)
        self.grab_set()
        self.etudiant_id = etudiant_id
        self.on_save = on_save
        self._build(nom, cur_statut, cur_just)
        self._center()

    def _center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 380) // 2
        y = (self.winfo_screenheight() - 290) // 2
        self.geometry(f"380x290+{x}+{y}")

    def _build(self, nom, cur_statut, cur_just):
        ctk.CTkLabel(self, text=f"Étudiant : {nom}",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(22, 14))

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=4)

        ctk.CTkLabel(frame, text="Statut", anchor="w").pack(anchor="w", padx=15, pady=(12, 6))

        self.var_statut = ctk.StringVar(value=cur_statut)
        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(anchor="w", padx=15)
        ctk.CTkRadioButton(row, text="🟢  Présent",
                           variable=self.var_statut, value="present").pack(side="left", padx=10)
        ctk.CTkRadioButton(row, text="🔴  Absent",
                           variable=self.var_statut, value="absent").pack(side="left", padx=10)

        ctk.CTkLabel(frame, text="Justification (optionnel)",
                     anchor="w").pack(anchor="w", padx=15, pady=(14, 4))
        self.ent_just = ctk.CTkEntry(frame, height=38)
        self.ent_just.pack(fill="x", padx=15, pady=(0, 14))
        if cur_just:
            self.ent_just.insert(0, cur_just)

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(pady=10)
        ctk.CTkButton(btns, text="Annuler",   width=100,
                      fg_color="gray30", command=self.destroy).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Confirmer", width=110,
                      command=self._confirm).pack(side="left", padx=5)

        self.bind("<Return>", lambda _: self._confirm())

    def _confirm(self):
        self.on_save(self.etudiant_id, self.var_statut.get(), self.ent_just.get().strip())
        self.destroy()
