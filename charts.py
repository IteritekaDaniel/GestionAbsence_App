"""
charts.py — Graphiques avancés avec matplotlib
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta
from database import get_conn

class AdvancedCharts:
    """Création de graphiques avancés"""
    
    @staticmethod
    def create_absence_trend(days: int = 30) -> Figure:
        """Graphique de tendance des absences"""
        conn = get_conn()
        
        # Récupérer les données par jour
        query = """
        SELECT DATE(date_absence) as day, COUNT(*) as count
        FROM absence
        WHERE date_absence >= DATE('now', '-' || ? || ' days')
        GROUP BY DATE(date_absence)
        ORDER BY day
        """
        rows = conn.execute(query, (days,)).fetchall()
        conn.close()
        
        dates = [row[0] for row in rows]
        counts = [row[1] for row in rows]
        
        fig = Figure(figsize=(12, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        ax.plot(dates, counts, marker='o', linewidth=2, markersize=6, color='#0066ff')
        ax.fill_between(range(len(dates)), counts, alpha=0.3, color='#0066ff')
        ax.set_title(f'Tendance des Absences ({days} derniers jours)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Nombre d\'absences')
        ax.grid(True, alpha=0.3)
        fig.autofmt_xdate()
        
        return fig
    
    @staticmethod
    def create_absence_by_class() -> Figure:
        """Graphique des absences par classe"""
        conn = get_conn()
        
        query = """
        SELECT c.class_name, COUNT(a.id) as count
        FROM classe c
        LEFT JOIN student s ON s.class_id = c.id
        LEFT JOIN absence a ON a.student_id = s.id
        GROUP BY c.id, c.class_name
        ORDER BY count DESC
        """
        rows = conn.execute(query).fetchall()
        conn.close()
        
        classes = [row[0] for row in rows]
        counts = [row[1] for row in rows]
        
        fig = Figure(figsize=(12, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Utiliser una palette disponible
        cmap = plt.get_cmap('viridis')
        colors = [cmap(i / len(classes)) for i in range(len(classes))]
        bars = ax.bar(classes, counts, color=colors, edgecolor='black', linewidth=1.2)
        
        # Valeurs sur les barres
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_title('Absences par Classe', fontsize=14, fontweight='bold')
        ax.set_ylabel('Nombre d\'absences')
        ax.grid(True, alpha=0.3, axis='y')
        fig.autofmt_xdate()
        
        return fig
    
    @staticmethod
    def create_absence_status_pie() -> Figure:
        """Graphique pie des statuts d'absences"""
        conn = get_conn()
        
        query = """
        SELECT status, COUNT(*) as count
        FROM absence
        GROUP BY status
        """
        rows = conn.execute(query).fetchall()
        conn.close()
        
        labels = [row[0] for row in rows]
        sizes = [row[1] for row in rows]
        
        colors = {'justified': '#2ecc71', 'unjustified': '#e74c3c', 'pending': '#f39c12'}
        pie_colors = [colors.get(l, '#95a5a6') for l in labels]
        
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        result = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                       colors=pie_colors, startangle=90)
        
        wedges = result[0]
        texts = result[1]
        autotexts = result[2] if len(result) > 2 else []
        
        ax.set_title('Distribution des Statuts d\'Absences', fontsize=14, fontweight='bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        return fig
    
    @staticmethod
    def create_students_alert_chart() -> Figure:
        """Graphique des étudiants en alerte"""
        conn = get_conn()
        
        query = """
        SELECT s.firstname || ' ' || s.lastname as name, COUNT(a.id) as absence_count
        FROM student s
        LEFT JOIN absence a ON a.student_id = s.id
        GROUP BY s.id
        HAVING absence_count >= 3
        ORDER BY absence_count DESC
        LIMIT 15
        """
        rows = conn.execute(query).fetchall()
        conn.close()
        
        if not rows:
            fig = Figure(figsize=(12, 5), dpi=100)
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, 'Aucun étudiant en alerte', 
                   ha='center', va='center', fontsize=14)
            return fig
        
        names = [row[0] for row in rows]
        counts = [row[1] for row in rows]
        
        fig = Figure(figsize=(12, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        colors = ['#e74c3c' if c >= 5 else '#f39c12' for c in counts]
        bars = ax.barh(names, counts, color=colors, edgecolor='black', linewidth=1)
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2., f' {int(width)}',
                   ha='left', va='center', fontweight='bold')
        
        ax.set_title('Top 15 Étudiants en Alerte d\'Absences', fontsize=14, fontweight='bold')
        ax.set_xlabel('Nombre d\'absences')
        ax.grid(True, alpha=0.3, axis='x')
        
        return fig
