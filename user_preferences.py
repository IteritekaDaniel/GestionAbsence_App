"""
user_preferences.py — Gestion des préférences utilisateur
Sauvegarde et chargement des paramètres personnalisés
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

class UserPreferencesManager:
    """Gestionnaire de préférences utilisateur avec persistance"""
    
    # Préférences par défaut
    DEFAULT_PREFERENCES = {
        'theme': 'system',  # system, light, dark
        'use_system_theme': True,
        'language': 'FR',  # FR, EN
        'font_size': 11,
        'notification_sounds': True,
        'email_notifications': True,
        'dark_mode_schedule': False,
        'dark_mode_start': '18:00',
        'dark_mode_end': '06:00',
        'compact_view': False,
        'show_welcome_on_startup': True,
        'auto_backup': True,
        'backup_frequency': 'weekly',  # daily, weekly, monthly
        'two_factor_enabled': False,
        'login_remember': False,
        'sidebar_collapsed': False,
        'sidebar_width': 250,
        'window_width': 1200,
        'window_height': 700,
        'window_position_x': 100,
        'window_position_y': 100,
        'recent_searches': [],
        'favorite_reports': [],
        'last_export_format': 'pdf',
        'last_export_path': '',
        'data_retention_days': 365,
        'enable_analytics': False,
        'custom_colors': {},
        'timezone': 'UTC',
        'date_format': 'DD/MM/YYYY',
        'time_format': '24h',
    }
    
    def __init__(self, app_name: str = 'DanProject'):
        """Initialise le gestionnaire de préférences"""
        self.app_name = app_name
        self.config_dir = self._get_config_directory()
        self.config_file = self.config_dir / 'preferences.json'
        self.preferences = self.DEFAULT_PREFERENCES.copy()
        self._load_preferences()
    
    def _get_config_directory(self) -> Path:
        """Retourne le répertoire de configuration"""
        if os.name == 'nt':  # Windows
            config_dir = Path(os.getenv('APPDATA', os.path.expanduser('~'))) / self.app_name
        else:  # macOS et Linux
            config_dir = Path.home() / f'.config/{self.app_name}'
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    def _load_preferences(self):
        """Charge les préférences depuis le fichier"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                    self.preferences.update(saved)
            except Exception as e:
                print(f"Erreur chargement préférences: {e}")
    
    def save(self):
        """Sauvegarde les préférences"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde préférences: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une préférence"""
        return self.preferences.get(key, default)
    
    def set(self, key: str, value: Any):
        """Définit une préférence"""
        self.preferences[key] = value
        self.save()
    
    def update(self, updates: Dict[str, Any]):
        """Met à jour plusieurs préférences"""
        self.preferences.update(updates)
        self.save()
    
    def reset_to_defaults(self):
        """Réinitialise aux valeurs par défaut"""
        self.preferences = self.DEFAULT_PREFERENCES.copy()
        self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """Retourne toutes les préférences"""
        return self.preferences.copy()
    
    def export_preferences(self, filepath: str) -> bool:
        """Exporte les préférences dans un fichier"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur export: {e}")
            return False
    
    def import_preferences(self, filepath: str) -> bool:
        """Importe des préférences depuis un fichier"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported = json.load(f)
                self.preferences.update(imported)
                self.save()
            return True
        except Exception as e:
            print(f"Erreur import: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════════════════════
    # RACCOURCIS POUR PRÉFÉRENCES COURANTES
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_theme(self) -> str:
        return self.get('theme', 'system')
    
    def set_theme(self, theme: str):
        self.set('theme', theme)
    
    def get_language(self) -> str:
        return self.get('language', 'FR')
    
    def set_language(self, lang: str):
        self.set('language', lang)
    
    def get_font_size(self) -> int:
        return self.get('font_size', 11)
    
    def set_font_size(self, size: int):
        self.set('font_size', max(8, min(20, size)))
    
    def is_dark_mode_enabled(self) -> bool:
        return self.get('theme') == 'dark'
    
    def are_notifications_enabled(self) -> bool:
        return self.get('notification_sounds', True)
    
    def is_two_factor_enabled(self) -> bool:
        return self.get('two_factor_enabled', False)
    
    def get_window_geometry(self) -> tuple[int, int, int, int]:
        """Retourne la géométrie de la fenêtre"""
        return (
            self.get('window_width', 1200),
            self.get('window_height', 700),
            self.get('window_position_x', 100),
            self.get('window_position_y', 100),
        )
    
    def set_window_geometry(self, width: int, height: int, x: int = 0, y: int = 0):
        """Définit la géométrie de la fenêtre"""
        self.update({
            'window_width': width,
            'window_height': height,
            'window_position_x': x,
            'window_position_y': y,
        })
    
    def add_recent_search(self, search: str, max_items: int = 10):
        """Ajoute une recherche récente"""
        searches = self.get('recent_searches', [])
        if search in searches:
            searches.remove(search)
        searches.insert(0, search)
        self.set('recent_searches', searches[:max_items])
    
    def get_recent_searches(self) -> list:
        """Retourne les recherches récentes"""
        return self.get('recent_searches', [])
    
    def add_favorite_report(self, report_id: str):
        """Ajoute un rapport aux favoris"""
        favorites = self.get('favorite_reports', [])
        if report_id not in favorites:
            favorites.append(report_id)
            self.set('favorite_reports', favorites)
    
    def remove_favorite_report(self, report_id: str):
        """Supprime un rapport des favoris"""
        favorites = self.get('favorite_reports', [])
        if report_id in favorites:
            favorites.remove(report_id)
            self.set('favorite_reports', favorites)
    
    def get_favorite_reports(self) -> list:
        """Retourne les rapports favoris"""
        return self.get('favorite_reports', [])
    
    def get_backup_path(self) -> Path:
        """Retourne le chemin pour les sauvegardes"""
        backup_dir = self.config_dir / 'backups'
        backup_dir.mkdir(exist_ok=True)
        return backup_dir
    
    def get_export_path(self) -> str:
        """Retourne le dernier chemin d'export"""
        path = self.get('last_export_path', '')
        if not path or not os.path.exists(os.path.dirname(path)):
            path = str(Path.home() / 'Documents')
        return path
    
    def set_export_path(self, path: str):
        """Définit le chemin d'export"""
        self.set('last_export_path', path)

# Instance globale
user_preferences = UserPreferencesManager('DanProject')
