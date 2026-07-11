
"""
calendar_widget.py — Calendrier interactif des absences
"""

import customtkinter as ctk
from tkinter import ttk
from datetime import datetime, timedelta
from database import get_conn
from theme import ThemeManager

class CalendarWidget(ctk.CTkFrame):
    """Widget calendrier pour visualiser les absences"""
    
    def __init__(self, parent, on_date_select=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_date_select = on_date_select
        self.current_date = datetime.now()
        self._build_ui()
    
    def _build_ui(self):
        """Construit le calendrier"""
        # En-tête avec navigation
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(header, text="◀", width=40, height=35,
                     command=self._prev_month).pack(side="left", padx=5)
        
        self.month_label = ctk.CTkLabel(header, text="", font=("Arial", 14, "bold"))
        self.month_label.pack(side="left", expand=True)
        
        ctk.CTkButton(header, text="▶", width=40, height=35,
                     command=self._next_month).pack(side="left", padx=5)
        
        # Grille du calendrier
        calendar_frame = ctk.CTkFrame(self)
        calendar_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Jours de la semaine
        days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        for i, day in enumerate(days):
            lbl = ctk.CTkLabel(calendar_frame, text=day, font=("Arial", 10, "bold"),
                              text_color=ThemeManager.get_color("accent"))
            lbl.grid(row=0, column=i, padx=5, pady=5)
        
        # Dates du mois
        self._draw_calendar(calendar_frame)
    
    def _draw_calendar(self, frame):
        """Dessine les dates du mois"""
        # Effacer les dates existantes
        for widget in frame.winfo_children()[7:]:
            widget.destroy()
        
        year = self.current_date.year
        month = self.current_date.month
        
        # Titre
        self.month_label.configure(text=self.current_date.strftime("%B %Y"))
        
        # Premier jour du mois et nombre de jours
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, 28) if month != 12 else datetime(year + 1, 1, 1)
        
        # Calculer décalage et jours
        start_weekday = first_day.weekday()  # 0=Lun, 6=Dim
        num_days = (last_day.replace(day=1) - timedelta(days=1)).day
        
        # Récupérer absences du mois
        absence_dates = self._get_month_absences(year, month)
        
        row = 1
        col = start_weekday
        
        for day in range(1, num_days + 1):
            date = datetime(year, month, day)
            has_absence = date in absence_dates
            
            btn_color = ThemeManager.get_color("error") if has_absence else ThemeManager.get_color("card")
            text_color = "white" if has_absence else ThemeManager.get_color("fg")
            
            btn = ctk.CTkButton(
                frame,
                text=str(day),
                width=45,
                height=45,
                fg_color=btn_color,
                text_color=text_color,
                hover_color=ThemeManager.get_color("accent"),
                command=lambda d=day: self._on_date_click(d)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            
            col += 1
            if col > 6:
                col = 0
                row += 1
    
    def _get_month_absences(self, year: int, month: int) -> set:
        """Récupère les dates avec absences du mois"""
        conn = get_conn()
        query = """
        SELECT DISTINCT DATE(date_absence)
        FROM absence
        WHERE YEAR(date_absence) = ? AND MONTH(date_absence) = ?
        """
        rows = conn.execute(query, (year, month)).fetchall()
        conn.close()
        
        absence_dates = set()
        for row in rows:
            try:
                absence_dates.add(datetime.strptime(row[0], "%Y-%m-%d"))
            except:
                pass
        
        return absence_dates
    
    def _on_date_click(self, day: int):
        """Callback du clic sur une date"""
        selected_date = self.current_date.replace(day=day)
        if self.on_date_select:
            self.on_date_select(selected_date)
    
    def _prev_month(self):
        """Mois précédent"""
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self._draw_calendar(self.winfo_children()[0])
    
    def _next_month(self):
        """Mois suivant"""
        year = self.current_date.year
        month = self.current_date.month
        if month == 12:
            self.current_date = datetime(year + 1, 1, 1)
        else:
            self.current_date = datetime(year, month + 1, 1)
        self._draw_calendar(self.winfo_children()[0])
