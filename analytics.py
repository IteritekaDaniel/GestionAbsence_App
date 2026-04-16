"""
analytics.py — Système d'analytics et statistiques personnalisé
Suivi des activités et générations de rapports
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from pathlib import Path

class Analytics:
    """Système d'analytics respectueux de la vie privée"""
    
    def __init__(self, app_name: str = 'DanProject'):
        self.app_name = app_name
        self.events: List[Dict] = []
        self.session_start = datetime.now()
        self.user_id = None
        self.enabled = False  # Désactivé par défaut
    
    def set_user_id(self, user_id: str):
        """Défini l'ID utilisateur"""
        self.user_id = user_id
    
    def enable(self):
        """Active l'analytique"""
        self.enabled = True
    
    def disable(self):
        """Désactive l'analytique"""
        self.enabled = False
    
    def track_event(self, event_name: str, properties: Optional[Dict] = None):
        """Suit un événement"""
        if not self.enabled:
            return
        
        event = {
            'timestamp': datetime.now().isoformat(),
            'event': event_name,
            'user_id': self.user_id,
            'properties': properties or {}
        }
        self.events.append(event)
    
    def track_page_view(self, page_name: str):
        """Suit une vue de page"""
        self.track_event('page_view', {'page': page_name})
    
    def track_action(self, action: str, target: Optional[str] = None):
        """Suit une action utilisateur"""
        self.track_event('user_action', {
            'action': action,
            'target': target
        })
    
    def track_error(self, error_message: str, error_type: Optional[str] = None):
        """Suit une erreur"""
        self.track_event('error', {
            'message': error_message,
            'type': error_type
        })
    
    def track_performance(self, metric_name: str, value: float, unit: str = 'ms'):
        """Suit une métrique de performance"""
        self.track_event('performance', {
            'metric': metric_name,
            'value': value,
            'unit': unit
        })
    
    def get_session_duration(self) -> timedelta:
        """Retourne la durée de la session"""
        return datetime.now() - self.session_start
    
    def get_events_count(self) -> int:
        """Retourne le nombre d'événements"""
        return len(self.events)
    
    def get_events_by_type(self, event_type: str) -> List[Dict]:
        """Retourne les événements d'un type"""
        return [e for e in self.events if e['event'] == event_type]
    
    def get_summary(self) -> Dict:
        """Retourne un résumé de la session"""
        return {
            'app_name': self.app_name,
            'session_start': self.session_start.isoformat(),
            'session_duration': str(self.get_session_duration()),
            'events_count': self.get_events_count(),
            'user_id': self.user_id,
            'analytics_enabled': self.enabled,
        }
    
    def export_events(self, filepath: str) -> bool:
        """Exporte les événements en JSON"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur export analytics: {e}")
            return False
    
    def clear_events(self):
        """Efface tous les événements"""
        self.events.clear()
    
    def get_stats(self) -> Dict:
        """Retourne les statistiques"""
        stats = {
            'total_events': len(self.events),
            'events_by_type': {},
            'first_event': None,
            'last_event': None,
        }
        
        if self.events:
            for event in self.events:
                event_type = event['event']
                stats['events_by_type'][event_type] = \
                    stats['events_by_type'].get(event_type, 0) + 1
            
            stats['first_event'] = self.events[0]['timestamp']
            stats['last_event'] = self.events[-1]['timestamp']
        
        return stats

class UsageReport:
    """Générateur de rapports d'utilisation"""
    
    def __init__(self, analytics: Analytics):
        self.analytics = analytics
    
    def generate_daily_report(self) -> Dict:
        """Génère un rapport journalier"""
        stats = self.analytics.get_stats()
        return {
            'date': datetime.now().date().isoformat(),
            'session_duration': str(self.analytics.get_session_duration()),
            'total_events': stats['total_events'],
            'events_by_type': stats['events_by_type'],
            'user_id': self.analytics.user_id,
        }
    
    def generate_feature_usage_report(self) -> Dict:
        """Rapport d'utilisation par fonctionnalité"""
        page_views = self.analytics.get_events_by_type('page_view')
        
        feature_usage = {}
        for event in page_views:
            page = event['properties'].get('page', 'unknown')
            feature_usage[page] = feature_usage.get(page, 0) + 1
        
        return {
            'generated_at': datetime.now().isoformat(),
            'feature_usage': feature_usage,
            'most_used_feature': max(feature_usage.items(), 
                                    key=lambda x: x[1])[0] if feature_usage else None,
        }
    
    def generate_error_report(self) -> Dict:
        """Rapport des erreurs"""
        errors = self.analytics.get_events_by_type('error')
        
        error_summary = {}
        for error in errors:
            error_type = error['properties'].get('type', 'unknown')
            if error_type not in error_summary:
                error_summary[error_type] = []
            error_summary[error_type].append(error['properties'].get('message', ''))
        
        return {
            'generated_at': datetime.now().isoformat(),
            'total_errors': len(errors),
            'errors_by_type': error_summary,
        }

# Instance globale
analytics = Analytics('DanProject')
