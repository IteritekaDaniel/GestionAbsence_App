#!/usr/bin/env python3
"""
QUICK_START_IMAGES.py — Démarrage rapide optimisation images
Copier-coller pour intégrer images dans votre UI
"""

# ═════════════════════════════════════════════════════════════════════════════
# 1. SETUP INITIAL (À faire une fois)
# ═════════════════════════════════════════════════════════════════════════════

"""
# Étape 1: Générer les assets de démo
python generate_demo_assets.py

# Étape 2: Optimiser (optionnel mais recommandé)
python optimize_images.py

# Étape 3: Tester la démo
python ui_with_images.py
"""

# ═════════════════════════════════════════════════════════════════════════════
# 2. UTILISATION DANS VOTRE CODE
# ═════════════════════════════════════════════════════════════════════════════

import customtkinter as ctk
from image_manager import image_manager

# ─────────────────────────────────────────────────────────────────────────────
# 2.1 CHARGER UNE IMAGE DEPUIS UN FICHIER (AVEC CACHE)
# ─────────────────────────────────────────────────────────────────────────────

def exemple_charger_logo():
    """Charger le logo dans un label"""
    logo = image_manager.load_image(
        "logos/danproject_logo.png",  # Chemin relatif à assets/
        size=(128, 128),               # Redimensionner à 128x128
        use_cache=True                 # ← IMPORTANT: 23x plus rapide
    )
    
    if logo:
        label = ctk.CTkLabel(parent, image=logo, text="")
        label.pack()
    else:
        print("⚠️  Logo non trouvé")


# ─────────────────────────────────────────────────────────────────────────────
# 2.2 GÉNÉRER UN AVATAR DYNAMIQUEMENT
# ─────────────────────────────────────────────────────────────────────────────

def exemple_avatar():
    """Créer un avatar avec les initiales d'un utilisateur"""
    initials = "JD"  # Jean Dupont
    bg_color = (100, 150, 200)  # Bleu
    
    avatar = image_manager.generate_avatar(
        initials=initials,
        size=(64, 64),
        bg_color=bg_color
    )
    
    label = ctk.CTkLabel(parent, image=avatar, text="")
    label.pack()


# ─────────────────────────────────────────────────────────────────────────────
# 2.3 GÉNÉRER UNE BANNIÈRE DÉGRADÉE
# ─────────────────────────────────────────────────────────────────────────────

def exemple_banner():
    """Créer une bannière avec dégradé"""
    banner = image_manager.generate_gradient_banner(
        size=(1200, 200),
        colors=((31, 60, 136), (147, 51, 234))  # Bleu → Violet
    )
    
    label = ctk.CTkLabel(parent, image=banner, text="")
    label.pack()


# ─────────────────────────────────────────────────────────────────────────────
# 2.4 GÉNÉRER UN PLACEHOLDER
# ─────────────────────────────────────────────────────────────────────────────

def exemple_placeholder():
    """Créer un placeholder coloré"""
    placeholder = image_manager.generate_placeholder(
        size=(200, 150),
        text="Photo\nélève",
        bg_color=(200, 100, 200)  # Rose
    )
    
    label = ctk.CTkLabel(parent, image=placeholder, text="")
    label.pack()


# ═════════════════════════════════════════════════════════════════════════════
# 3. PATTERNS COURANTS
# ═════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# PATTERN 1: Afficher un logo avec du texte (sidebar)
# ─────────────────────────────────────────────────────────────────────────────

def pattern_logo_with_text(parent):
    """Afficher logo + texte côte à côte"""
    container = ctk.CTkFrame(parent, fg_color='transparent')
    container.pack()
    
    # Logo
    logo = image_manager.load_image("logos/danproject_logo.png", size=(40, 40))
    if logo:
        logo_label = ctk.CTkLabel(container, image=logo, text="")
        logo_label.pack(side='left', padx=(0, 10))
    
    # Texte
    text_label = ctk.CTkLabel(
        container,
        text="DanProject",
        font=("Arial", 16, "bold")
    )
    text_label.pack(side='left')


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN 2: Liste d'avatars (pour élèves, parents)
# ─────────────────────────────────────────────────────────────────────────────

def pattern_avatars_list(parent, users):
    """Afficher une liste d'avatars + noms"""
    colors = [(100, 150, 200), (200, 100, 150), (100, 200, 150), (200, 150, 100)]
    
    for idx, (nom, prenom) in enumerate(users):
        # Créer une ligne
        row = ctk.CTkFrame(parent)
        row.pack(fill='x', padx=10, pady=5)
        
        # Avatar
        initials = (nom[0] + prenom[0]).upper()
        color = colors[idx % len(colors)]
        avatar = image_manager.generate_avatar(initials, size=(48, 48), bg_color=color)
        
        avatar_label = ctk.CTkLabel(row, image=avatar, text="")
        avatar_label.pack(side='left', padx=10)
        
        # Texte
        text_label = ctk.CTkLabel(row, text=f"{prenom} {nom}", font=("Arial", 12))
        text_label.pack(side='left')


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN 3: Statistiques avec icônes
# ─────────────────────────────────────────────────────────────────────────────

