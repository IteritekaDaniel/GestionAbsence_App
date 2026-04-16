"""
email_manager.py — Gestionnaire d'emails avancé
Envoyer des messages à tous les étudiants, groupes, ou une sélection
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path

class EmailManager:
    """Gestionnaire d'emails pour communiquer avec les étudiants et parents"""
    
    def __init__(self):
        """Initialise le gestionnaire d'emails"""
        self.config_file = Path.home() / '.config/DanProject/email_config.json'
        self.config = self._load_config()
        self.smtp_server = None
        self.email_templates = self._load_templates()
    
    def _load_config(self) -> Dict:
        """Charge la configuration SMTP"""
        default_config = {
            'sender_email': '',
            'sender_password': '',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_name': 'DanProject - Gestion Absences',
            'enabled': False,
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    saved = json.load(f)
                    default_config.update(saved)
            except:
                pass
        
        return default_config
    
    def save_config(self, email: str, password: str, smtp_server: str = 'smtp.gmail.com', 
                   smtp_port: int = 587, name: str = 'DanProject'):
        """Sauvegarde la configuration SMTP"""
        self.config.update({
            'sender_email': email,
            'sender_password': password,
            'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'sender_name': name,
            'enabled': True,
        })
        
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _load_templates(self) -> Dict[str, Dict]:
        """Charge les modèles d'email"""
        return {
            'absence_alert': {
                'subject': 'Alerte Absence - {student_name}',
                'body': """
Bonjour,

Nous vous informons que {student_name} de la classe {class_name} 
a enregistré une absence le {date}.

Statut: {status}
Justification: {justification}

Cordialement,
{school_name}
                """
            },
            'daily_report': {
                'subject': 'Rapport Journalier - {date}',
                'body': """
Bonjour,

Veuillez trouver ci-joint le rapport d'absences du {date}.

Nombre total d'absences: {total_absences}
Absences justifiées: {justified}
Absences non justifiées: {unjustified}

Cordialement,
{school_name}
                """
            },
            'custom': {
                'subject': 'Message de DanProject',
                'body': 'Votre message personnalisé'
            }
        }
    
    def test_connection(self) -> bool:
        """Teste la connexion SMTP"""
        if not self.config.get('enabled'):
            return False
        
        try:
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['sender_email'], self.config['sender_password'])
            server.quit()
            return True
        except Exception as e:
            print(f"Erreur connexion email: {e}")
            return False
    
    def send_email(self, recipient_email: str, subject: str, body: str, 
                  attachments: Optional[List[str]] = None) -> bool:
        """Envoie un email simple"""
        if not self.config.get('enabled'):
            print("Email non configuré")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['sender_email']
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Ajouter les pièces jointes
            if attachments:
                for filepath in attachments:
                    self._attach_file(msg, filepath)
            
            # Connecter et envoyer
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['sender_email'], self.config['sender_password'])
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Erreur envoi email: {e}")
            return False
    
    def send_to_students(self, student_list: List[Dict], subject: str, body: str,
                        filter_class: Optional[str] = None, filter_status: Optional[str] = None) -> Dict:
        """Envoie un email à plusieurs étudiants"""
        if not self.config.get('enabled'):
            return {'success': 0, 'failed': 0, 'errors': ['Email non configuré']}
        
        results = {'success': 0, 'failed': 0, 'errors': []}
        
        for student in student_list:
            # Filtrer par classe si demandé
            if filter_class and student.get('classe') != filter_class:
                continue
            
            email = student.get('email')
            if not email:
                results['failed'] += 1
                results['errors'].append(f"Pas d'email pour {student.get('nom')}")
                continue
            
            # Personnaliser le message
            personalized_subject = subject.format(
                student_name=f"{student.get('prenom')} {student.get('nom')}",
                class_name=student.get('classe', '')
            )
            
            personalized_body = body.format(
                student_name=f"{student.get('prenom')} {student.get('nom')}",
                class_name=student.get('classe', ''),
                date=datetime.now().strftime('%d/%m/%Y')
            )
            
            if self.send_email(email, personalized_subject, personalized_body):
                results['success'] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def send_bulk_alert(self, absences_data: List[Dict]) -> Dict:
        """Envoie des alertes d'absence aux parents"""
        if not self.config.get('enabled'):
            return {'success': 0, 'failed': 0}
        
        results = {'success': 0, 'failed': 0}
        
        for absence in absences_data:
            parent_email = absence.get('parent_email')
            if not parent_email:
                continue
            
            subject = f"Alerte Absence - {absence.get('student_name')}"
            body = f"""
Bonjour,

Nous vous informons que {absence.get('student_name')} de la classe {absence.get('class_name')}
a enregistré une absence le {absence.get('date')}.

Statut: {absence.get('status')}

Cordialement,
{self.config['sender_name']}
            """
            
            if self.send_email(parent_email, subject, body):
                results['success'] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def send_daily_report(self, report_data: Dict, recipient_emails: List[str]) -> Dict:
        """Envoie un rapport journalier"""
        if not self.config.get('enabled'):
            return {'success': 0, 'failed': 0}
        
        results = {'success': 0, 'failed': 0}
        
        subject = f"Rapport Journalier - {datetime.now().strftime('%d/%m/%Y')}"
        body = f"""
Bonjour,

Veuillez trouver le rapport d'absences du {datetime.now().strftime('%d/%m/%Y')}.

Résumé:
- Total absences: {report_data.get('total', 0)}
- Justifiées: {report_data.get('justified', 0)}
- Non justifiées: {report_data.get('unjustified', 0)}
- En attente: {report_data.get('pending', 0)}

Détails par classe:
{report_data.get('details', 'N/A')}

Cordialement,
{self.config['sender_name']}
        """
        
        for email in recipient_emails:
            if self.send_email(email, subject, body):
                results['success'] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def send_custom_message(self, recipients: List[str], subject: str, body: str) -> Dict:
        """Envoie un message personnalisé"""
        if not self.config.get('enabled'):
            return {'success': 0, 'failed': 0}
        
        results = {'success': 0, 'failed': 0}
        
        for email in recipients:
            if self.send_email(email, subject, body):
                results['success'] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def _attach_file(self, msg: MIMEMultipart, filepath: str):
        """Ajoute une pièce jointe"""
        try:
            with open(filepath, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {filepath.split("/")[-1]}')
                msg.attach(part)
        except Exception as e:
            print(f"Erreur pièce jointe: {e}")
    
    def get_config(self) -> Dict:
        """Retourne la configuration actuelle"""
        return {
            'enabled': self.config.get('enabled', False),
            'sender_email': self.config.get('sender_email', ''),
            'smtp_server': self.config.get('smtp_server', 'smtp.gmail.com'),
            'smtp_port': self.config.get('smtp_port', 587),
            'sender_name': self.config.get('sender_name', 'DanProject'),
        }
    
    def disable(self):
        """Désactive l'envoi d'emails"""
        self.config['enabled'] = False
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_templates_list(self) -> List[str]:
        """Retourne la liste des modèles disponibles"""
        return list(self.email_templates.keys())
    
    def get_template(self, template_name: str) -> Dict:
        """Retourne un modèle d'email"""
        return self.email_templates.get(template_name, {})

# Instance globale
email_manager = EmailManager()
