"""
README - GUIDE UTILISATION RAPIDE - DanProject v2.0
"""

# ✨ DanProject v2.0 — GUIDE COMPLET

Bienvenue dans DanProject, votre solution intelligente de gestion!

## 🚀 DÉMARRAGE RAPIDE

### 1️⃣ Lancer l'application
```bash
python main.py
```

### 2️⃣ Identifiants par défaut
- **Nom d'utilisateur:** admin
- **Mot de passe:** admin123

### 3️⃣ Vous êtes connecté!
Vous verrez l'interface principale avec la sidebar de navigation en doré, bleu et rose.

---

## 📚 GUIDE DES PRINCIPALES FONCTIONNALITÉS

### 🎨 1. CHANGER DE THÈME (Doré / Bleu / Rose)

**Méthode 1: Bouton dans la sidebar**
- Cliquez sur le bouton "🌙 Thème" en bas à gauche

**Méthode 2: Raccourci clavier**
- Appuyez sur `Ctrl + Shift + T`

**Effet:** L'interface bascule entre mode clair et mode sombre instantanément

---

## ⌨️ 2. NAVIGATION RAPIDE (Raccourcis Clavier)

Au lieu de cliquer, utilisez ces raccourcis:

| Touche | Action |
|--------|--------|
| `Ctrl + 1` | Voir Étudiants |
| `Ctrl + 2` | Voir Absences |
| `Ctrl + 3` | Voir Parents |
| `Ctrl + 4` | Voir Demandes |
| `Ctrl + 5` | Voir Statistiques |
| `Ctrl + 6` | Voir Rapports |
| `Ctrl + 7` | Voir Alertes |
| `Ctrl + 8` | Voir Audit |
| `Ctrl + Shift + S` | Paramètres |
| `Ctrl + Shift + T` | Basculer Thème |
| `Ctrl + Shift + Q` | Déconnexion |

**Astuce:** Gardez ces raccourcis en mémoire pour accélérer votre travail!

---

### 🔐 3. ACTIVER LA DOUBLE AUTHENTIFICATION (2FA)

Pour plus de sécurité, activez le 2FA:

1. Cliquez sur **⚙️ Paramètres** dans la sidebar
2. Cherchez la section **"Sécurité"**
3. Cliquez sur **"Activer 2FA"**
4. Scannez le QR code affichéé avec **Google Authenticator** ou **Microsoft Authenticator**
5. Entrez le code à 6 chiffres pour confirmer
6. Sauvegardez vos codes de secours (important!)

**Désormais:** À chaque connexion, vous devrez entrer un code de votre téléphone en plus du mot de passe

---

### 📊 4. CONSULTER LES GRAPHIQUES AVANCÉS

---

## 📋 ÉQUIVALENCES d'INTERFACE

Toutes les zones principales accessibles par **sidebar** ou **raccourci clavier**:

```
SIDEBAR              RACCOURCI    DESCRIPTION
─────────────────────────────────────────────────────
👥 Étudiants        Ctrl + 1      Gestion des étudiants
📅 Absences         Ctrl + 2      Enregistrement absences
👨‍👩‍👧 Parents         Ctrl + 3      Contacts des parents
📋 Demandes         Ctrl + 4      Demandes de validation
📊 Statistiques     Ctrl + 5      Graphiques avancés
📈 Rapports         Ctrl + 6      Exportation rapports
🔔 Alertes          Ctrl + 7      Règles d'alertes
📋 Audit            Ctrl + 8      Historique des actions
🔐 Administrateurs  -             Gestion des admins
⚙️ Paramètres       Ctrl + Shift+S Configuration
🌙 Thème            Ctrl + Shift+T Basculer clair/sombre
🔓 Déconnexion      Ctrl + Shift+Q Quitter l'app
```

---

## 🎯 CONSEILS D'UTILISATION

### ✨ Les meilleurs pratiques:

1. **Utilisez les raccourcis clavier** pour aller plus vite
2. **Activez le 2FA** pour plus de sécurité
3. **Exportez régulièrement** vos données en PDF/Excel
4. **Consultez les graphiques** une fois par semaine pour suivre les tendances
5. **Vérifiez l'audit** pour tracer qui a fait quoi et quand

### 🔍 Résolution de problèmes:

**L'application plante?**
- Redémarrez-la: `python main.py`
- Vérifiez que les dépendances sont installées: `pip install -r requirements.txt`

**Les données ne se mettent pas à jour?**
- Actualisez la vue: `Ctrl + F5` ou fermez/réouvrez la fenêtre

**Vous avez oublié le mot de passe 2FA?**
- Utilisez l'un de vos codes de secours sauvegardés
- Ou réactivez le 2FA depuis les paramètres

---

## 📂 STRUCTURE DES FICHIERS

```
GestionAbsence App/
├── main.py                  [Point d'entrée]
├── ui_*.py                  [Interfaces utilisateur]
├── database.py              [Gestion de la base de données]
├── services.py              [Logique métier]
├── theme.py                 [🎨 Système de thème]
├── notifications.py         [🔔 Notifications temps réel]
├── i18n.py                  [🌐 Multi-langue]
├── shortcuts.py             [⌨️ Raccourcis clavier]
├── auth_2fa.py              [🔐 Authentification 2FA]
├── charts.py                [📊 Graphiques avancés]
├── calendar_widget.py       [📅 Calendrier]
├── export_utils.py          [📄 Exports PDF/Excel]
├── config.py                [⚙️ Configuration]
├── requirements.txt         [Dépendances Python]
└── absences.db              [Base de données (créée auto)]
```

---

## 🎓 EXEMPLES D'USAGE AVANCÉ

### Utiliser les notifications dans du code:

```python
from notifications import NotificationManager

# Afficher une notification
NotificationManager.success("Succès", "Les données ont été sauvegardées")
NotificationManager.error("Erreur", "Impossible de créer l'étudiant")
```

### Utiliser le système de thème:

```python
from theme import ThemeManager

# Changer le thème
ThemeManager.set_theme("dark")  # ou "light"

# Récupérer une couleur
color = ThemeManager.get_color("accent")
```

### Utiliser les traductions:

```python
from i18n import t

# Traduire un texte
text = t("students")  # Retourne "Étudiants" en français
```

---

## 📞 SUPPORT & QUESTIONS

**Besoin d'aide?**

1. Consultez la documentation: `AMELIORATIONS_v2.md`
2. Vérifiez les fichiers source (codes bien commentés)
3. Consultez le README original pour plus de détails

---

## 🎉 BONNE UTILISATION!

Vous disposez maintenant d'une application complète, moderne et élégante pour gérer vos données.

**Design:** Doré 🟡 | Bleu 🔵 | Rose 💗  
**Amusez-vous et soyez productif!** 🚀

---

*Dernière mise à jour: 6 Avril 2026*  
*Version: 2.0*