def pattern_stats_with_icons(parent):
    """Afficher des stats avec icônes"""
    stats = [
        ("users.png", "Étudiants", "1,254"),
        ("calendar.png", "Absences", "87"),
        ("alert.png", "Alertes", "12"),
        ("check.png", "Validées", "45"),
    ]
    
    for icon_file, label, value in stats:
        # Charger icône
        icon = image_manager.load_image(f"icons/{icon_file}", size=(40, 40))
        
        # Créer une card
        card = ctk.CTkFrame(parent, fg_color="#2D2D2D", corner_radius=10)
        card.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Icône
        if icon:
            icon_label = ctk.CTkLabel(card, image=icon, text="")
            icon_label.pack(pady=10)
        
        # Label
        label_widget = ctk.CTkLabel(card, text=label, font=("Arial", 12, "bold"))
        label_widget.pack()
        
        # Valeur
        value_label = ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold"), text_color="#FFD700")
        value_label.pack(pady=10)


# ═════════════════════════════════════════════════════════════════════════════
# 4. GESTION DU CACHE (OPTIONNEL)
# ═════════════════════════════════════════════════════════════════════════════

def gerer_cache():
    """Exemples de gestion du cache"""
    
    # Voir la taille du cache
    print(f"Images en cache: {len(image_manager.cache)}")
    
    # Vider le cache (si besoin de mémoire)
    image_manager.clear_cache()
    print("✅ Cache vidé")
    
    # Vider le cache périodiquement
    import threading
    import time
    
    def clear_cache_periodically():
        while True:
            time.sleep(3600)  # Chaque heure
            image_manager.clear_cache()
    
    # thread = threading.Thread(target=clear_cache_periodically, daemon=True)
    # thread.start()


# ═════════════════════════════════════════════════════════════════════════════
# 5. AJOUTER VOS PROPRES IMAGES
# ═════════════════════════════════════════════════════════════════════════════

"""
ÉTAPES:

1. Placer vos images dans assets/:
   cp ma_photo.jpg assets/avatars/
   cp mon_logo.png assets/logos/

2. (OPTIONNEL) Optimiser:
   python optimize_images.py
   → ~35% réduction taille

3. Charger dans votre UI:
   img = image_manager.load_image("avatars/ma_photo.jpg", size=(64, 64))
   label = ctk.CTkLabel(parent, image=img, text="")
   label.pack()
"""


# ═════════════════════════════════════════════════════════════════════════════
# 6. DÉPANNAGE
# ═════════════════════════════════════════════════════════════════════════════

"""
❌ PROBLÈME: "Image manquante"
   ✅ SOLUTION: 
      python generate_demo_assets.py
      
❌ PROBLÈME: "UI lente"
   ✅ SOLUTION: 
      python optimize_images.py
      
❌ PROBLÈME: "PIL not found"
   ✅ SOLUTION: 
      pip install Pillow
      
❌ PROBLÈME: "Cache trop gros"
   ✅ SOLUTION: 
      image_manager.clear_cache()
      
❌ PROBLÈME: "Couleurs bizarres"
   ✅ SOLUTION: 
      Utiliser RGB format (100, 150, 200) pas "blue"
"""


# ═════════════════════════════════════════════════════════════════════════════
# 7. EXEMPLE COMPLET: UI AVEC IMAGES
# ═════════════════════════════════════════════════════════════════════════════

class SimpleUIWithImages(ctk.CTk):
    """Exemple complet d'une UI avec images"""
    
    def __init__(self):
        super().__init__()
        self.title("Mon App avec Images")
        self.geometry("800x600")
        
        # En-tête avec logo
        self.create_header()
        
        # Contenu avec avatars
        self.create_content()
    
    def create_header(self):
        """En-tête avec logo et titre"""
        header = ctk.CTkFrame(self, fg_color="#2D2D2D")
        header.pack(fill='x', pady=(0, 20))
        
        # Logo
        logo = image_manager.load_image("logos/danproject_logo.png", size=(50, 50))
        if logo:
            logo_label = ctk.CTkLabel(header, image=logo, text="")
            logo_label.pack(side='left', padx=20, pady=10)
        
        # Titre
        title = ctk.CTkLabel(header, text="Mon Application", font=("Arial", 20, "bold"))
        title.pack(side='left', padx=10)
    
    def create_content(self):
        """Contenu principal"""
        content = ctk.CTkFrame(self)
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(content, text="👥 Utilisateurs", font=("Arial", 16, "bold")).pack(anchor='w')
        
        # Exemple d'avatars
        users = [("Dupont", "Jean"), ("Bonnet", "Marie"), ("Didier", "Sophie")]
        for nom, prenom in users:
            row = ctk.CTkFrame(content)
            row.pack(fill='x', pady=5)
            
            initials = (nom[0] + prenom[0]).upper()
            avatar = image_manager.generate_avatar(initials, size=(40, 40), bg_color=(100, 150, 200))
            
            avatar_label = ctk.CTkLabel(row, image=avatar, text="")
            avatar_label.pack(side='left', padx=10)
            
            text_label = ctk.CTkLabel(row, text=f"{prenom} {nom}")
            text_label.pack(side='left')


# ═════════════════════════════════════════════════════════════════════════════
# À EXÉCUTER POUR TESTER
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Lancer l'UI démo simple
    app = SimpleUIWithImages()
    app.mainloop()
