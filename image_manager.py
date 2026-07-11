"""
image_manager.py — Gestionnaire d'images optimisées et générées
Charge, cache et optimise les images pour l'UI DanProject
"""

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Optional, Tuple
import io

class ImageManager:
    """Gère le cache et l'optimisation des images pour l'application"""
    
    def __init__(self, assets_dir: str = "assets"):
        self.assets_dir = Path(assets_dir)
        self.cache = {}  # Cache CTkImage pour éviter rechargements répétés
        self._ensure_assets_exist()
    
    def _ensure_assets_exist(self):
        """Crée les dossiers d'assets s'ils n'existent pas"""
        for subdir in ['logos', 'banners', 'avatars', 'icons', 'backgrounds']:
            (self.assets_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    # ═════════════════════════════════════════════════════════════════════════
    # CHARGER IMAGES DEPUIS FICHIERS
    # ═════════════════════════════════════════════════════════════════════════
    
    def load_image(self, path: str, size: Tuple[int, int] = (128, 128), 
                   use_cache: bool = True) -> Optional[ctk.CTkImage]:
        """Charge une image d'un fichier et la retourne en CTkImage
        
        Args:
            path: Chemin du fichier (relatif à assets/ ou absolu)
            size: Tuple (width, height) pour redimensionner
            use_cache: Utiliser le cache
            
        Returns:
            CTkImage ou None si le fichier n'existe pas
        """
        
        cache_key = f"{path}_{size}"
        if use_cache and cache_key in self.cache:
            return self.cache[cache_key]
        
        # Chercher le fichier
        if Path(path).exists():
            full_path = Path(path)
        else:
            full_path = self.assets_dir / path
        
        if not full_path.exists():
            print(f"⚠️  Image manquante: {full_path}")
            return None
        
        try:
            pil_image = Image.open(full_path).convert("RGBA")
            pil_image.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Convertir en CTkImage
            ctk_img = ctk.CTkImage(light_image=pil_image, size=size)
            
            if use_cache:
                self.cache[cache_key] = ctk_img
            
            return ctk_img
        except Exception as e:
            print(f"❌ Erreur chargement image {full_path}: {e}")
            return None
    
    # ═════════════════════════════════════════════════════════════════════════
    # GÉNÉRER IMAGES DYNAMIQUEMENT
    # ═════════════════════════════════════════════════════════════════════════
    
    def generate_placeholder(self, size: Tuple[int, int] = (200, 100),
                            text: str = "Logo", bg_color: Tuple[int, int, int] = (200, 100, 200)) -> ctk.CTkImage:
        """Génère un placeholder coloré avec texte
        
        Args:
            size: (width, height)
            text: Texte à afficher au centre
            bg_color: Couleur RGB de fond
            
        Returns:
            CTkImage
        """
        pil_image = Image.new("RGB", size, bg_color)
        draw = ImageDraw.Draw(pil_image)
        
        # Ajouter texte blanc au centre
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        return ctk.CTkImage(light_image=pil_image, size=size)
    
    def generate_avatar(self, initials: str = "AB", size: Tuple[int, int] = (64, 64),
                       bg_color: Tuple[int, int, int] = (100, 150, 200)) -> ctk.CTkImage:
        """Génère un avatar avec les initiales de l'utilisateur
        
        Args:
            initials: 1-2 caractères (ex: "JD" pour Jean Dupont)
            size: (width, height)
            bg_color: Couleur RGB
            
        Returns:
            CTkImage
        """
        pil_image = Image.new("RGB", size, bg_color)
        draw = ImageDraw.Draw(pil_image)
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Lettres en blanc au centre
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        draw.text((x, y), initials.upper(), fill=(255, 255, 255), font=font)
        
        return ctk.CTkImage(light_image=pil_image, size=size)
    
    def generate_gradient_banner(self, size: Tuple[int, int] = (1200, 200),
                                colors: Tuple[Tuple[int, int, int], Tuple[int, int, int]] = ((50, 100, 200), (150, 50, 150))) -> ctk.CTkImage:
        """Génère une bannière avec gradient linéaire
        
        Args:
            size: (width, height)
            colors: ((r1, g1, b1), (r2, g2, b2)) pour le gradient
            
        Returns:
            CTkImage
        """
        pil_image = Image.new("RGB", size)
        pixels = pil_image.load()
        
        # Remplissage gradient horizontal
        for x in range(size[0]):
            ratio = x / size[0]
            r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
            
            for y in range(size[1]):
                pixels[x, y] = (r, g, b)
        
        return ctk.CTkImage(light_image=pil_image, size=size)
    
    # ═════════════════════════════════════════════════════════════════════════
    # UTILITAIRES
    # ═════════════════════════════════════════════════════════════════════════
    
    def clear_cache(self):
        """Vide le cache des images"""
        self.cache.clear()
        print("✅ Cache images vidé")
    
    def get_assets_path(self, asset_type: str = "logos") -> Path:
        """Retourne le chemin du dossier d'assets"""
        return self.assets_dir / asset_type


# Instance globale pour utilisation dans l'app
image_manager = ImageManager()
