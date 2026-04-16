"""
theme_advanced.py — Système de thème avancé
Gestion complète: Clair, Sombre, Mode Système (50% Doré, 30% Bleu, 20% Rose)
"""

import customtkinter as ctk
import platform
import os
from typing import Dict, Callable, Optional

class AdvancedThemeManager:
    """Gestionnaire de thème avancé avec Mode Système fiable"""
    
    # ═══════════════════════════════════════════════════════════════════════════
    # THÈME CLAIR (Proportions: 50% Doré, 30% Bleu, 20% Rose)
    # ═══════════════════════════════════════════════════════════════════════════
    LIGHT_THEME = {
        # Palette principale (50% Doré)
        'bg_main': '#FFFFFF',
        'bg_light': '#FAFBFC',
        'bg_darker': '#F3F4F6',
        'accent_gold': '#D4AF37',
        'accent_gold_light': '#F9E79F',
        'accent_gold_ultra_light': '#FEF3C7',
        'accent_gold_dark': '#B8860B',
        'accent_gold_hover': '#FBBF24',
        
        # Palette secondaire (30% Bleu)
        'accent_blue': '#1E40AF',
        'accent_blue_light': '#3B82F6',
        'accent_blue_ultra_light': '#EFF6FF',
        'accent_blue_dark': '#1E3A8A',
        'accent_blue_hover': '#60A5FA',
        
        # Palette tertiaire (20% Rose)
        'accent_rose': '#EC4899',
        'accent_rose_light': '#F472B6',
        'accent_rose_ultra_light': '#FBCFE8',
        'accent_rose_dark': '#BE185D',
        'accent_rose_hover': '#FB7185',
        
        # Textes
        'text_primary': '#1F2937',
        'text_secondary': '#6B7280',
        'text_tertiary': '#9CA3AF',
        'text_light': '#D1D5DB',
        
        # Surfaces
        'surface_bg': '#FFFFFF',
        'surface_secondary': '#F9FAFB',
        'surface_tertiary': '#F3F4F6',
        'surface_elevated': '#FAFBFC',
        'surface_border': '#E5E7EB',
        
        # États
        'success': '#10B981',
        'warning': '#F59E0B',
        'error': '#EF4444',
        'info': '#3B82F6',
        'pending': '#F59E0B',
        
        # Sidebar & Navigation
        'sidebar_bg': '#F9FAFB',
        'sidebar_hover': '#F3F4F6',
        'sidebar_active': '#FEF3C7',
        'nav_text': '#6B7280',
        
        # Cards & Containers
        'card_bg': '#FFFFFF',
        'card_shadow': '#00000008',
        'card_border': '#E5E7EB',
        
        # Input & Forms
        'input_bg': '#FFFFFF',
        'input_border': '#D1D5DB',
        'input_focus': '#3B82F6',
        'input_text': '#1F2937',
        'input_placeholder': '#9CA3AF',
        
        # Buttons
        'btn_primary_bg': '#D4AF37',
        'btn_primary_text': '#FFFFFF',
        'btn_primary_hover': '#FBBF24',
        'btn_secondary_bg': '#1E40AF',
        'btn_secondary_text': '#FFFFFF',
        'btn_secondary_hover': '#3B82F6',
        'btn_tertiary_bg': '#EC4899',
        'btn_tertiary_text': '#FFFFFF',
        'btn_tertiary_hover': '#F472B6',
        
        # Charts & Graphs
        'chart_grid': '#E5E7EB',
        'chart_label': '#6B7280',
        'chart_color_1': '#D4AF37',
        'chart_color_2': '#1E40AF',
        'chart_color_3': '#EC4899',
    }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # THÈME SOMBRE (Proportions: 50% Doré, 30% Bleu, 20% Rose)
    # ═══════════════════════════════════════════════════════════════════════════
    DARK_THEME = {
        # Palette principale (50% Doré lumineux)
        'bg_main': '#0F172A',
        'bg_light': '#1A202C',
        'bg_darker': '#2D3748',
        'accent_gold': '#FBBF24',
        'accent_gold_light': '#FCD34D',
        'accent_gold_ultra_light': '#FEF3C7',
        'accent_gold_dark': '#D4AF37',
        'accent_gold_hover': '#FDE047',
        
        # Palette secondaire (30% Bleu lumineux)
        'accent_blue': '#3B82F6',
        'accent_blue_light': '#60A5FA',
        'accent_blue_ultra_light': '#0F172A',
        'accent_blue_dark': '#1E40AF',
        'accent_blue_hover': '#93C5FD',
        
        # Palette tertiaire (20% Rose lumineux)
        'accent_rose': '#F472B6',
        'accent_rose_light': '#FB7185',
        'accent_rose_ultra_light': '#1A202C',
        'accent_rose_dark': '#EC4899',
        'accent_rose_hover': '#FCA5D0',
        
        # Textes
        'text_primary': '#F3F4F6',
        'text_secondary': '#D1D5DB',
        'text_tertiary': '#9CA3AF',
        'text_light': '#6B7280',
        
        # Surfaces
        'surface_bg': '#0F172A',
        'surface_secondary': '#1A202C',
        'surface_tertiary': '#2D3748',
        'surface_elevated': '#1F2937',
        'surface_border': '#374151',
        
        # États
        'success': '#10B981',
        'warning': '#FBBF24',
        'error': '#F87171',
        'info': '#60A5FA',
        'pending': '#FBBF24',
        
        # Sidebar & Navigation
        'sidebar_bg': '#1A202C',
        'sidebar_hover': '#2D3748',
        'sidebar_active': '#2D2405',
        'nav_text': '#D1D5DB',
        
        # Cards & Containers
        'card_bg': '#1A202C',
        'card_shadow': '#00000020',
        'card_border': '#374151',
        
        # Input & Forms
        'input_bg': '#1F2937',
        'input_border': '#4B5563',
        'input_focus': '#60A5FA',
        'input_text': '#F3F4F6',
        'input_placeholder': '#9CA3AF',
        
        # Buttons
        'btn_primary_bg': '#FBBF24',
        'btn_primary_text': '#0F172A',
        'btn_primary_hover': '#FDE047',
        'btn_secondary_bg': '#3B82F6',
        'btn_secondary_text': '#FFFFFF',
        'btn_secondary_hover': '#60A5FA',
        'btn_tertiary_bg': '#F472B6',
        'btn_tertiary_text': '#FFFFFF',
        'btn_tertiary_hover': '#FB7185',
        
        # Charts & Graphs
        'chart_grid': '#374151',
        'chart_label': '#D1D5DB',
        'chart_color_1': '#FBBF24',
        'chart_color_2': '#3B82F6',
        'chart_color_3': '#F472B6',
    }
    
    def __init__(self):
        """Initialise le gestionnaire avancé de thème"""
        self.current_theme = 'light'
        self.use_system_theme = True
        self.subscribers: list[Callable] = []
        self.system_theme = 'light'
        self._initialize_system_theme()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DÉTECTION DU THÈME SYSTÈME
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _initialize_system_theme(self):
        """Initialise et détecte le thème système de manière fiable"""
        try:
            self._detect_system_theme()
            if self.use_system_theme:
                self.current_theme = self.system_theme
                self._apply_appearance_mode()
        except Exception as e:
            print(f"Erreur détection thème système: {e}")
            self.current_theme = 'light'
            self.system_theme = 'light'
            self.use_system_theme = False
    
    def _detect_system_theme(self):
        """Détecte le thème système selon le système d'exploitation"""
        try:
            if platform.system() == 'Windows':
                self._detect_windows_theme()
            elif platform.system() == 'Darwin':
                self._detect_macos_theme()
            else:
                self._detect_linux_theme()
        except Exception as e:
            print(f"Erreur: {e}")
            self.system_theme = 'light'
    
    def _detect_windows_theme(self):
        """Détecte le thème sur Windows via le registre"""
        try:
            import winreg
            registry_path = r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize'
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, registry_path)
            value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
            self.system_theme = 'light' if value == 1 else 'dark'
            winreg.CloseKey(key)
        except Exception:
            self.system_theme = 'light'
    
    def _detect_macos_theme(self):
        """Détecte le thème sur macOS"""
        try:
            import subprocess
            result = subprocess.run(
                ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                capture_output=True,
                text=True,
                timeout=2
            )
            self.system_theme = 'dark' if result.returncode == 0 else 'light'
        except Exception:
            self.system_theme = 'light'
    
    def _detect_linux_theme(self):
        """Détecte le thème sur Linux (GTK/GNOME)"""
        try:
            config_file = os.path.expanduser('~/.config/gtk-3.0/settings.ini')
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    content = f.read()
                    if 'gtk-application-prefer-dark-theme=1' in content:
                        self.system_theme = 'dark'
                    else:
                        self.system_theme = 'light'
            else:
                self.system_theme = 'light'
        except Exception:
            self.system_theme = 'light'
    
    def _apply_appearance_mode(self):
        """Applique le mode d'apparence à CustomTkinter"""
        try:
            if self.current_theme == 'dark':
                ctk.set_appearance_mode('dark')
            else:
                ctk.set_appearance_mode('light')
        except Exception as e:
            print(f"Erreur application thème: {e}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # GESTION DU THÈME
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_color(self, color_key: str) -> str:
        """Retourne une couleur du thème actuel"""
        theme = self.DARK_THEME if self.current_theme == 'dark' else self.LIGHT_THEME
        return theme.get(color_key, '#FFFFFF')
    
    def get_colors(self, *color_keys: str) -> Dict[str, str]:
        """Retourne plusieurs couleurs en une seule requête"""
        return {key: self.get_color(key) for key in color_keys}
    
    def set_theme(self, theme: str):
        """Change le thème (light/dark)"""
        if theme in ['light', 'dark']:
            self.current_theme = theme
            self.use_system_theme = False
            self._apply_appearance_mode()
            self._notify_subscribers()
    
    def toggle_theme(self) -> str:
        """Bascule entre clair et sombre"""
        self.set_theme('dark' if self.current_theme == 'light' else 'light')
        return self.current_theme
    
    def enable_system_theme(self):
        """Active le suivi du thème système"""
        self.use_system_theme = True
        self._detect_system_theme()
        self.current_theme = self.system_theme
        self._apply_appearance_mode()
        self._notify_subscribers()
    
    def disable_system_theme(self):
        """Désactive le suivi du thème système"""
        self.use_system_theme = False
    
    def is_dark_mode(self) -> bool:
        """Vérifie si le mode sombre est actif"""
        return self.current_theme == 'dark'
    
    def is_light_mode(self) -> bool:
        """Vérifie si le mode clair est actif"""
        return self.current_theme == 'light'
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ABONNEMENTS AUX CHANGEMENTS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def subscribe(self, callback: Callable):
        """S'abonne aux changements de thème"""
        if callback not in self.subscribers:
            self.subscribers.append(callback)
    
    def unsubscribe(self, callback: Callable):
        """Se désabonne des changements de thème"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)
    
    def _notify_subscribers(self):
        """Notifie tous les abonnés"""
        for callback in self.subscribers:
            try:
                callback()
            except Exception as e:
                print(f"Erreur callback thème: {e}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ACCÈS AUX DICTIONNAIRES
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_theme_dict(self) -> Dict[str, str]:
        """Retourne le dictionnaire complet du thème actuel"""
        return self.DARK_THEME if self.current_theme == 'dark' else self.LIGHT_THEME
    
    def get_light_theme(self) -> Dict[str, str]:
        """Retourne le thème clair"""
        return self.LIGHT_THEME
    
    def get_dark_theme(self) -> Dict[str, str]:
        """Retourne le thème sombre"""
        return self.DARK_THEME
    
    def get_status(self) -> Dict:
        """Retourne le statut complet du gestionnaire"""
        return {
            'current_theme': self.current_theme,
            'system_theme': self.system_theme,
            'use_system_theme': self.use_system_theme,
            'is_dark': self.is_dark_mode(),
            'is_light': self.is_light_mode(),
        }

# Instance globale avec support complet du thème système
advanced_theme_manager = AdvancedThemeManager()
