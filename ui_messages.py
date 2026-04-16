"""
ui_messages.py — Interface d'envoi de messages
Envoyer des emails aux étudiants et parents
"""

import customtkinter as ctk
from email_manager import email_manager
import services
from theme_advanced import advanced_theme_manager as theme
from tkinter import messagebox, filedialog
from typing import List, Dict

class MessagesView(ctk.CTkFrame):
    """Vue pour envoyer des messages aux étudiants"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(fg_color=theme.get_color('bg_main'))
        
        self.selected_students = []
        self.selected_parents = []
        
        self._build_ui()
    
    def _build_ui(self):
        """Construit l'interface"""
        
        # ═══════════════════════════════════════════════════════════════════
        # HEADER
        # ═══════════════════════════════════════════════════════════════════
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=15, pady=15)
        
        ctk.CTkLabel(
            header,
            text='💬 Communication',
            font=('Segoe UI', 20, 'bold'),
            text_color=theme.get_color('accent_gold_main')
        ).pack(side='left')
        
        status = '✅ Configuré' if email_manager.config.get('enabled') else '⚠️ Non configuré'
        ctk.CTkLabel(
            header,
            text=status,
            font=('Segoe UI', 11),
            text_color=theme.get_color('success' if email_manager.config.get('enabled') else 'warning')
        ).pack(side='right')
        
        divider = ctk.CTkFrame(self, height=1, fg_color=theme.get_color('surface_border'))
        divider.pack(fill='x')
        divider.configure(height=1)
        
        # ═══════════════════════════════════════════════════════════════════
        # CONTENU PRINCIPAL
        # ═══════════════════════════════════════════════════════════════════
        main_frame = ctk.CTkFrame(self, fg_color='transparent')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # ONGLETS
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill='both', expand=True)
        
        self.tab_send = self.tabview.add('Envoyer Un Message')
        self.tab_config = self.tabview.add('Configuration Email')
        self.tab_history = self.tabview.add('Historique')
        
        self._build_tab_send()
        self._build_tab_config()
        self._build_tab_history()
    
    def _build_tab_send(self):
        """Construit l'onglet d'envoi"""
        
        container = ctk.CTkScrollableFrame(self.tab_send, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ── DESTINATAIRES ──────────────────────────────────────
        ctk.CTkLabel(
            container,
            text='Destinataires',
            font=('Segoe UI', 13, 'bold'),
            text_color=theme.get_color('accent_blue_main')
        ).pack(anchor='w', pady=(0, 10))
        
        dest_frame = ctk.CTkFrame(container, fg_color='transparent')
        dest_frame.pack(fill='x', pady=10)
        
        # Radio buttons pour type de destinataires
        self.recipient_type = ctk.StringVar(value='all_students')
        
        types = [
            ('Tous les étudiants', 'all_students'),
            ('Une classe spécifique', 'class_specific'),
            ('Liste personnalisée', 'custom_list'),
            ('Parents', 'parents'),
        ]
        
        for label, value in types:
            ctk.CTkRadioButton(
                dest_frame,
                text=label,
                variable=self.recipient_type,
                value=value,
                command=self._update_ui
            ).pack(anchor='w', pady=5)
        
        # Selection de classe (caché par défaut)
        self.class_frame = ctk.CTkFrame(container, fg_color='transparent')
        self.class_frame.pack(fill='x', pady=10)
        
        ctk.CTkLabel(
            self.class_frame,
            text='Classe:',
            font=('Segoe UI', 11)
        ).pack(side='left', padx=(0, 10))
        
        self.class_var = ctk.StringVar()
        classes = self._get_classes()
        
        class_dropdown = ctk.CTkComboBox(
            self.class_frame,
            values=classes,
            variable=self.class_var,
            state='readonly',
            width=200
        )
        class_dropdown.pack(side='left')
        self.class_frame.pack_forget()
        
        # ── SUJET ET MESSAGE ───────────────────────────────────
        ctk.CTkLabel(
            container,
            text='Sujet',
            font=('Segoe UI', 13, 'bold'),
            text_color=theme.get_color('accent_blue_main')
        ).pack(anchor='w', pady=(20, 10))
        
        self.subject_entry = ctk.CTkEntry(
            container,
            placeholder_text='Entrez le sujet du message...',
            height=40
        )
        self.subject_entry.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(
            container,
            text='Message',
            font=('Segoe UI', 13, 'bold'),
            text_color=theme.get_color('accent_blue_main')
        ).pack(anchor='w', pady=(10, 10))
        
        self.message_text = ctk.CTkTextbox(
            container,
            height=250,
            fg_color=theme.get_color('input_bg'),
            text_color=theme.get_color('text_primary'),
            border_color=theme.get_color('input_border'),
            border_width=1
        )
        self.message_text.pack(fill='both', expand=True, pady=(0, 15))
        
        # Variables supportées
        vars_text = """
Variables disponibles:
{student_name} - Nom de l'étudiant
{class_name} - Classe
{date} - Date d'aujourd'hui
{school_name} - Nom de l'établissement
        """
        ctk.CTkLabel(
            container,
            text=vars_text,
            font=('Segoe UI', 9),
            text_color=theme.get_color('text_secondary'),
            justify='left'
        ).pack(anchor='w', pady=(0, 15))
        
        # ── BOUTONS D'ACTION ───────────────────────────────────
        button_frame = ctk.CTkFrame(container, fg_color='transparent')
        button_frame.pack(fill='x', pady=20)
        
        ctk.CTkButton(
            button_frame,
            text='📤 Envoyer',
            font=('Segoe UI', 12, 'bold'),
            fg_color=theme.get_color('accent_gold_main'),
            text_color='#0F172A',
            height=40,
            command=self._send_message
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            button_frame,
            text='🔄 Effacer',
            font=('Segoe UI', 12, 'bold'),
            fg_color=theme.get_color('accent_blue_main'),
            text_color='white',
            height=40,
            command=self._clear_form
        ).pack(side='left', padx=5)
    
    def _build_tab_config(self):
        """Construit l'onglet de configuration"""
        
        container = ctk.CTkScrollableFrame(self.tab_config, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        if not email_manager.config.get('enabled'):
            # Configuration SMTP
            ctk.CTkLabel(
                container,
                text='Configuration Email SMTP',
                font=('Segoe UI', 14, 'bold'),
                text_color=theme.get_color('accent_gold_main')
            ).pack(anchor='w', pady=(0, 20))
            
            # Email
            ctk.CTkLabel(container, text='Email d\'envoi:', font=('Segoe UI', 11)).pack(anchor='w', pady=(10, 2))
            self.config_email = ctk.CTkEntry(container, placeholder_text='votre.email@gmail.com', height=35)
            self.config_email.pack(fill='x', pady=(0, 15))
            
            # Mot de passe
            ctk.CTkLabel(container, text='Mot de passe:', font=('Segoe UI', 11)).pack(anchor='w', pady=(10, 2))
            self.config_password = ctk.CTkEntry(container, placeholder_text='••••••••', show='•', height=35)
            self.config_password.pack(fill='x', pady=(0, 15))
            
            # Serveur SMTP
            ctk.CTkLabel(container, text='Serveur SMTP:', font=('Segoe UI', 11)).pack(anchor='w', pady=(10, 2))
            self.config_server = ctk.CTkEntry(container, height=35)
            self.config_server.insert(0, 'smtp.gmail.com')
            self.config_server.pack(fill='x', pady=(0, 15))
            
            # Port SMTP
            ctk.CTkLabel(container, text='Port SMTP:', font=('Segoe UI', 11)).pack(anchor='w', pady=(10, 2))
            self.config_port = ctk.CTkEntry(container, height=35)
            self.config_port.insert(0, '587')
            self.config_port.pack(fill='x', pady=(0, 15))
            
            # Nom de l'expéditeur
            ctk.CTkLabel(container, text='Nom (apparaît dans les emails):', font=('Segoe UI', 11)).pack(anchor='w', pady=(10, 2))
            self.config_name = ctk.CTkEntry(container, height=35)
            self.config_name.insert(0, 'DanProject - Gestion Absences')
            self.config_name.pack(fill='x', pady=(0, 20))
            
            # Boutons
            btn_frame = ctk.CTkFrame(container, fg_color='transparent')
            btn_frame.pack(fill='x', pady=20)
            
            ctk.CTkButton(
                btn_frame,
                text='🧪 Tester La Connexion',
                font=('Segoe UI', 11, 'bold'),
                fg_color=theme.get_color('accent_blue_main'),
                text_color='white',
                height=40,
                command=self._test_email_config
            ).pack(side='left', padx=5)
            
            ctk.CTkButton(
                btn_frame,
                text='✅ Enregistrer',
                font=('Segoe UI', 11, 'bold'),
                fg_color=theme.get_color('accent_gold_main'),
                text_color='#0F172A',
                height=40,
                command=self._save_email_config
            ).pack(side='left', padx=5)
        else:
            # Email déjà configuré
            ctk.CTkLabel(
                container,
                text='✅ Email Configuré',
                font=('Segoe UI', 14, 'bold'),
                text_color=theme.get_color('success')
            ).pack(anchor='w', pady=(0, 20))
            
            config = email_manager.get_config()
            
            info = f"""
Email d'envoi: {config['sender_email']}
Serveur: {config['smtp_server']}:{config['smtp_port']}
Nom: {config['sender_name']}

Statut: Prêt à envoyer des messages
            """
            
            ctk.CTkLabel(
                container,
                text=info,
                font=('Segoe UI', 11),
                text_color=theme.get_color('text_secondary'),
                justify='left'
            ).pack(anchor='w', pady=20)
            
            ctk.CTkButton(
                container,
                text='⚙️ Modifier Configuration',
                font=('Segoe UI', 11, 'bold'),
                fg_color=theme.get_color('accent_blue_main'),
                text_color='white',
                height=40,
                command=self._modify_email_config
            ).pack(fill='x', pady=20)
    
    def _build_tab_history(self):
        """Construit l'onglet d'historique"""
        
        container = ctk.CTkScrollableFrame(self.tab_history, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            container,
            text='Historique des Messages Envoyés',
            font=('Segoe UI', 14, 'bold'),
            text_color=theme.get_color('accent_gold_main')
        ).pack(anchor='w', pady=(0, 20))
        
        # Historique vide pour maintenant
        ctk.CTkLabel(
            container,
            text='Aucun message envoyé pour le moment.',
            font=('Segoe UI', 11),
            text_color=theme.get_color('text_secondary')
        ).pack(pady=30)
    
    # ─────────────────────────────────────────────────────────────────────
    # MÉTHODES D'ACTION
    # ─────────────────────────────────────────────────────────────────────
    
    def _update_ui(self):
        """Met à jour l'UI selon le type de destinataire sélectionné"""
        typ = self.recipient_type.get()
        if typ == 'class_specific':
            self.class_frame.pack(fill='x', pady=10)
        else:
            self.class_frame.pack_forget()
    
    def _get_classes(self) -> List[str]:
        """Récupère la liste des classes"""
        students = services.get_all_students()
        classes = sorted(set(s.get('classe', '') for s in students if s.get('classe')))
        return classes
    
    def _send_message(self):
        """Envoie le message"""
        
        if not email_manager.config.get('enabled'):
            messagebox.showerror('Erreur', 'Email non configuré. Allez à Configuration Email.')
            return
        
        subject = self.subject_entry.get().strip()
        message = self.message_text.get('1.0', 'end-1c').strip()
        
        if not subject or not message:
            messagebox.showwarning('Erreur', 'Sujet et message sont obligatoires.')
            return
        
        recipient_type = self.recipient_type.get()
        
        # Récupérer les destinataires
        if recipient_type == 'all_students':
            recipients = services.get_all_students()
        elif recipient_type == 'class_specific':
            class_name = self.class_var.get()
            if not class_name:
                messagebox.showwarning('Erreur', 'Sélectionnez une classe.')
                return
            recipients = services.get_all_students(classe=class_name)
        elif recipient_type == 'parents':
            recipients = services.get_all_parents()
        else:
            recipients = []
        
        # Envoyer
        result = email_manager.send_to_students(recipients, subject, message)
        
        messagebox.showinfo(
            'Résultat',
            f'Messages envoyés: {result["success"]}\nEchecs: {result["failed"]}'
        )
        
        self._clear_form()
    
    def _clear_form(self):
        """Efface le formulaire"""
        self.subject_entry.delete(0, 'end')
        self.message_text.delete('1.0', 'end')
    
    def _test_email_config(self):
        """Teste la configuration email"""
        if email_manager.test_connection():
            messagebox.showinfo('Succès', 'Connexion email OK!')
        else:
            messagebox.showerror('Erreur', 'La connexion a échoué.\nVérifiez vos identifiants.')
    
    def _save_email_config(self):
        """Sauvegarde la configuration email"""
        email = self.config_email.get().strip()
        password = self.config_password.get()
        server = self.config_server.get().strip()
        port = int(self.config_port.get())
        name = self.config_name.get().strip()
        
        if not email or not password:
            messagebox.showerror('Erreur', 'Email et mot de passe obligatoires.')
            return
        
        email_manager.save_config(email, password, server, port, name)
        messagebox.showinfo('Succès', 'Configuration sauvegardée!')
        
        # Recharger l'interface
        self._build_ui()
    
    def _modify_email_config(self):
        """Modifie la configuration email"""
        email_manager.disable()
        self._build_ui()
