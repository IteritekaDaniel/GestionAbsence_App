# 📧 EXEMPLES PRATIQUES — UTILISATION DU MODULE MESSAGES

## 📚 Table des Matières
1. [Exemples simples](#exemples-simples)
2. [Exemples avancés](#exemples-avancés)
3. [Scénarios réels](#scénarios-réels)
4. [Erreurs courantes](#erreurs-courantes)
5. [FAQ](#faq)

---

## 📝 Exemples Simples

### 1️⃣ Message Basique à Tous les Étudiants

**Situation:** Vous voulez annoncer quelque chose à tous les étudiants

**Configuration:**
- Destinataires: `Tous les étudiants`
- Sujet: `Annonce importante`
- Message:
```
Bonjour,

Nous vous informons que...

Cordialement,
Management
```

**Résultat:** Email reçu par tous les étudiants dans la base

---

### 2️⃣ Message à Une Classe Spécifique

**Situation:** Vous voulez notifier une seule classe

**Configuration:**
- Destinataires: `Une classe spécifique`
- Choisir: `3ème A` (du ComboBox)
- Sujet: `Info pour 3ème A`
- Message:
```
Bonjour les élèves de 3ème A,

Nous avons une annonce spéciale pour vous...

À bientôt,
Prof
```

**Résultat:** Email reçu seulement par les étudiants de 3ème A

---

### 3️⃣ Message aux Parents

**Situation:** Communiquer avec les parents sur les absences

**Configuration:**
- Destinataires: `Parents`
- Sujet: `Absence de votre enfant`
- Message:
```
Madame, Monsieur,

Votre enfant a une absence...

Merci de la justifier.

Cordialement
```

**Résultat:** Email reçu par tous les parents

---

## 🚀 Exemples Avancés

### Utilisation des Variables Dynamiques

#### 1. Message Personnalisé Automatiquement

**Situation:** Notifier d'absence avec infos spécifiques à chaque étudiant

**Configuration:**
- Destinataires: `Tous les étudiants`
- Sujet: `Absence enregistrée - {student_name}`
- Message:
```
Bonjour {student_name},

Nous avons enregistré votre absence du {date}.
Votre classe: {class_name}

Veuillez la justifier au plus tôt.

Merci,
{school_name}
```

**Exemple d'Email Reçu par Jean Dupont:**
```
Sujet: Absence enregistrée - Jean Dupont

Bonjour Jean Dupont,

Nous avons enregistré votre absence du 06/04/2025.
Votre classe: 3ème A

Veuillez la justifier au plus tôt.

Merci,
Collège Saint-Pierre
```

**Exemple d'Email Reçu par Marie Martin:**
```
Sujet: Absence enregistrée - Marie Martin

Bonjour Marie Martin,

Nous avons enregistré votre absence du 06/04/2025.
Votre classe: 3ème B

Veuillez la justifier au plus tôt.

Merci,
Collège Saint-Pierre
```

#### 2. Alerte Absences aux Parents

**Configuration:**
- Destinataires: `Parents`
- Sujet: `Absence - {student_name}`
- Message:
```
Madame, Monsieur,

Nous vous informons que {student_name} 
a une absence enregistrée le {date}.

Classe: {class_name}
Établissement: {school_name}

Veuillez vérifier la justification.

Cordialement
```

**Variables Remplacées Automatiquement:**
```
{student_name} → Prénom Nom de l'élève
{date}         → 06/04/2025
{class_name}   → 3ème A
{school_name}  → Collège Saint-Pierre
```

---

## 🎯 Scénarios Réels

### Scénario 1: Début de l'Année Scolaire

**Objectif:** Accueillir les étudiants et informer des règles

**Étapes:**

1. **Message 1 - Bienvenue**
   ```
   Destinataires: Tous les étudiants
   Sujet: Bienvenue en {class_name}!
   Message:
   Bienvenue!
   
   Nous sommes heureux de vous accueillir 
   en {class_name}.
   
   N'hésitez pas à contacter Management 
   pour toute question.
   
   Bonne année scolaire!
   {school_name}
   ```

2. **Message 2 - Règlement Absences**
   ```
   Destinataires: Parents
   Sujet: Règlement Absences {school_name}
   Message:
   Madame, Monsieur,
   
   Veuillez prendre connaissance de notre 
   règlement sur les absences...
   
   Merci pour votre collaboration.
   ```

---

### Scénario 2: Gestion des Absences Non Justifiées

**Objectif:** Relancer les absences et parents

**Étapes:**

1. **Jour 1 - Notification à l'étudiant**
   ```
   Destinataires: Tous les étudiants
   Sujet: Absence à justifier - {student_name}
   Message:
   Bonjour {student_name},
   
   Vous avez une absence non justifiée 
   le {date} en {class_name}.
   
   Veuillez présenter une justification.
   
   Merci
   ```

2. **Jour 2 - Alerte aux parents**
   ```
   Destinataires: Parents
   Sujet: URGENT - Absence non justifiée
   Message:
   Madame, Monsieur,
   
   {student_name} a une absence non justifiée.
   Votre action est requise.
   
   Merci de régulariser
   {school_name}
   ```

---

### Scénario 3: Fin de Trimestre

**Objectif:** Envoyer des rapports trimestriels

**Étapes:**

1. **Bulletin Trimestres by Classe**
   ```
   Pour chaque classe (3ème A, 3ème B, etc):
   
   Destinataires: Parents (de cette classe)
   Sujet: Bulletin Trimestre 1 - {class_name}
   Message:
   Madame, Monsieur,
   
   Retrouvez ici le bulletin du trimestre 1
   pour votre enfant en {class_name}.
   
   Absences: X jours
   Justifiées: Y jours
   
   Merci de votre attention
   ```

---

### Scénario 4: Alertes Automatiques

**Objectif:** Avertir des seuils d'absences

**Étapes:**

1. **Email aux Étudiants Absentéistes**
   ```
   Destinataires: Classe (ou Custom list)
   Sujet: ⚠️ Attention - Absences multiples
   Message:
   Cher(e) {student_name},
   
   Nous constatons plusieurs absences.
   Situation actuelle pour {class_name}:
   
   - Absences: 8 jours
   - Justifiées: 2 jours
   
   Nous vous encourageons à régulariser
   cette situation.
   
   {school_name}
   ```

---

## ❌ Erreurs Courantes

### Erreur 1: Variables Non Remplacées

**Problème:**
```
Message reçu:
"Bonjour {student_name}, ..."
```

**Cause:** Mauvaise syntaxe variable

**Solution:**
- ✅ Correct: `{student_name}`
- ❌ Faux: `{student name}` (espace)
- ❌ Faux: `$student_name` (dollar)
- ❌ Faux: `[student_name]` (crochets)

### Erreur 2: Email Non Configuré

**Problème:**
```
❌ Erreur: Email non configuré
```

**Solution:**
1. Allez à: `Onglet Configuration Email`
2. Entrez vos infos:
   - `Email d'envoi` (ex: mon@gmail.com)
   - `Mot de passe app` (Gmail: https://myaccount.google.com/apppasswords)
   - `Serveur SMTP` (Gmail: smtp.gmail.com)
   - `Port` (Gmail: 587)
3. Cliquez `Tester La Connexion`
4. Attendez l'affichage de ✅

### Erreur 3: Pas d'Étudiants Trouvés

**Problème:**
```
❌ Aucun destinataire trouvé (0/0)
```

**Causes Possibles:**
1. La classe n'existe pas
2. Aucun étudiant dans la classe
3. Les étudiants n'ont pas d'email

**Solutions:**
1. Vérifiez les étudiants: `Gestion → Étudiants`
2. Vérifiez qu'ils ont un email
3. Choisissez une autre classe
4. Utilisez "Tous les étudiants" pour tester

### Erreur 4: Mot de Passe Rejeté (Gmail)

**Problème:**
```
❌ Erreur: 535 5.7.8 Username and password not accepted
```

**Cause:** Mot de passe incorrect ou 2FA activée

**Solution:**
1. Activez la 2FA: https://myaccount.google.com/security
2. Générez un "mot de passe app": https://myaccount.google.com/apppasswords
3. Utilisez CE mot de passe (pas votre mot de passe normal)
4. Testez la connexion

### Erreur 5: Serveur SMTP Inaccessible

**Problème:**
```
❌ Erreur: [Errno 111] Connection refused
```

**Cause:** 
- Serveur incorrect
- Port incorrect
- Firewall bloquant

**Solution:**
1. Vérifiez le serveur SMTP:
   - Gmail: `smtp.gmail.com`
   - Outlook: `smtp-mail.outlook.com`
   - Yahoo: `smtp.mail.yahoo.com`
2. Vérifiez le port: `587` (TLS) ou `465` (SSL)
3. Vérifiez votre connexion internet

---

## ❓ FAQ

### Q1: Variables disponibles?

**R:** Variables actuelles:
- `{student_name}` - Prénom Nom étudiant
- `{class_name}` - Classe (ex: 3ème A)
- `{date}` - Date du jour
- `{school_name}` - Nom établissement

D'autres peuvent être ajoutées (ajouter dans `email_manager.py`).

### Q2: Pouvez-vous envoyer des pièces jointes?

**R:** Non actuellement, mais c'est prévu.
Utilisez pour l'instant:
- Google Drive (lien dans message)
- WeTransfer
- Email d'une autre adresse

### Q3: Combien d'emails on peut envoyer?

**R:** Dépend du serveur:
- **Gmail**: ~500 par jour
- **Outlook**: ~300 par jour
- **Autres**: Peut varier

Pour grandes listes, envoyez par batch.

### Q4: Comment programmer l'envoi?

**R:** Pas disponible actuellement.
Solution provisoire:
- Composez le message
- L'envoyer manuellement à l'heure voulue
- Ou utilisez `Task Scheduler` (Windows) / `Cron` (Linux/Mac)

### Q5: Comment supprimer configuration email?

**R:** 
1. Allez à `Configuration Email`
2. Laissez les champs vides
3. Cliquez `Sauvegarder`
4. Le fichier sera réinitialisé

### Q6: Sécurité du mot de passe?

**R:** 
- ✅ Mot de passe stocké localement
- ✅ Jamais envoyé à serveur externe
- ✅ Fichier: `~/.config/DanProject/email_config.json`
- ⚠️ Protégez ce fichier

### Q7: Pouvez-vous voir l'historique des messages?

**R:** Oui - Onglet "Historique"
(Actuellement vide, sera rempli avec les envois)

### Q8: Comment relancer un message?

**R:** Recomposez et envoyez à nouveau
(Historique ne permet pas encore la duplication)

---

## 💡 Conseils d'Utilisation

### ✅ À FAIRE

1. **Testez d'abord**
   ```
   Destinataires: Liste personnalisée (votre email)
   Sujet: Test
   Message: Ceci est un test
   → Vérifiez qu'il arrive
   ```

2. **Utilisez les variables**
   ```
   ✅ Bon: "Bonjour {student_name}"
   ❌ Mauvais: "Bonjour Étudiants"
   ```

3. **Timing approprié**
   - Pas avant 6h du matin
   - Pas après 21h
   - Pas en weekend si possible

4. **Vérifiez les données**
   - Classe existe?
   - Étudiants ont email?
   - Emails valides?

5. **Sauvegardez vos messages importants**
   - Copie dans un document
   - Backup de l'historique

### ❌ À ÉVITER

1. **Ne pas envoyer en masse d'un coup**
   - Risque d'être marqué comme spam
   - Surcharge serveur
   - Solution: 50-100 par jour

2. **Ne pas utiliser des variables inexistantes**
   ```
   ❌ {nom_complet}     (pas supportée)
   ✅ {student_name}    (correcte)
   ```

3. **Ne pas partager config email**
   - Gardez mot de passe secret
   - Ne montrez pas le fichier config

4. **Ne pas envoyer de contenu douteux**
   - Respectez la loi
   - Pas de spam
   - Consentement des parents

5. **Ne pas oublier de tester**
   - D'abord à vous-même
   - Puis petit groupe
   - Puis masse

---

## 🎊 Conclusion

Le module de messages est maintenant prêt pour:
- ✅ Envoyer emails à étudiants/parents
- ✅ Communiquer facilement
- ✅ Personnaliser les messages
- ✅ Conserver historique

**Bon usage! 📧**

---

**DanProject v2.0 - Module de Communication**  
*Facilitez votre gestion scolaire avec des messages personnalisés*
