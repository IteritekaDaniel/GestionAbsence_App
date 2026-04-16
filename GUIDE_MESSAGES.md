"""
GUIDE_MESSAGES.md — Guide d'Utilisation - Module de Communication
═════════════════════════════════════════════════════════════════

📧 MODULE DE COMMUNICATION - ENVOYER DES EMAILS
═════════════════════════════════════════════════════════════════

## 🎯 QU'EST-CE QUE C'EST?

Le module de communication vous permet d':
✅ Envoyer des messages aux étudiants
✅ Contacter les parents
✅ Alerter sur les absences
✅ Envoyer des rapports
✅ Personnaliser vos messages

## 🚀 DÉMARRAGE RAPIDE

### 1️⃣ CONFIGURER VOTRE EMAIL

Allez à: **Communications** → **Configuration Email**

Remplissez:
- Email d'envoi: votree@gmail.com
- Mot de passe: votre_mot_de_passe_app
- Serveur SMTP: smtp.gmail.com (par défaut)
- Port: 587 (par défaut)
- Nom: DanProject - Gestion Absences

**Pour Gmail:**
1. Activez `Authentication à 2 facteurs` (2FA) / `Validation en deux étapes`
2. Générez un mot de passe d'application
3. Utilisez ce mot de passe ici (NOT votre mot de passe Gmail)

Liens:
- Gmail 2FA: https://myaccount.google.com/security
- Mot de passe app: https://myaccount.google.com/apppasswords

### 2️⃣ TESTER LA CONNEXION

Cliquez sur "🧪 Tester La Connexion"
- ✅ Si OK: Configuration correcte
- ❌ Si erreur: Vérifiez email/mot de passe

### 3️⃣ ENVOYER UN MESSAGE

Allez à: **Communications** → **Envoyer Un Message**

Choisissez:
- **Tous les étudiants**: Envoyer à tous
- **Une classe spécifique**: Choisir 3ème A, 3ème B, etc.
- **Parents**: Contacter les parents
- **Liste personnalisée**: Emails spécifiques

Composez:
- Sujet: Le titre du message
- Message: Le contenu

Variables supportées (remplacées automatiquement):
```
{student_name}   → Prénom Nom de l'étudiant
{class_name}     → Classe (3ème A)
{date}           → Date du jour (06/04/2026)
{school_name}    → Nom de l'établissement
```

Exemple:
```
Sujet: Absence signalée - {student_name}

Bonjour,
Nous avons enregistré une absence pour {student_name} 
de la classe {class_name}.

Merci de régulariser cette situation.

Cordialement,
{school_name}
```

Cliquez "📤 Envoyer"

## 📝 MODÈLES D'EMAIL

Des modèles pré-configurés sont disponibles:

### 1. ALERTE ABSENCE
```
Utilisé pour: Notifier d'une absence
Variables: {student_name}, {class_name}, {date}
```

### 2. RAPPORT JOURNALIER
```
Utilisé pour: Envoyer le résumé du jour
Variables: {total_absences}, {justified}, {unjustified}
```

### 3. MESSAGE PERSONNALISÉ
```
Utilisé pour: Vos propres communications
Variables: Celles que vous créez avec {}
```

## 🔧 EXEMPLES DE MESSAGES

### Exemple 1: Absence Non Justifiée
```
Sujet: Absence à justifier - {student_name}

Bonjour Madame, Monsieur,

Votre enfant {student_name} a une absence non justifiée 
le {date} dans la classe {class_name}.

Pouvez-vous nous envoyer une justification?

Merci,
Direction
```

### Exemple 2: Alerte Absentéisme
```
Sujet: Attention - {student_name}

Bonjour,

{student_name} cumule plusieurs absences.
Nous vous invitons à régulariser rapidement.

Classe: {class_name}
Date: {date}

Cordialement
```

### Exemple 3: Information Générale
```
Sujet: Info importante pour {class_name}

Tous les étudiants de {class_name},

Veuillez noter que...

Merci de votre attention,
Admin
```

## ⚙️ CONFIGURATION AVANCÉE

### Changement de Serveur

Autres serveurs SMTP populaires:

| Service | SMTP | Port | App Password |
|---------|------|------|--------------|
| Gmail | smtp.gmail.com | 587 | ✅ Oui |
| Outlook | smtp-mail.outlook.com | 587 | ✅ Oui |
| Yahoo | smtp.mail.yahoo.com | 587 | ✅ Oui |
| Orange | smtp.orange.fr | 587 | ❓ Non |
| Free | smtp.free.fr | 25 | ❓ Non |

### Vérifier la Configuration

File: `~/.config/DanProject/email_config.json`

Contenu:
```json
{
  "sender_email": "votre@email.com",
  "sender_password": "mot_de_passe_app",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_name": "DanProject - Gestion Absences",
  "enabled": true
}
```

## 🆘 DÉPANNAGE

### ❌ "Email non configuré"
→ Allez à **Configuration Email** et entrez vos paramètres

### ❌ "Erreur: Connexion échouée"
Solutions:
1. Vérifiez votre email/mot de passe
2. Activez le mot de passe d'application (Gmail)
3. Vérifiez votre serveur SMTP
4. Vérifiez votre connexion internet

### ❌ "Messages envoyés: 0"
Raisons possibles:
1. Aucun étudiant dans la base
2. Les étudiants n'ont pas d'email
3. Erreur de configuration SMTP
4. Limite de débit SMTP atteinte

### ❌ "Aucun destinataire trouvé"
→ Vérifiez que la classe/liste existe dans les étudiants

## 📊 HISTORIQUE DES MESSAGES

**Bientôt disponible:**
- Voir tous les messages envoyés
- Jour et heure d'envoi
- Nombre de destinataires
- Statut (succès/erreur)
- Re-envoyer un message

## 🔒 SÉCURITÉ & CONFIDENTIALITÉ

✅ Mot de passe chiffré localement
✅ Pas d'envoi à l'extérieur
✅ Aucun tracking des destinataires
✅ Messages non conservés

⚠️ Attention:
- Gardez votre mot de passe app secret
- Ne le donnez à personne
- Régénérez-le si compromis

## 📋 LISTE DE VÉRIFICATION

Avant d'envoyer en masse:

- [ ] Configuration testée (✅ Tester La Connexion)
- [ ] Sujet clair et complet
- [ ] Message sans erreurs
- [ ] Destinataires corrects
- [ ] Variables correctes

## 💡 CONSEILS D'UTILISATION

1. **Testez d'abord**: Envoyez à vous-même d'abord
2. **Timing**: Évitez l'envoi en masse la nuit
3. **Fréquence**: Pas plus de 1 mail/jour par destinataire
4. **Personnalisez**: Utilisez {student_name} pour plus d'impact
5. **Sauvegardez**: Gardez une copie de vos messages importants

## 📞 CONTACTER LE SUPPORT

Problèmes d'email?
1. Vérifiez votre configuration
2. Testez la connexion SMTP
3. Consultez le dépannage ci-dessus
4. Vérifiez vos paramètres de compte

## 🎓 RESSOURCES

- https://support.google.com/mail/answer/185833 (Gmail SMTP)
- https://help.outlook.com/en-us/outlook-com/msa-outlook-com-faq (Outlook)
- https://help.yahoo.com/kb/SLN4075.html (Yahoo)

═════════════════════════════════════════════════════════════════

DanProject v2.0 - Module de Communication
Envoyez vos messages facilement et en masse!
