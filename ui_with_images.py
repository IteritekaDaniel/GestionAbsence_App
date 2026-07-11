"""
ui_with_images.py — Exemple d'intégration d'images optimisées dans l'UI
Montre comment utiliser l'ImageManager pour charger des images réelles
"""

import customtkinter as ctk
from image_manager import image_manager
from pathlib import Path

class UIWithImages(ctk.CTk):
    """Interface démo avec images optimisées"""
    
    def __init__(self):
        super().__init__()
        
        self.title("DanProject - UI avec Images Optimisées")
        self.geometry("900x700")
        
        # Configuration
        ctk.set_appearance_mode("dark")
        
        # Construire l'interface
        self._build_ui()
    
    def _build_ui(self):
        """Construit l'interface avec images"""
        
        # ═════════════════════════════════════════════════════════════
        # HEADER AVEC BANNIÈRE
        # ═════════════════════════════════════════════════════════════
        
        header_frame = ctk.CTkFrame(self, fg_color="#1F3C88")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Bannière
        banner_img = image_manager.generate_gradient_banner(
            size=(900, 150),
            colors=((31, 60, 136), (147, 51, 234))
        )
        
        if banner_img:
            banner_label = ctk.CTkLabel(header_frame, image=banner_img, text="")
            banner_label.pack(pady=10)
        
        # ═════════════════════════════════════════════════════════════
        # SECTION LOGOS
        # ═════════════════════════════════════════════════════════════
        
        logo_section = ctk.CTkFrame(self)
        logo_section.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(logo_section, text="🎨 LOGOS ET IMAGES",
                    font=("Arial", 16, "bold")).pack(anchor="w")
        
        logo_frame = ctk.CTkFrame(logo_section)
        logo_frame.pack(fill="x", pady=10)
        
        # Logo chargé depuis fichier
        logo_path = image_manager.assets_dir / "logos" / "danproject_logo.png"
        if logo_path.exists():
            logo_img = image_manager.load_image(str(logo_path), size=(128, 128))
            if logo_img:
                logo_label = ctk.CTkLabel(logo_frame, image=logo_img, text="")
                logo_label.pack(side="left", padx=10)
        
        # Logo généré dynamiquement
        gen_logo = image_manager.generate_placeholder(
            size=(128, 128),
            text="Logo\nCustom",
            bg_color=(200, 100, 200)
        )
        logo_label2 = ctk.CTkLabel(logo_frame, image=gen_logo, text="")
        logo_label2.pack(side="left", padx=10)
        
        # ═════════════════════════════════════════════════════════════
        # SECTION AVATARS
        # ═════════════════════════════════════════════════════════════
        
        avatar_section = ctk.CTkFrame(self)
        avatar_section.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(avatar_section, text="👤 AVATARS UTILISATEURS",
                    font=("Arial", 16, "bold")).pack(anchor="w")
        
        avatar_frame = ctk.CTkFrame(avatar_section)
        avatar_frame.pack(fill="x", pady=10)
        
        users = ["JD", "MB", "SD", "AC"]
        colors = [(100, 150, 200), (200, 100, 150), (100, 200, 150), (200, 150, 100)]
        
        for user, color in zip(users, colors):
            avatar_img = image_manager.generate_avatar(user, size=(64, 64), bg_color=color)
            avatar_label = ctk.CTkLabel(avatar_frame, image=avatar_img, text="")
            avatar_label.pack(side="left", padx=10)
        
        # ═════════════════════════════════════════════════════════════
        # SECTION STATISTIQUES AVEC ICÔNES
        # ═════════════════════════════════════════════════════════════
        
        stats_section = ctk.CTkFrame(self)
        stats_section.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(stats_section, text="📊 STATISTIQUES",
                    font=("Arial", 16, "bold")).pack(anchor="w")
        
        stats_frame = ctk.CTkFrame(stats_section)
        stats_frame.pack(fill="both", expand=True, pady=10)
        
        # Charger les icônes
        icons_dir = image_manager.assets_dir / "icons"
        icons_info = [
            ("users.png", "Étudiants", "1,254"),
            ("calendar.png", "Absences", "87"),
            ("alert.png", "Alertes", "12"),
            ("check.png", "Validées", "45"),
        ]
        
        for icon_file, label, value in icons_info:
            icon_path = icons_dir / icon_file
            if icon_path.exists():
                icon_img = image_manager.load_image(str(icon_path), size=(40, 40))
                
                card = ctk.CTkFrame(stats_frame, fg_color="#2D2D2D", corner_radius=10)
                card.pack(side="left", fill="both", expand=True, padx=10, pady=10)
                
                top = ctk.CTkFrame(card, fg_color="transparent")
                top.pack(fill="x", padx=10, pady=(10, 5))
                
                if icon_img:
                    icon_label = ctk.CTkLabel(top, image=icon_img, text="")
                    icon_label.pack(side="left", padx=5)
                
                ctk.CTkLabel(top, text=label, font=("Arial", 12, "bold")).pack(side="left")
                
                ctk.CTkLabel(card, text=value, font=("Arial", 20, "bold"), text_color="#FFD700").pack(pady=(5, 10))
        
        # ═════════════════════════════════════════════════════════════
        # FOOTER AVEC INFO
        # ═════════════════════════════════════════════════════════════
        
        footer = ctk.CTkFrame(self, fg_color="#2D2D2D")
        footer.pack(fill="x", side="bottom", pady=(10, 0))
        
        info_text = "✅ Images optimisées | 💾 Cache mémoire | 🚀 Performance maximale"
        ctk.CTkLabel(footer, text=info_text, text_color="#FFD700").pack(pady=10)


if __name__ == "__main__":
    app = UIWithImages()
    app.mainloop()
