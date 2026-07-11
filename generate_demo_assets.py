"""
generate_demo_assets.py — Génère les images de démo PNG à partir des SVG
À exécuter une fois pour créer les assets initiaux
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_demo_assets():
    """Génère des images démo pour tester l'image manager"""
    
    assets_dir = Path("assets")
    
    # Créer dossiers s'ils n'existent pas
    for subdir in ['logos', 'banners', 'avatars', 'icons', 'backgrounds']:
        (assets_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("🎨 GÉNÉRATION D'IMAGES DE DÉMO")
    print("="*70 + "\n")
    
    # 1. Logo DanProject
    create_logo(assets_dir / "logos" / "danproject_logo.png")
    
    # 2. Bannière header
    create_banner(assets_dir / "banners" / "header_banner.png")
    
    # 3. Avatars de démo
    create_avatars(assets_dir / "avatars")
    
    # 4. Icônes simples
    create_icons(assets_dir / "icons")
    
    # 5. Fond de connexion
    create_background(assets_dir / "backgrounds" / "login_bg.png")
    
    print("\n✨ Images de démo créées avec succès!")
    print(f"📁 Dossier: {assets_dir}")
    print("="*70 + "\n")


def create_logo(output_path: Path):
    """Crée le logo DanProject"""
    img = Image.new("RGB", (256, 256), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Gradient simplifié - cercle doré
    for r in range(120, 0, -1):
        color = (
            255 - int((255-200) * (1 - r/120)),  # R
            int(215 * (r/120)),                   # G
            0                                      # B
        )
        draw.ellipse([(128-r, 128-r), (128+r, 128+r)], fill=color)
    
    # Texte au centre
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    # Calendrier simplifié
    draw.rectangle([(80, 100), (176, 160)], outline=(0, 0, 0), width=2, fill=(255, 255, 255))
    draw.text((128, 120), "DAN", font=font, fill=(0, 0, 0), anchor="mm")
    
    img.save(output_path)
    print(f"✅ Logo créé: {output_path.name}")


def create_banner(output_path: Path):
    """Crée la bannière d'en-tête"""
    img = Image.new("RGB", (1200, 200))
    draw = ImageDraw.Draw(img)
    
    # Gradient bleu → violet
    for x in range(1200):
        ratio = x / 1200
        r = int(31 * (1-ratio) + 147 * ratio)      # 1F -> 93
        g = int(60 * (1-ratio) + 51 * ratio)       # 3C -> 33
        b = int(136 * (1-ratio) + 234 * ratio)     # 88 -> EA
        
        draw.line([(x, 0), (x, 200)], fill=(r, g, b))
    
    # Cercles décoratives
    draw.ellipse([(50, 10), (190, 150)], outline=(255, 215, 0), width=2)
    draw.ellipse([(1050, 50), (1150, 150)], outline=(255, 107, 157), width=2)
    
    # Texte
    try:
        font_title = ImageFont.load_default()
    except:
        font_title = None
    
    draw.text((600, 70), "DanProject", font=font_title, fill=(255, 255, 255), anchor="mm")
    draw.text((600, 120), "Gestion des Absences", font=font_title, fill=(224, 231, 255), anchor="mm")
    
    img.save(output_path)
    print(f"✅ Bannière créée: {output_path.name}")


def create_avatars(output_dir: Path):
    """Crée des avatars de démo"""
    avatars = [
        ("JD", (100, 150, 200)),  # Jean Dupont
        ("MB", (200, 100, 150)),  # Marie Bonnet
        ("SD", (100, 200, 150)),  # Sophie Didier
        ("AC", (200, 150, 100)),  # Alex Curran
    ]
    
    for initials, color in avatars:
        img = Image.new("RGB", (64, 64), color=color)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        draw.text((32, 32), initials, font=font, fill=(255, 255, 255), anchor="mm")
        
        filename = f"avatar_{initials.lower()}.png"
        img.save(output_dir / filename)
        print(f"✅ Avatar créé: {filename}")


def create_icons(output_dir: Path):
    """Crée des icônes simples"""
    icons = {
        "users.png": "👥",
        "calendar.png": "📅",
        "alert.png": "⚠️",
        "check.png": "✓",
        "settings.png": "⚙️",
    }
    
    for filename, symbol in icons.items():
        img = Image.new("RGB", (48, 48), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        
        # Fond coloré
        colors = {
            "users": (59, 130, 246),
            "calendar": (251, 146, 60),
            "alert": (239, 68, 68),
            "check": (34, 197, 94),
            "settings": (168, 85, 247),
        }
        
        for key, color in colors.items():
            if key in filename:
                draw.ellipse([(0, 0), (48, 48)], fill=color)
                break
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        draw.text((24, 24), symbol, font=font, fill=(255, 255, 255), anchor="mm")
        
        img.save(output_dir / filename)
        print(f"✅ Icône créée: {filename}")


def create_background(output_path: Path):
    """Crée un fond de connexion"""
    img = Image.new("RGB", (800, 600))
    draw = ImageDraw.Draw(img)
    
    # Gradient bleu clair → blanc
    for y in range(600):
        ratio = y / 600
        r = int(31 * (1-ratio) + 255 * ratio)
        g = int(60 * (1-ratio) + 255 * ratio)
        b = int(136 * (1-ratio) + 255 * ratio)
        
        draw.line([(0, y), (800, y)], fill=(r, g, b))
    
    # Cercles décoratives
    draw.ellipse([(50, 50), (200, 200)], outline=(255, 215, 0), width=3, fill=None)
    draw.ellipse([(600, 400), (750, 550)], outline=(255, 107, 157), width=3, fill=None)
    
    img.save(output_path)
    print(f"✅ Fond créé: {output_path.name}")


if __name__ == "__main__":
    create_demo_assets()
