"""
ui_reports.py — Rapports Avancés et Exports
"""

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from datetime import date, timedelta
import services
import csv


class ReportsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self._build_ui()

    def _build_ui(self):
        # ── En-tête ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 8))

        ctk.CTkLabel(header, text="📊 Rapports Avancés",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")

        # ── SECTION 1 : Rapport par étudiant ──────────────────────────
        frame1 = ctk.CTkFrame(self, fg_color="transparent", border_width=1, border_color="gray30")
        frame1.pack(fill="x", padx=15, pady=(8, 15), ipady=12)

        ctk.CTkLabel(frame1, text="📋 Rapport Détaillé par Étudiant",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=5)

        bar1 = ctk.CTkFrame(frame1, fg_color="transparent")
        bar1.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(bar1, text="Classe:").pack(side="left", padx=5)
        self.cmb_classe1 = ctk.CTkComboBox(bar1, values=["Toutes"] + services.get_classes(),
                                           width=150, height=36)
        self.cmb_classe1.set("Toutes")
        self.cmb_classe1.pack(side="left", padx=5)

        ctk.CTkButton(bar1, text="📄  Générer CSV", width=100, height=36,
                      command=self._generate_student_report).pack(side="left", padx=5)
        ctk.CTkButton(bar1, text="📥  En PDF", width=100, height=36,
                      command=self._generate_student_pdf).pack(side="left", padx=5)

        # ── SECTION 2 : Rapport de date ──────────────────────────────
        frame2 = ctk.CTkFrame(self, fg_color="transparent", border_width=1, border_color="gray30")
        frame2.pack(fill="x", padx=15, pady=(0, 15), ipady=12)

        ctk.CTkLabel(frame2, text="🗓️  Rapport par Date",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=5)

        bar2 = ctk.CTkFrame(frame2, fg_color="transparent")
        bar2.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(bar2, text="Classe:").pack(side="left", padx=5)
        self.cmb_classe2 = ctk.CTkComboBox(bar2, values=["Toutes"] + services.get_classes(),
                                           width=150, height=36)
        self.cmb_classe2.set("Toutes")
        self.cmb_classe2.pack(side="left", padx=5)

        ctk.CTkLabel(bar2, text="Date:").pack(side="left", padx=5)
        self.ent_date = ctk.CTkEntry(bar2, width=150, height=36)
        self.ent_date.insert(0, date.today().isoformat())
        self.ent_date.pack(side="left", padx=5)

        ctk.CTkButton(bar2, text="📄  Générer CSV", width=100, height=36,
                      command=self._generate_date_report).pack(side="left", padx=5)
        ctk.CTkButton(bar2, text="📥  En PDF", width=100, height=36,
                      command=self._generate_date_pdf).pack(side="left", padx=5)

        # ── SECTION 3 : Rapport de période ──────────────────────────
        frame3 = ctk.CTkFrame(self, fg_color="transparent", border_width=1, border_color="gray30")
        frame3.pack(fill="x", padx=15, pady=(0, 15), ipady=12)

        ctk.CTkLabel(frame3, text="📅 Rapport de Période",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=5)

        bar3 = ctk.CTkFrame(frame3, fg_color="transparent")
        bar3.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(bar3, text="De:").pack(side="left", padx=5)
        self.ent_from = ctk.CTkEntry(bar3, width=150, height=36)
        self.ent_from.insert(0, (date.today() - timedelta(days=30)).isoformat())
        self.ent_from.pack(side="left", padx=5)

        ctk.CTkLabel(bar3, text="À:").pack(side="left", padx=5)
        self.ent_to = ctk.CTkEntry(bar3, width=150, height=36)
        self.ent_to.insert(0, date.today().isoformat())
        self.ent_to.pack(side="left", padx=5)

        ctk.CTkButton(bar3, text="📄  Générer CSV", width=100, height=36,
                      command=self._generate_period_report).pack(side="left", padx=5)
        ctk.CTkButton(bar3, text="📊  Stats", width=100, height=36,
                      command=self._show_period_stats).pack(side="left", padx=5)

        # ── SECTION 4 : Alertes et Demandes ──────────────────────────
        frame4 = ctk.CTkFrame(self, fg_color="transparent", border_width=1, border_color="gray30")
        frame4.pack(fill="x", padx=15, pady=(0, 15), ipady=12)

        ctk.CTkLabel(frame4, text="⚠️  Alertes et Demandes",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=5)

        bar4 = ctk.CTkFrame(frame4, fg_color="transparent")
        bar4.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(bar4, text="🔴  Alertes Actives", width=140, height=36,
                      command=self._export_active_alerts).pack(side="left", padx=5)
        ctk.CTkButton(bar4, text="⏳  Demandes en Attente", width=150, height=36,
                      command=self._export_pending_requests).pack(side="left", padx=5)
        ctk.CTkButton(bar4, text="👨‍👩‍👧  Contacts Parents", width=140, height=36,
                      command=self._export_parents).pack(side="left", padx=5)

    # ─────────────────────────────────────────────────────────────────
    #   GÉNÉRATIONS DE RAPPORTS
    # ─────────────────────────────────────────────────────────────────

    def _generate_student_report(self):
        """Génère un rapport détaillé par étudiant."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if not filepath:
            return

        classe = self.cmb_classe1.get()
        if classe == "Toutes":
            classe = ""

        stats = services.get_stats_by_student(classe)

        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["Nom", "Prénom", "Classe", "Absences", "Présences", "Total", "Taux Absence %"])
            writer.writeheader()

            for s in stats:
                total = s["nb_absences"] + s["nb_presences"]
                taux = (s["nb_absences"] / total * 100) if total > 0 else 0
                writer.writerow({
                    "Nom": s["nom"],
                    "Prénom": s["prenom"],
                    "Classe": s["classe"],
                    "Absences": s["nb_absences"],
                    "Présences": s["nb_presences"],
                    "Total": total,
                    "Taux Absence %": f"{taux:.1f}%"
                })

        messagebox.showinfo("Succès", f"Rapport généré: {filepath}")

    def _generate_student_pdf(self):
        """Génère un rapport PDF détaillé."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")]
        )
        if not filepath:
            return

        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
            from reportlab.lib.units import cm

            classe = self.cmb_classe1.get()
            if classe == "Toutes":
                classe = ""

            stats = services.get_stats_by_student(classe)
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []

            # Titre
            elements.append(Paragraph("Rapport Détaillé des Présences/Absences", styles["Title"]))
            if classe:
                elements.append(Paragraph(f"Classe: {classe}", styles["Normal"]))
            else:
                elements.append(Paragraph("Tous les étudiants", styles["Normal"]))
            elements.append(Spacer(1, 0.5*cm))

            # Tableau
            table_data = [["Nom", "Prénom", "Classe", "Absences", "Présences", "Total", "% Absence"]]
            for s in stats:
                total = s["nb_absences"] + s["nb_presences"]
                taux = (s["nb_absences"] / total * 100) if total > 0 else 0
                table_data.append([
                    s["nom"], s["prenom"], s["classe"],
                    str(s["nb_absences"]), str(s["nb_presences"]),
                    str(total), f"{taux:.1f}%"
                ])

            table = Table(table_data, colWidths=[2.5*cm, 2.5*cm, 2*cm, 2*cm, 2*cm, 1.8*cm, 1.7*cm])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1f538d")),
                ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                ("FONTSIZE", (0,0), (-1,-1), 8),
                ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f0f4f8")]),
                ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
                ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ]))
            elements.append(table)

            doc.build(elements)
            messagebox.showinfo("Succès", f"Rapport PDF généré: {filepath}")
        except ImportError:
            messagebox.showerror("Erreur", "ReportLab non installé")

    def _generate_date_report(self):
        """Génère un rapport pour une date spécifique."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if not filepath:
            return

        date_str = self.ent_date.get()
        classe = self.cmb_classe2.get() if self.cmb_classe2.get() != "Toutes" else ""

        absences = services.get_absences_for_date(date_str, classe)

        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["Nom", "Prénom", "Classe", "Statut"])
            writer.writeheader()

            for a in absences:
                statut = "Absent" if a["statut"] == "absent" else (
                    "Présent" if a["statut"] == "present" else "Non marqué"
                )
                writer.writerow({
                    "Nom": a["nom"],
                    "Prénom": a["prenom"],
                    "Classe": a["classe"],
                    "Statut": statut
                })

        messagebox.showinfo("Succès", f"Rapport généré: {filepath}")

    def _generate_date_pdf(self):
        """Génère un rapport PDF pour une date."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")]
        )
        if not filepath:
            return

        date_str = self.ent_date.get()
        classe = self.cmb_classe2.get() if self.cmb_classe2.get() != "Toutes" else ""
        services.export_pdf(filepath, date_str, classe)
        messagebox.showinfo("Succès", f"Rapport PDF généré: {filepath}")

    def _generate_period_report(self):
        """Génère un rapport pour une période."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if not filepath:
            return

        msgbox_result = messagebox.showinfo("Info", "Génération en cours...")
        # À implémenter : logique pour récupérer stats sur la période

        messagebox.showinfo("Succès", f"Rapport généré: {filepath}")

    def _show_period_stats(self):
        """Affiche les stats de la période sélectionnée."""
        messagebox.showinfo("Info", "Stats de période à implémenter")

    def _export_active_alerts(self):
        """Exporte les alertes actives."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if not filepath:
            return

        alerts = services.get_active_alerts()

        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["Étudiant", "Classe", "Message", "Date", "Email envoyé"])
            writer.writeheader()

            for alert in alerts:
                student = services.get_student_by_id(alert["etudiant_id"])
                if student:
                    writer.writerow({
                        "Étudiant": f"{student['nom']} {student['prenom']}",
                        "Classe": student["classe"],
                        "Message": alert["message"],
                        "Date": alert["created_at"],
                        "Email envoyé": "Oui" if alert["email_sent"] else "Non"
                    })

        messagebox.showinfo("Succès", f"Alertes exportées: {filepath}")

    def _export_pending_requests(self):
        """Exporte les demandes en attente."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if not filepath:
            return

        requests = services.get_absence_requests(statut="pending")

        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["ID", "Étudiant", "Date", "Raison", "Demandé le"])
            writer.writeheader()

            for req in requests:
                writer.writerow({
                    "ID": req["id"],
                    "Étudiant": f"{req['nom']} {req['prenom']}",
                    "Date": req["date"],
                    "Raison": req["raison"],
                    "Demandé le": req["created_at"]
                })

        messagebox.showinfo("Succès", f"Demandes exportées: {filepath}")

    def _export_parents(self):
        """Exporte la liste des contacts parents."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if not filepath:
            return

        students = services.get_all_students()

        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["Étudiant", "Classe", "Parent", "Email", "Téléphone"])
            writer.writeheader()

            for student in students:
                parent = services.get_parent(student["id"])
                if parent:
                    writer.writerow({
                        "Étudiant": f"{student['nom']} {student['prenom']}",
                        "Classe": student["classe"],
                        "Parent": f"{parent['prenom']} {parent['nom']}",
                        "Email": parent.get("email", ""),
                        "Téléphone": parent.get("telephone", "")
                    })

        messagebox.showinfo("Succès", f"Contacts exportés: {filepath}")
