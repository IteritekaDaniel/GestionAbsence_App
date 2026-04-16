# 🎓 AbsencesPro v2.0 — Système Complet de Gestion des Absences

**Application desktop Python pour gérer les absences d'étudiants** avec toutes les fonctionnalités professionnelles : notifications email, demandes de validation, alertes intelligentes, multi-administrateurs avec 2FA, et rapports avancés.

---

## ✨ Nouvelles Fonctionnalités (v2.0)

### 📧 **Email & Notifications**
- ✅ Notifications aux parents des absences
- ✅ Alertes de seuil d'absences (configurables)
- ✅ Templates d'email personnalisables
- ✅ Envoi de notifications en masse

### 📋 **Demandes de Validation**
- ✅ Les étudiants demandent la validation de leurs absences
- ✅ Admin approuve/rejette les demandes
- ✅ Workflow complet avec statuts (en attente, approuvé, rejeté)
- ✅ Support des documents justificatifs

### 👨‍👩‍👧 **Gestion des Parents**
- ✅ Enregistrement des contacts parents/tuteurs
- ✅ Email, téléphone, relation (parent/tuteur/autre)
- ✅ Vue de tous les parents associés aux étudiants
- ✅ Export des contacts parents

### 🔔 **Alertes Intelligentes**
- ✅ Règles d'alerte configurables (max absences + période)
- ✅ Alertes par classe ou globales
- ✅ Vérification automatique des seuils
- ✅ Suivi des notifications envoyées

### 🔐 **Sécurité Avancée**
- ✅ Multi-administrateurs avec rôles (Admin/Éditeur/Lecteur)
- ✅ 2FA (Deux Facteurs) avec TOTP/Google Authenticator
- ✅ Codes de secours pour 2FA
- ✅ Validation de force de mot de passe
- ✅ Gestion sécurisée des sessions

### 📊 **Rapports Avancés**
- ✅ Rapports détaillés par étudiant (PDF + CSV)
- ✅ Rapports par date de classe
- ✅ Rapports de période (date de/à)
- ✅ Export des alertes actives
- ✅ Export des demandes en attente
- ✅ Liste de contacts parents

### 📋 **Journaux d'Audit**
- ✅ Traçabilité complète des actions (ADD/UPDATE/DELETE/LOGIN)
- ✅ Filtrage par table, admin, action
- ✅ Détails complets (avant/après valeurs)
- ✅ Export audit en CSV
- ✅ Timestamps et IP logging

### 📝 **Notes Détaillées d'Absence**
- ✅ Types d'absence (justifiée/non-justifiée)
- ✅ Notes admin personnalisées
- ✅ Historique des modifications

---

## 📁 Structure du Projet

```
GestionAbsence App/
│
├── Core
│   ├── main.py                    ← Point d'entrée
│   ├── database.py                ← Schema SQLite (12 tables)
│   └── services.py                ← Logique métier (100+ fonctions)
│
├── UI - Modules de vue
│   ├── ui_login.py                ← Connexion
│   ├── ui_main.py                 ← Navigation principale
│   │
│   ├── ui_students.py             ← Gestion des étudiants
│   ├── ui_parents.py              ← Gestion parents (NEW)
│   ├── ui_absences.py             ← Marquage absences
│   ├── ui_absence_requests.py     ← Demandes validation (NEW)
│   │
│   ├── ui_stats.py                ← Statistiques
│   ├── ui_reports.py              ← Rapports avancés (NEW)
│   │
│   ├── ui_alerts.py               ← Gestion alertes (NEW)
│   ├── ui_admins.py               ← Gestion admins multi-roles (NEW)
│   ├── ui_audit.py                ← Journaux d'audit (NEW)
│   ├── ui_settings.py             ← Paramètres
│
├── Configuration
│   ├── requirements.txt            ← Dépendances
│   └── README.md                   ← Cette doc
│
└── Data
    └── absences.db                 ← Base SQLite (auto-créée)
```

---

## 🗄️ Schéma Base de Données (v2.0)

### Tables Principales
1. **etudiants** - Étudiants (id, nom, prénom, classe, email)
2. **absences** - Absences (id, etudiant_id, date, statut, justification)
3. **parents** - Parents/tuteurs (id, etudiant_id, nom, email, téléphone) **NEW**
4. **absence_notes** - Notes détaillées d'absences (type, notes_admin) **NEW**

