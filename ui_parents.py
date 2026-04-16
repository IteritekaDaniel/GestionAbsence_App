"""
ui_parents.py — Gestion des Parents/Tuteurs
"""

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import services
from ui_students import _style_tree


class ParentsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.selected_id: int | None = None
        self._build_ui()

    def _build_ui(self):
        # ── En-tête ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 8))

        ctk.CTkLabel(header, text="👨‍👩‍👧 Gestion des Parents",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="+ Ajouter", width=120, height=36,
                      command=self._open_add).pack(side="right")

        # ── Barre recherche ────────────────────────────────────────
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=15, pady=4)

        self.var_search = ctk.StringVar()
        self.var_search.trace("w", lambda *_: self.refresh())
        ctk.CTkEntry(bar, placeholder_text="🔍 Rechercher étudiant…",
                     textvariable=self.var_search,
                     height=38, width=300).pack(side="left")

        self.lbl_count = ctk.CTkLabel(bar, text="", text_color="gray")
        self.lbl_count.pack(side="right")

        # ── Tableau ───────────────────────────────────────────────────
        tbl_frame = ctk.CTkFrame(self)
        tbl_frame.pack(fill="both", expand=True, padx=15, pady=8)

        _style_tree("Parent.Treeview")

        cols = ("ID Étudiant", "Étudiant", "Parent", "Email", "Téléphone", "Relation")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
                                  style="Parent.Treeview", selectmode="browse")
        widths = {"ID Étudiant": 80, "Étudiant": 120, "Parent": 140,
                  "Email": 180, "Téléphone": 110, "Relation": 90}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths.get(col, 100), anchor="center")

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

        ctk.CTkButton(act, text="📧  Notifier", width=120,
                      command=self._notify_parent).pack(side="left", padx=4)

        ctk.CTkButton(act, text="📥  Export CSV", width=140,
                      command=self._export_csv).pack(side="right", padx=4)

        self.refresh()

    def refresh(self):
        """Recharge la liste des parents."""
        self.tree.delete(*self.tree.get_children())
        search = self.var_search.get()
        
        all_students = services.get_all_students()
        count = 0
        
        for student in all_students:
            if search.lower() not in (student["nom"] + " " + student["prenom"]).lower():
                continue
            
            parent = services.get_parent(student["id"])
            if parent:
                parent_nom = f"{parent['prenom']} {parent['nom']}"
                self.tree.insert("", "end", iid=student["id"], values=(
                    student["id"],
                    f"{student['nom']} {student['prenom']}",
                    parent_nom,
                    parent.get("email", ""),
                    parent.get("telephone", ""),
                    parent.get("relation", "")
                ))
                count += 1
        
        self.lbl_count.configure(text=f"{count} parent(s)")

    def _on_select(self, event):
        """Sélection d'une ligne."""
        sel = self.tree.selection()
        if sel:
            self.selected_id = int(sel[0])
            self.btn_edit.configure(state="normal")
            self.btn_del.configure(state="normal")
        else:
            self.selected_id = None
            self.btn_edit.configure(state="disabled")
            self.btn_del.configure(state="disabled")

    def _open_add(self):
        """Ouvre la fenêtre d'ajout/sélection d'étudiant."""
        win = ctk.CTkToplevel(self)
        win.title("Ajouter un parent")
        win.geometry("450x400")
        win.resizable(False, False)

        ctk.CTkLabel(win, text="Sélectionner un étudiant",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)

        # Combobox d'étudiants
        students = services.get_all_students()
        student_names = [f"{s['nom']} {s['prenom']} ({s['classe']})" for s in students]
        
        ctk.CTkLabel(win, text="Étudiant:").pack(anchor="w", padx=15)
        cmb_student = ctk.CTkComboBox(win, values=student_names, width=400, height=36)
        cmb_student.pack(padx=15, pady=5)

        # Champs parent
        ctk.CTkLabel(win, text="Nom du parent:").pack(anchor="w", padx=15, pady=(15,0))
        ent_nom = ctk.CTkEntry(win, height=36)
        ent_nom.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Prénom du parent:").pack(anchor="w", padx=15)
        ent_prenom = ctk.CTkEntry(win, height=36)
        ent_prenom.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Email:").pack(anchor="w", padx=15)
        ent_email = ctk.CTkEntry(win, height=36)
        ent_email.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Téléphone:").pack(anchor="w", padx=15)
        ent_tel = ctk.CTkEntry(win, height=36)
        ent_tel.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Relation:").pack(anchor="w", padx=15)
        cmb_relation = ctk.CTkComboBox(win, values=["parent", "tuteur", "autre"], height=36)
        cmb_relation.set("parent")
        cmb_relation.pack(padx=15, fill="x", pady=5)

        def save():
            if not cmb_student.get() or not ent_nom.get() or not ent_prenom.get():
                messagebox.showerror("Erreur", "Remplissez les champs obligatoires")
                return
            
            student_idx = student_names.index(cmb_student.get())
            student_id = students[student_idx]["id"]
            
            # Vérifier si parent existe déjà
            existing = services.get_parent(student_id)
            if existing:
                services.update_parent(student_id, ent_nom.get(), ent_prenom.get(),
                                      ent_email.get(), ent_tel.get(), cmb_relation.get())
            else:
                services.add_parent(student_id, ent_nom.get(), ent_prenom.get(),
                                   ent_email.get(), ent_tel.get(), cmb_relation.get())
            
            services.log_action(action="ADD_PARENT", table_name="parents", record_id=student_id)
            messagebox.showinfo("Succès", "Parent ajouté/modifié")
            self.refresh()
            win.destroy()

        ctk.CTkButton(win, text="Enregistrer", command=save, height=40).pack(
            padx=15, pady=15, fill="x")

    def _open_edit(self):
        """Ouvre la fenêtre de modification."""
        if not self.selected_id:
            return

        parent = services.get_parent(self.selected_id)
        student = services.get_student_by_id(self.selected_id)

        if not parent:
            messagebox.showwarning("Attention", "Aucun parent enregistré pour cet étudiant")
            return

        win = ctk.CTkToplevel(self)
        win.title("Modifier parent")
        win.geometry("450x350")
        win.resizable(False, False)

        ctk.CTkLabel(win, text=f"Parent de {student['nom']} {student['prenom']}",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)

        ctk.CTkLabel(win, text="Nom:").pack(anchor="w", padx=15, pady=(10,0))
        ent_nom = ctk.CTkEntry(win, height=36)
        ent_nom.insert(0, parent["nom"])
        ent_nom.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Prénom:").pack(anchor="w", padx=15)
        ent_prenom = ctk.CTkEntry(win, height=36)
        ent_prenom.insert(0, parent["prenom"])
        ent_prenom.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Email:").pack(anchor="w", padx=15)
        ent_email = ctk.CTkEntry(win, height=36)
        ent_email.insert(0, parent.get("email", ""))
        ent_email.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Téléphone:").pack(anchor="w", padx=15)
        ent_tel = ctk.CTkEntry(win, height=36)
        ent_tel.insert(0, parent.get("telephone", ""))
        ent_tel.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Relation:").pack(anchor="w", padx=15)
        cmb_relation = ctk.CTkComboBox(win, values=["parent", "tuteur", "autre"], height=36)
        cmb_relation.set(parent.get("relation", "parent"))
        cmb_relation.pack(padx=15, fill="x", pady=5)

        def save():
            services.update_parent(self.selected_id, ent_nom.get(), ent_prenom.get(),
                                  ent_email.get(), ent_tel.get(), cmb_relation.get())
            services.log_action(action="UPDATE_PARENT", table_name="parents", record_id=self.selected_id)
            messagebox.showinfo("Succès", "Parent modifié")
            self.refresh()
            win.destroy()

        ctk.CTkButton(win, text="Enregistrer", command=save, height=40).pack(
            padx=15, pady=10, fill="x")

    def _delete(self):
        """Supprime un parent."""
        if not self.selected_id:
            return

        if messagebox.askyesno("Confirmation", "Supprimer ce parent ?"):
            services.delete_parent(self.selected_id)
            services.log_action(action="DELETE_PARENT", table_name="parents", record_id=self.selected_id)
            messagebox.showinfo("Succès", "Parent supprimé")
            self.refresh()

    def _notify_parent(self):
        """Envoie une notification au parent."""
        if not self.selected_id:
            return

        parent = services.get_parent(self.selected_id)
        student = services.get_student_by_id(self.selected_id)

        if not parent or not parent.get("email"):
            messagebox.showerror("Erreur", "Pas d'email pour ce parent")
            return

        # Créer une fenêtre pour rédiger l'email
        win = ctk.CTkToplevel(self)
        win.title("Envoyer une notification")
        win.geometry("500x400")

        ctk.CTkLabel(win, text=f"À: {parent['email']}", text_color="gray").pack(pady=5)

        ctk.CTkLabel(win, text="Objet:").pack(anchor="w", padx=15, pady=(5,0))
        ent_subject = ctk.CTkEntry(win, height=36)
        ent_subject.insert(0, f"Notification d'absence - {student['nom']}")
        ent_subject.pack(padx=15, fill="x", pady=5)

        ctk.CTkLabel(win, text="Message:").pack(anchor="w", padx=15)
        txt_body = ctk.CTkTextbox(win, height=200)
        txt_body.pack(padx=15, fill="both", expand=True, pady=5)

        def send():
            if services.send_email(parent.get("email"), ent_subject.get(), txt_body.get("1.0", "end")):
                messagebox.showinfo("Succès", "Email envoyé")
                win.destroy()
            else:
                messagebox.showerror("Erreur", "Impossible d'envoyer l'email")

        ctk.CTkButton(win, text="Envoyer", command=send, height=40).pack(
            padx=15, pady=10, fill="x")

    def _export_csv(self):
        """Exporte la liste en CSV."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if not filepath:
            return

        import csv
        students = services.get_all_students()
        
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["ID Étudiant", "Étudiant", "Classe", "Parent", "Email", "Téléphone", "Relation"])
            
            for student in students:
                parent = services.get_parent(student["id"])
                if parent:
                    writer.writerow([
                        student["id"],
                        f"{student['nom']} {student['prenom']}",
                        student["classe"],
                        f"{parent['prenom']} {parent['nom']}",
                        parent.get("email", ""),
                        parent.get("telephone", ""),
                        parent.get("relation", "")
                    ])
        
        messagebox.showinfo("Succès", f"Fichier exporté: {filepath}")
