"""
optimize_images.py — Script d'optimisation d'images batch
Compresse, redimensionne et optimise toutes les images du dossier assets/
"""

from PIL import Image
from pathlib import Path
import sys
from typing import Tuple, List

class ImageOptimizer:
    """Optimise les images pour la performance d'application"""
    
    def __init__(self, assets_dir: str = "assets"):
        self.assets_dir = Path(assets_dir)
        self.stats = {
            'processed': 0,
            'skipped': 0,
            'errors': 0,
            'original_size': 0,
            'optimized_size': 0
        }
    
    # ─────────────────────────────────────────────────────────────────────────
    # OPTIMISATION PRINCIPALE
    # ─────────────────────────────────────────────────────────────────────────
    
    def optimize_all(self, quality: int = 85, max_width: int = 2000):
        """Optimise toutes les images du dossier assets
        
        Args:
            quality: Qualité JPEG (1-100, défaut 85)
            max_width: Largeur max pour redimensionner
        """
        print("\n" + "="*70)
        print("🖼️  OPTIMISATION D'IMAGES - DanProject")
        print("="*70)
        
        if not self.assets_dir.exists():
            print(f"❌ Dossier {self.assets_dir} non trouvé")
            return False
        
        # Extensions supportées
        supported = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        
        # Parcourir tous les fichiers
        image_files = []
        for ext in supported:
            image_files.extend(self.assets_dir.rglob(f"*{ext}"))
        
        if not image_files:
            print(f"⚠️  Aucune image trouvée dans {self.assets_dir}")
            return False
        
        print(f"\n📁 Trouvé {len(image_files)} images à traiter\n")
        
        # Traiter chaque image
        for img_path in sorted(image_files):
            self._optimize_file(img_path, quality, max_width)
        
        # Afficher statistiques
        self._print_stats()
        return True
    
    def _optimize_file(self, img_path: Path, quality: int, max_width: int):
        """Optimise un fichier image unique"""
        try:
            # Taille avant
            original_size = img_path.stat().st_size
            self.stats['original_size'] += original_size
            
            # Ouvrir et redimensionner si nécessaire
            img = Image.open(img_path)
            
            # Convertir en RGB si nécessaire (pour JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = bg
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionner si > max_width
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                print(f"  📐 Redimensionné: {img_path.name}")
            
            # Sauvegarder optimisée
            output_path = img_path.with_stem(img_path.stem + "_optimized")
            img.save(output_path, "JPEG", quality=quality, optimize=True)
            
            # Remplacer l'original
            optimized_size = output_path.stat().st_size
            img_path.unlink()  # Supprimer original
            output_path.rename(img_path)  # Renommer .optimized en original
            
            # Stat
            self.stats['optimized_size'] += optimized_size
            reduction = ((original_size - optimized_size) / original_size) * 100
            
            print(f"✅ {img_path.name:40} | "
                  f"{original_size/1024:8.1f}KB → {optimized_size/1024:8.1f}KB ({reduction:5.1f}%)")
            self.stats['processed'] += 1
            
        except Exception as e:
            print(f"❌ Erreur: {img_path.name} - {e}")
            self.stats['errors'] += 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # UTILITAIRES
    # ─────────────────────────────────────────────────────────────────────────
    
    def _print_stats(self):
        """Affiche les statistiques d'optimisation"""
        print("\n" + "-"*70)
        print("📊 STATISTIQUES")
        print("-"*70)
        print(f"✅ Traitées:     {self.stats['processed']}")
        print(f"⚠️  Erreurs:      {self.stats['errors']}")
        print(f"⏭️  Ignorées:     {self.stats['skipped']}")
        
        if self.stats['original_size'] > 0:
            total_reduction = ((self.stats['original_size'] - self.stats['optimized_size']) 
                             / self.stats['original_size']) * 100
            print(f"\n💾 Gain d'espace:")
            print(f"   Avant:  {self.stats['original_size']/1024/1024:8.2f} MB")
            print(f"   Après:  {self.stats['optimized_size']/1024/1024:8.2f} MB")
            print(f"   Gain:   {(self.stats['original_size']-self.stats['optimized_size'])/1024/1024:8.2f} MB ({total_reduction:5.1f}%)")
        
        print("="*70 + "\n")
    
    def resize_for_category(self, category: str, target_size: Tuple[int, int]):
        """Redimensionne toutes les images d'une catégorie (logos, avatars, etc.)
        
        Args:
            category: Dossier (logos, avatars, banners, etc.)
            target_size: (width, height) cible
        """
        cat_path = self.assets_dir / category
        if not cat_path.exists():
            print(f"⚠️  Catégorie non trouvée: {category}")
            return
        
        print(f"\n🔄 Redimensionnement {category} à {target_size}...")
        
        for img_path in cat_path.glob("*.png"):
            if img_path.stem.endswith("_optimized"):
                continue
            
            try:
                img = Image.open(img_path)
                img.thumbnail(target_size, Image.Resampling.LANCZOS)
                
                # Remplissage jusqu'à target_size
                if img.size != target_size:
                    bg = Image.new('RGBA', target_size, (0, 0, 0, 0))
                    offset = ((target_size[0] - img.size[0]) // 2,
                             (target_size[1] - img.size[1]) // 2)
                    bg.paste(img, offset, img)
                    img = bg
                
                img.save(img_path, "PNG", optimize=True)
                print(f"  ✅ {img_path.name}")
            except Exception as e:
                print(f"  ❌ {img_path.name}: {e}")


# ─────────────────────────────────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    optimizer = ImageOptimizer()
    
    # Optimisation globale
    optimizer.optimize_all(quality=85, max_width=2000)
    
    # Redimensionner les catégories spécifiques
    print("\n📐 Redimensionnement des catégories...")
    optimizer.resize_for_category("logos", (256, 256))
    optimizer.resize_for_category("avatars", (64, 64))
    optimizer.resize_for_category("banners", (1200, 200))
    optimizer.resize_for_category("icons", (48, 48))
    
    print("\n✨ Optimisation terminée!")