### Tables Administrateurs
5. **admin** - Admin legacy (compatibility)
6. **admins_extended** - Admins multi-rôles (username, role, 2fa_enabled) **NEW**
7. **two_fa_tokens** - Tokens 2FA (secret_key, backup_codes) **NEW**

### Tables Workflow
8. **absence_requests** - Demandes de validation (date, raison, statut) **NEW**
9. **threshold_alerts** - Règles d'alerte (max_absences, periode_jours) **NEW**
10. **alert_notifications** - Alertes actives (etudiant_id, message, email_sent) **NEW**

### Tables Système
11. **audit_logs** - Journaux d'audit (action, table_name, old/new_values, ip) **NEW**
12. **email_templates** - Templates d'email (nom, sujet, contenu) **NEW**

---

## 🔧 Installation

### Prérequis
- Python 3.9+
- pip

### Setup rapide

```bash
# 1. Clone/navigate au dossier
cd "GestionAbsence App"

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'app
python main.py
```

### Identifiants par défaut
```
Utilisateur: admin
Mot de passe: admin123
```

**⚠️ IMPORTANT:** Changez le mot de passe par défaut immédiatement dans Settings!

---

## 🚀 Utilisation

### 📖 Navigation
L'interface est organisée en 3 groupes dans la sidebar:

#### GESTION
- **Étudiants** (👥) - CRUD complet, recherche, export
- **Parents** (👨‍👩‍👧) - Ajouter contacts parents, envoyer notifications
- **Absences** (📅) - Marquer absences par date, notes justification

#### SUIVI
- **Demandes** (📋) - Approuver/rejeter demandes d'absence des étudiants
- **Alertes** (🔔) - Configurer règles, voir alertes actives, notifier parents
- **Statistiques** (📊) - KPIs globaux, tendances, graphiques

#### ADMINISTRATION
- **Rapports** (📈) - PDF/CSV détaillés, filtres période/classe
- **Administrateurs** (🔐) - Ajouter admins, gérer rôles, activer 2FA
- **Audit** (📋) - Historique complet des actions, filtrage, export
- **Paramètres** (⚙️) - Compte, préférences, templates email

---

## 🔐 Sécurité

### Meilleures pratiques implémentées

1. **Authentification renforcée**
   - Hashage SHA256 des mots de passe
   - Validation de force de mot de passe (min 8 chars, majuscule, chiffre, spécial)
   - 2FA optionnel par admin

2. **Contrôle d'accès**
   - 3 rôles: Admin (accès total), Éditeur (CRUD), Lecteur (lecture seule)
   - Chaque action est tracée

3. **Audit et traçabilité**
   - Toutes les actions logées (qui, quand, quoi, avant/après)
   - Filtrage par table, admin, action
   - Export audit complet

4. **Protection données**
   - FK CASCADE pour intégrité référentielle
   - Suppression en cascade sécurisée
   - Validation des entrées

---

## 📧 Configuration Email

Pour activer l'envoi d'emails, modifiez `services.py`:

```python
def send_email(destinataire: str, sujet: str, corps: str) -> bool:
    # Configurez vos paramètres SMTP
    SMTP_SERVER = "smtp.gmail.com"
    SENDER_EMAIL = "votre_email@gmail.com"
    SENDER_PASSWORD = "votre_app_password"  # Gmail app password
    ...
```

