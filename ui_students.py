"""
ui_students.py — Vue "Gestion des Étudiants" (CRUD complet)
"""

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import services


class StudentsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.selected_id: int | None = None
        self._build_ui()

    # ─────────────────────────────────────────────────────────────────
    #   Construction de l'interface
    # ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── En-tête ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 8))

        ctk.CTkLabel(header, text="👥 Gestion des Étudiants",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="+ Ajouter", width=120, height=36,
                      command=self._open_add).pack(side="right")

        # ── Barre recherche / filtre ──────────────────────────────────
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=15, pady=4)

        self.var_search = ctk.StringVar()
        self.var_search.trace("w", lambda *_: self.refresh())
        ctk.CTkEntry(bar, placeholder_text="🔍 Rechercher (nom ou prénom)…",
                     textvariable=self.var_search,
                     height=38, width=280).pack(side="left")

        ctk.CTkLabel(bar, text="Classe :").pack(side="left", padx=(18, 4))
        self.cmb_classe = ctk.CTkComboBox(bar, width=130, height=38,
                                          command=lambda _: self.refresh())
        self.cmb_classe.pack(side="left")

        ctk.CTkButton(bar, text="↺  Réinitialiser", width=130, height=38,
                      fg_color="gray30", command=self._reset_filters).pack(side="left", padx=6)

        self.lbl_count = ctk.CTkLabel(bar, text="", text_color="gray")
        self.lbl_count.pack(side="right")

        # ── Tableau ───────────────────────────────────────────────────
        tbl_frame = ctk.CTkFrame(self)
        tbl_frame.pack(fill="both", expand=True, padx=15, pady=8)

        _style_tree("Student.Treeview")

        cols = ("ID", "Nom", "Prénom", "Classe", "Email", "Absences")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
                                  style="Student.Treeview", selectmode="browse")
        widths = {"ID": 50, "Nom": 160, "Prénom": 160,
                  "Classe": 110, "Email": 210, "Absences": 80}
        for col in cols:
            self.tree.heading(col, text=col,
                              command=lambda c=col: self._sort_by(c))
            self.tree.column(col, width=widths[col], anchor="center")

        sb = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-Button-1>",  lambda _: self._open_edit())

        # ── Boutons d'action ──────────────────────────────────────────
        act = ctk.CTkFrame(self, fg_color="transparent")
        act.pack(fill="x", padx=15, pady=(0, 12))

        self.btn_edit = ctk.CTkButton(act, text="✏️  Modifier",   width=120,
                                       state="disabled", command=self._open_edit)
        self.btn_edit.pack(side="left", padx=4)

        self.btn_del = ctk.CTkButton(act, text="🗑  Supprimer",  width=120,
                                      fg_color="#8B0000", hover_color="#600000",
                                      state="disabled", command=self._delete)
        self.btn_del.pack(side="left", padx=4)

        ctk.CTkButton(act, text="📥  Export CSV", width=140,
                      command=self._export_csv).pack(side="right", padx=4)

    # ─────────────────────────────────────────────────────────────────
    #   Données
    # ─────────────────────────────────────────────────────────────────

    def refresh(self):
        """Recharge la liste selon les filtres en cours."""
        search = self.var_search.get()
        classe = self.cmb_classe.get()
        if classe in ("Toutes", ""):
            classe = ""

        # Mettre à jour le combobox des classes
        all_classes = ["Toutes"] + services.get_classes()
        current = self.cmb_classe.get()
        self.cmb_classe.configure(values=all_classes)
        if current not in all_classes:
            self.cmb_classe.set("Toutes")

        # Nombre d'absences par étudiant (pour affichage)
        absences_map = {s["id"]: s["nb_absences"]
                        for s in services.get_stats_by_student()}

        students = services.get_all_students(search, classe)

        # Vider + remplir le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)

        for s in students:
            nb_abs = absences_map.get(s["id"], 0)
            tag = "alert" if nb_abs >= 3 else ""   # rouge si ≥ 3 absences
            self.tree.insert("", "end", iid=str(s["id"]),
                             values=(s["id"], s["nom"], s["prenom"],
                                     s["classe"], s["email"], nb_abs),
                             tags=(tag,))

        self.tree.tag_configure("alert", foreground="#ff9090")
        self.lbl_count.configure(text=f"{len(students)} étudiant(s)")

        # Désactiver les boutons si rien de sélectionné
        self.selected_id = None
        self.btn_edit.configure(state="disabled")
        self.btn_del.configure(state="disabled")

    # ─────────────────────────────────────────────────────────────────
    #   Événements
    # ─────────────────────────────────────────────────────────────────

    def _on_select(self, _event):
        sel = self.tree.selection()
        if sel:
            self.selected_id = int(sel[0])
            self.btn_edit.configure(state="normal")
            self.btn_del.configure(state="normal")

    def _reset_filters(self):
        self.var_search.set("")
        self.cmb_classe.set("Toutes")
        self.refresh()

    def _sort_by(self, col):
        """Tri du tableau au clic sur l'en-tête de colonne."""
        col_map = {"ID": 0, "Nom": 1, "Prénom": 2, "Classe": 3, "Email": 4, "Absences": 5}
        idx = col_map.get(col, 1)
        data = [(self.tree.set(c, col), c) for c in self.tree.get_children("")]
        data.sort(key=lambda t: (t[0].isdigit(), int(t[0]) if t[0].isdigit() else t[0].lower()))
        for i, (_, iid) in enumerate(data):
            self.tree.move(iid, "", i)

    # ─────────────────────────────────────────────────────────────────
    #   CRUD
    # ─────────────────────────────────────────────────────────────────

    def _open_add(self):
        StudentDialog(self, title="Ajouter un étudiant",
                      on_save=lambda d: (services.add_student(**d), self.refresh()))

    def _open_edit(self):
        if not self.selected_id:
            return
        student = services.get_student_by_id(self.selected_id)
        if student:
            StudentDialog(
                self, title="Modifier l'étudiant", prefill=student,
                on_save=lambda d: (
                    services.update_student(self.selected_id, **d), self.refresh()
                )
            )

    def _delete(self):
        if not self.selected_id:
            return
        s = services.get_student_by_id(self.selected_id)
        name = f"{s['prenom']} {s['nom']}" if s else "cet étudiant"
        if messagebox.askyesno(
            "Confirmation",
            f"Supprimer {name} ainsi que toutes ses absences ?",
            icon="warning"
        ):
            services.delete_student(self.selected_id)
            self.refresh()

    def _export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Fichier CSV", "*.csv")],
            title="Exporter en CSV"
        )
        if path:
            services.export_csv(path)
            messagebox.showinfo("Export réussi", f"✅ Fichier enregistré :\n{path}")


