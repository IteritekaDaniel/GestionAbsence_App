# 🎨 PALETTE DE COULEURS - DANPROJECT v2.0

## Couleurs Principales

### Doré (Gold)
- **Clair**: `#FBBF24` - Doré lumineux pour le mode sombre
- **Standard**: `#D4AF37` - Doré élégant pour le mode clair
- **Foncé**: `#B8860B` - Doré foncé (non utilisé directement)
- **Usage**: Titres principaux, accents, logo

### Bleu (Blue)
- **Royal**: `#1E40AF` - Bleu royal clair mode
- **Sky**: `#3B82F6` - Bleu ciel mode sombre
- **Foncé**: `#1E3A8A` - Bleu foncé pour surfaces
- **Usage**: Navigation, boutons principaux, éléments clés

### Rose (Rose)
- **Rose**: `#EC4899` - Rose moderne en mode clair
- **Rose-Clair**: `#F472B6` - Rose clair en mode sombre
- **Usage**: Boutons secondaires, éléments d'accent

---

## Palette Complète (Mode Clair)

```
Fond Principal:     #F8F9FC (Gris ultra-léger)
Texte Principal:    #1A1A2E (Noir deep)
Texte Secondaire:   #6B7280 (Gris)
Carte/Surface:      #FFFFFF (Blanc pur)
Bordure:            #E5E7EB (Gris léger)
Accent Or:          #D4AF37 (Doré)
Accent Bleu:        #1E40AF (Bleu royal)
Accent Rose:        #EC4899 (Rose)
Hover:              #F3F4F6 (Gris très léger)
```

---

## Palette Complète (Mode Sombre)

```
Fond Principal:     #0F172A (Bleu très foncé)
Texte Principal:    #F1F5F9 (Blanc cassé)
Texte Secondaire:   #94A3B8 (Gris clair)
Carte/Surface:      #1E293B (Gris bleu)
Bordure:            #1E293B (Gris bleu)
Accent Or:          #FBBF24 (Doré lumineux)
Accent Bleu:        #3B82F6 (Bleu ciel)
Accent Rose:        #F472B6 (Rose clair)
Hover:              #1E293B (Gris bleu plus clair)
```

---

## États des Boutons

### Bouton Primaire (Bleu)
- **Fond**: Bleu (#1E40AF en clair, #3B82F6 en sombre)
- **Texte**: Blanc
- **Hover**: Doré (#D4AF37 / #FBBF24)

### Bouton Secondaire (Rose)
- **Fond**: Transparent
- **Texte**: Rose (#EC4899 / #F472B6)
- **Hover**: Fond semi-transparent

### Bouton Déconnexion
- **Fond**: Transparent
- **Texte**: Rose intense
- **Hover**: Fond rougeâtre foncé

---

## Éléments de Sévérité

```
✅ Succès:    #10B981 (Vert)
⚠️  Avert:     #F59E0B (Ambre)
❌ Erreur:    #EF4444 (Rouge)
ℹ️  Info:      #3B82F6 (Bleu)
```

---

## Gradients (Optionnel pour future)

### Gradient Doré → Rose
```
De: #D4AF37
À:  #EC4899
```

### Gradient Bleu → Doré
```
De: #1E40AF
À:  #D4AF37
```

### Gradient Rose → Bleu
```
De: #EC4899
À:  #3B82F6
```

---

## Code CSS/Tkinter

### CustomTkinter Colors
```python
from theme import ThemeManager

# Utiliser les couleurs
accent_gold = ThemeManager.get_color("accent_gold")
accent_blue = ThemeManager.get_color("accent")
accent_rose = ThemeManager.get_color("accent_rose")
```

### Mode Clair
```
Light: #F8F9FC background
Light Gold: #D4AF37 accents
Light Blue: #1E40AF navigation
Light Rose: #EC4899 secondary
```

### Mode Sombre
```
Dark: #0F172A background
Dark Gold: #FBBF24 accents
Dark Blue: #3B82F6 navigation
Dark Rose: #F472B6 secondary
```

---

## Inspiration Design

- **Élégance**: Doré apaise luxury et prestige
- **Confiance**: Bleu royal inspire reliability et professionnalisme
- **Énergie**: Rose apaise modernité et dynamisme
- **Harmonie**: Les trois couleurs créent un équilibre visuel

---

## Utilisation Pratique

1. **Titres & Logos**: Doré
2. **Navigation & Actions**: Bleu
3. **Accents secondaires**: Rose
4. **Fond**: Blanc en clair, Bleu très foncé en sombre
5. **Texte**: Noir en clair, Blanc cassé en sombre

---

**Palette créée pour DanProject v2.0**  
**Design: Moderne, Élégant, Professionnel**
