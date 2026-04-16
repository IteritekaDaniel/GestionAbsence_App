"""
main.py — Point d'entrée de DanProject v2.0
Lance l'application avec support du thème système

╔════════════════════════════════════════════════════════════════╗
║                  ✨ DAN PROJECT v2.0 ✨                        ║
║              Gestion Intelligente & Moderne                    ║
║                                                                ║
║            Couleurs: Doré 50% | Bleu 30% | Rose 20%          ║
║         Mode Système: ✅ | Thème Sombre: ✅ | Sans IA: ✅     ║
╚════════════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
import sys

# Initialiser la base de données
from database import init_db
init_db()

# Importer les modules avancés
from theme_advanced import advanced_theme_manager as theme
from user_preferences import user_preferences
from symbols import Symbols
from ui_login import LoginWindow

if __name__ == "__main__":
    print("-" * 62)
    print(f"✨ {Symbols.APP_NAME} v2.0")
    print(f"   {Symbols.APP_TAGLINE}")
    print("-" * 62)
    print(f"🎨 Thème système: {theme.system_theme.upper()}")
    print(f"🔐 Mode système activé: {'OUI ✅' if theme.use_system_theme else 'NON'}")
    print(f"🎯 Couleurs: Doré 50% | Bleu 30% | Rose 20%")
    print(f"⚡ Sans IA | Respectueux de la vie privée")
    print("-" * 62)
    
    try:
        # Appliquer le thème selon les préférences utilisateur
        theme_pref = user_preferences.get_theme()
        
        if theme_pref == 'dark':
            theme.set_theme('dark')
            ctk.set_appearance_mode("dark")
        elif theme_pref == 'light':
            theme.set_theme('light')
            ctk.set_appearance_mode("light")
        else:  # system (défaut)
            theme.enable_system_theme()
            appearance = "dark" if theme.is_dark_mode() else "light"
            ctk.set_appearance_mode(appearance)
        
        # Configuration CustomTkinter
        ctk.set_default_color_theme("blue")
        
        # Lancer l'application
        print("✅ Démarrage de l'application...")
        app = LoginWindow()
        app.mainloop()
        
    except ImportError as e:
        print(f"❌ Erreur: Module manquant - {e}")
        print("\nInstallation des dépendances:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