# ─────────────────────────────────────────────────────────────────────────────
#   Dialogue Ajouter / Modifier
# ─────────────────────────────────────────────────────────────────────────────

class StudentDialog(ctk.CTkToplevel):
    """Fenêtre modale pour créer ou modifier un étudiant."""

    def __init__(self, parent, title: str, on_save, prefill: dict = None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x400")
        self.resizable(False, False)
        self.grab_set()       # bloque la fenêtre principale
        self.on_save = on_save
        self._build(prefill)
        self._center()

    def _center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 400) // 2
        y = (self.winfo_screenheight() - 400) // 2
        self.geometry(f"400x400+{x}+{y}")

    def _build(self, prefill):
        ctk.CTkLabel(self, text=self.title(),
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(22, 12))

        form = ctk.CTkFrame(self)
        form.pack(fill="both", expand=True, padx=22, pady=4)

        fields = [("Nom *", "nom"), ("Prénom *", "prenom"),
                  ("Classe *", "classe"), ("Email", "email")]
        self.entries: dict[str, ctk.CTkEntry] = {}

        for label, key in fields:
            ctk.CTkLabel(form, text=label, anchor="w").pack(anchor="w", padx=14, pady=(10, 2))
            entry = ctk.CTkEntry(form, height=38)
            entry.pack(fill="x", padx=14)
            if prefill and prefill.get(key):
                entry.insert(0, prefill[key])
            self.entries[key] = entry

        self.lbl_err = ctk.CTkLabel(self, text="", text_color="#ff6b6b")
        self.lbl_err.pack(pady=6)

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(pady=(0, 14))
        ctk.CTkButton(btns, text="Annuler",      width=105,
                      fg_color="gray30", command=self.destroy).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Enregistrer",  width=120,
                      command=self._save).pack(side="left", padx=5)

        self.bind("<Return>", lambda _: self._save())

    def _save(self):
        data = {k: e.get().strip() for k, e in self.entries.items()}
        if not data["nom"] or not data["prenom"] or not data["classe"]:
            self.lbl_err.configure(text="⚠  Nom, Prénom et Classe sont obligatoires")
            return
        self.on_save(data)
        self.destroy()


# ─────────────────────────────────────────────────────────────────────────────
#   Helper partagé de style Treeview
# ─────────────────────────────────────────────────────────────────────────────

def _style_tree(name: str):
    """Configure le style sombre d'un Treeview."""
    s = ttk.Style()
    s.theme_use("clam")
    s.configure(name,
                background="#2b2b2b", foreground="white",
                fieldbackground="#2b2b2b", rowheight=30,
                font=("Arial", 11))
    s.configure(f"{name}.Heading",
                background="#1f538d", foreground="white",
                font=("Arial", 11, "bold"))
    s.map(name, background=[("selected", "#1f538d")])
