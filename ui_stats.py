"""
ui_stats.py — Vue "Statistiques"
Affiche KPIs, graphiques matplotlib et tableau détaillé.
"""

import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import services
from ui_students import _style_tree

# Couleurs matplotlib adaptées au thème sombre
BG     = "#2b2b2b"
BLUE   = "#1f538d"
GREEN  = "#1a6b2a"
RED    = "#8B0000"
GRID   = "#3a3a3a"
WHITE  = "#dddddd"


class StatsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self._build_ui()

    # ─────────────────────────────────────────────────────────────────
    #   Construction
    # ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        ctk.CTkLabel(self, text="📊 Statistiques",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(
            anchor="w", padx=15, pady=(15, 10)
        )

        # ── Cartes KPI ────────────────────────────────────────────────
        kpi_row = ctk.CTkFrame(self, fg_color="transparent")
        kpi_row.pack(fill="x", padx=15, pady=6)

        self._kpi_cards: dict[str, ctk.CTkLabel] = {}
        for key, label, color in [
            ("nb_etudiants",      "👥 Étudiants",       "#1f538d"),
            ("nb_absences_total", "❌ Absences totales", "#8B0000"),
            ("nb_classes",        "🏫 Classes",          "#1a6b2a"),
            ("moyenne_absences",  "📈 Moy. absences",    "#6b4a00"),
        ]:
            card = ctk.CTkFrame(kpi_row, corner_radius=10,
                                border_width=1, border_color=color)
            card.pack(side="left", padx=6, expand=True, fill="x")
            ctk.CTkLabel(card, text=label, text_color="gray",
                         font=ctk.CTkFont(size=11)).pack(pady=(10, 2))
            val_lbl = ctk.CTkLabel(card, text="—",
                                   font=ctk.CTkFont(size=26, weight="bold"),
                                   text_color=color)
            val_lbl.pack(pady=(0, 10))
            self._kpi_cards[key] = val_lbl

        # ── Onglets ───────────────────────────────────────────────────
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=15, pady=10)

        self.tabs.add("Top absents")
        self.tabs.add("Par mois")
        self.tabs.add("Tableau complet")

        self._build_tab_top()
        self._build_tab_month()
        self._build_tab_table()

    # ── Onglet 1 : Top absents ────────────────────────────────────────

    def _build_tab_top(self):
        tab = self.tabs.tab("Top absents")
        self._fig_top = Figure(figsize=(5, 3.5), dpi=90, facecolor=BG)
        self._ax_top  = self._fig_top.add_subplot(111, facecolor=BG)
        self._fig_top.subplots_adjust(left=0.22, right=0.98, top=0.88, bottom=0.12)
        canvas = FigureCanvasTkAgg(self._fig_top, master=tab)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self._canvas_top = canvas

    # ── Onglet 2 : Par mois ───────────────────────────────────────────

    def _build_tab_month(self):
        tab = self.tabs.tab("Par mois")

        ctrl = ctk.CTkFrame(tab, fg_color="transparent")
        ctrl.pack(fill="x", padx=10, pady=6)
        ctk.CTkLabel(ctrl, text="Année :").pack(side="left")
        self._ent_year = ctk.CTkEntry(ctrl, width=80, height=32)
        self._ent_year.insert(0, str(datetime.now().year))
        self._ent_year.pack(side="left", padx=5)
        ctk.CTkButton(ctrl, text="Actualiser", width=100, height=32,
                      command=self._draw_month_chart).pack(side="left")

        self._fig_month = Figure(figsize=(5, 3), dpi=90, facecolor=BG)
        self._ax_month  = self._fig_month.add_subplot(111, facecolor=BG)
        self._fig_month.subplots_adjust(left=0.1, right=0.98, top=0.88, bottom=0.18)
        canvas = FigureCanvasTkAgg(self._fig_month, master=tab)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10)
        self._canvas_month = canvas

    # ── Onglet 3 : Tableau ────────────────────────────────────────────

    def _build_tab_table(self):
        tab = self.tabs.tab("Tableau complet")
        _style_tree("Stats.Treeview")

        cols = ("Rang", "Nom", "Prénom", "Classe", "Absences", "Présences")
        self._tbl = ttk.Treeview(tab, columns=cols, show="headings",
                                  style="Stats.Treeview")
        widths = {"Rang": 60, "Nom": 155, "Prénom": 155,
                  "Classe": 110, "Absences": 100, "Présences": 100}
        for col in cols:
            self._tbl.heading(col, text=col)
            self._tbl.column(col, width=widths[col], anchor="center")

        sb = ttk.Scrollbar(tab, orient="vertical", command=self._tbl.yview)
        self._tbl.configure(yscrollcommand=sb.set)
        self._tbl.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    # ─────────────────────────────────────────────────────────────────
    #   Rafraîchissement
    # ─────────────────────────────────────────────────────────────────

    def refresh(self):
        # KPIs
        stats = services.get_global_stats()
        self._kpi_cards["nb_etudiants"].configure(text=str(stats["nb_etudiants"]))
        self._kpi_cards["nb_absences_total"].configure(text=str(stats["nb_absences_total"]))
        self._kpi_cards["nb_classes"].configure(text=str(stats["nb_classes"]))
        self._kpi_cards["moyenne_absences"].configure(text=str(stats["moyenne_absences"]))

        # Top 10 absents → graphique horizontal
        data = services.get_stats_by_student()[:10]
        self._draw_top_chart(data)

        # Tableau
        for item in self._tbl.get_children():
            self._tbl.delete(item)
        for i, d in enumerate(services.get_stats_by_student(), 1):
            tag = "alert" if d["nb_absences"] >= 3 else ""
            self._tbl.insert("", "end", tags=(tag,),
                             values=(i, d["nom"], d["prenom"], d["classe"],
                                     d["nb_absences"], d["nb_presences"]))
        self._tbl.tag_configure("alert", foreground="#ff9090")

        # Graphique par mois
        self._draw_month_chart()

    # ─────────────────────────────────────────────────────────────────
    #   Graphiques matplotlib
    # ─────────────────────────────────────────────────────────────────

    def _draw_top_chart(self, data: list[dict]):
        ax = self._ax_top
        ax.clear()
        ax.set_facecolor(BG)

        if data:
            # Inverser pour afficher le plus absent en haut
            names  = [f"{d['prenom'][0]}. {d['nom']}" for d in data][::-1]
            values = [d["nb_absences"] for d in data][::-1]

            bars = ax.barh(names, values, color=BLUE, edgecolor="#4a8ad4", height=0.65)

            # Afficher les valeurs à droite des barres
            for bar, val in zip(bars, values):
                if val > 0:
                    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                            str(val), va="center", ha="left",
                            color=WHITE, fontsize=9)

            ax.set_title("Top 10 — Étudiants les Plus Absents",
                         color=WHITE, fontsize=11, pad=10)
            ax.tick_params(colors=WHITE, labelsize=9)
            ax.set_xlabel("Nombre d'absences", color=WHITE, fontsize=9)
        else:
            ax.text(0.5, 0.5, "Aucune donnée disponible",
                    ha="center", va="center", color="gray",
                    transform=ax.transAxes, fontsize=12)

        _style_ax(ax)
        self._canvas_top.draw()

    def _draw_month_chart(self):
        try:
            year = int(self._ent_year.get())
        except (ValueError, AttributeError):
            year = datetime.now().year

        rows = services.get_absences_by_month(year)
        months = ["Jan","Fév","Mar","Avr","Mai","Juin",
                  "Jul","Aoû","Sep","Oct","Nov","Déc"]
        counts = [0] * 12
        for r in rows:
            counts[int(r["mois"]) - 1] = r["total"]

        ax = self._ax_month
        ax.clear()
        ax.set_facecolor(BG)

        x = range(12)
        bars = ax.bar(x, counts, color=GREEN, edgecolor="#2a9b3a", width=0.6)

        # Valeurs au-dessus des barres
        for bar, val in zip(bars, counts):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        str(val), ha="center", va="bottom",
                        color=WHITE, fontsize=9)

        ax.set_xticks(x)
        ax.set_xticklabels(months, color=WHITE, fontsize=9)
        ax.set_title(f"Absences par mois — {year}",
                     color=WHITE, fontsize=11, pad=10)
        _style_ax(ax)
        self._canvas_month.draw()


# ─────────────────────────────────────────────────────────────────────────────
#   Helper : style commun des axes matplotlib
# ─────────────────────────────────────────────────────────────────────────────

def _style_ax(ax):
    ax.tick_params(colors=WHITE)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.yaxis.label.set_color(WHITE)