**Gmail:** Générez un [App Password](https://support.google.com/accounts/answer/185833)

---

## 🔧 API Services (résumé)

### Authentification
```python
services.verify_login(username, password)              # Admin legacy
services.verify_login_extended(username, password)     # Multi-admin
services.validate_password_strength(password)          # Force MDP
```

### Étudiants & Parents
```python
services.get_all_students(search="", classe="")
services.add_student(nom, prenom, classe, email)
services.get_parent(etudiant_id)
services.add_parent(etudiant_id, nom, prenom, email, telephone)
```

### Absences & Demandes
```python
services.mark_absence(etudiant_id, date_str, statut, justification)
services.get_absences_for_date(date_str, classe="")
services.create_absence_request(etudiant_id, date, raison, documents)
services.approve_request(request_id, admin_id, mark_as_present=True)
services.reject_request(request_id, admin_id)
```

### Alertes
```python
services.create_alert_rule(nom, classe, max_absences, periode_jours)
services.check_absence_thresholds()                  # Vérifier tous seuils
services.get_active_alerts(etudiant_id=None)
services.notify_parent_absence(email, etudiant_nom, date, justification)
```

### Gestion Admins & 2FA
```python
services.add_admin(username, password, email, role)  # viewer/editor/admin
services.enable_2fa(admin_id)                        # Retourne secret + backup_codes
services.verify_2fa_token(admin_id, token)
services.update_admin_password(admin_id, new_password)
```

### Audit
```python
services.log_action(admin_id, action, table_name, record_id, old_values, new_values)
services.get_audit_logs(limit=100, admin_id=None, table_name=None)
```

### Rapports & Exports
```python
services.export_csv(filepath, classe="")
services.export_pdf(filepath, date_str, classe="")
services.get_stats_by_student(classe="")
services.get_global_stats()                         # KPIs
```

---

## 🐛 Troubleshooting

### Erreur: "ModuleNotFoundError: No module named 'customtkinter'"
```bash
pip install customtkinter>=5.2.0
```

### Erreur: "Impossible d'envoyer l'email"
- Vérifiez config SMTP dans `services.py`
- Pour Gmail: utilisez un [App Password](https://support.google.com/accounts/answer/185833)
- Vérifiez que le compte autorise connexion "moins sécurisée"

### Erreur: "Database is locked"
- Fermez la base de données dans une autre instance
- Redémarrez l'application

### 2FA n'affiche pas le QR:
```bash
pip install qrcode pillow
```

---

## 📈 Roadmap Future (v3.0)

- [ ] Portal web pour parents
- [ ] Mobile app (Flutter)
- [ ] Intégration Google Calendar
- [ ] SMS notifications
- [ ] Analytics avancées
- [ ] Support multi-langues
- [ ] Sauvegarde cloud automatique
- [ ] Single Sign-On (SSO)

---

## 📄 Licence

Propriétaire - Utilisation personnelle/établissement

---

## 🤝 Support

Pour les bugs ou améliorations: contact via l'app

---

**AbsencesPro v2.0** — Conçu pour simplifier la gestion des absences en établissements scolaires.
Dernière mise à jour: April 2026

**Règle d'or :** L'UI ne touche JAMAIS directement la BDD. Elle passe toujours par services.py.

---

## 🗄️ Base de données

```sql
-- 3 tables
etudiants (id, nom, prenom, classe, email, created_at)
absences  (id, etudiant_id→FK, date, statut, justification)
admin     (id, username, password_hashé, email)
```

La suppression d'un étudiant supprime automatiquement ses absences (ON DELETE CASCADE).

---

## 🚀 Installation et lancement

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Lancer l'application

```bash
python main.py
```

### 3. Connexion par défaut

| Champ          | Valeur    |
|----------------|-----------|
| Utilisateur    | `admin`   |
| Mot de passe   | `admin123`|

---

## 🖥️ Fonctionnalités par vue

### 👥 Étudiants
- Ajouter / Modifier / Supprimer un étudiant
- Recherche dynamique (nom, prénom)
- Filtre par classe
- Tri par colonne (clic sur l'en-tête)
- Export CSV
- Ligne rouge = étudiant avec ≥ 3 absences

### 📅 Absences
- Saisir une date (YYYY-MM-DD)
- Marquer Présent / Absent par double-clic
- "Tous présents" / "Tous absents" en un clic
- Justification d'absence optionnelle
- Sauvegarde groupée (bouton "Tout enregistrer")
- Export PDF du rapport journalier

### 📊 Statistiques
- KPIs : nb étudiants, absences totales, classes, moyenne
- Graphique barres horizontales : Top 10 absents
- Graphique barres par mois (choisir l'année)
- Tableau complet trié par absences décroissantes

### ⚙️ Paramètres
- Choix du thème (Sombre / Clair / Système)
- Modifier username, email, mot de passe admin

---

## 🔒 Sécurité

Les mots de passe sont hashés avec SHA-256 avant stockage.
```python
hashlib.sha256(password.encode()).hexdigest()
```

---

## 📦 Dépendances

| Bibliothèque     | Rôle                        |
|------------------|-----------------------------|
| customtkinter    | Interface graphique moderne |
| matplotlib       | Graphiques statistiques     |
| reportlab        | Export PDF                  |
| sqlite3          | Base de données (intégré)   |
| hashlib          | Hashage des mots de passe   |
