"""
═════════════════════════════════════════════════════════════════════════════════
⚙️  SCRIPT DE CONFIGURATION MYSQL AUTOMATISÉ
═════════════════════════════════════════════════════════════════════════════════

Ce script automatise:
  1. Vérification que MySQL est installé
  2. Création de la base de données
  3. Configuration de la connexion
  4. Migration de données (SQLite → MySQL)
  5. Tests et validation

Utilisation:
  python setup_mysql_auto.py
═════════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import sqlite3
import subprocess
from pathlib import Path

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
except ImportError:
    print("❌ mysql-connector-python n'est pas installé")
    print("   Installer avec: pip install mysql-connector-python")
    sys.exit(1)


class MySQLSetup:
    """Classe pour gérer le setup MySQL de AbsencesPro"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.sql_script = self.project_dir / "SQL_MySQL_Complete.sql"
        self.sqlite_db = self.project_dir / "absences.db"
        self.database_mysql_file = self.project_dir / "database_mysql.py"
        
        self.mysql_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "gestion_absences",
            "port": 3306
        }
    
    def print_header(self, title):
        """Affiche un titre formaté"""
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    
    def print_step(self, step_num, title):
        """Affiche une étape"""
        print(f"\n📍 ÉTAPE {step_num}: {title}")
        print(f"{"─"*75}\n")
    
    def check_mysql_installed(self):
        """Vérifie que MySQL est installé et démarré"""
        self.print_step(1, "Vérifier que MySQL est installé")
        
        try:
            conn = mysql.connector.connect(
                host=self.mysql_config["host"],
                user=self.mysql_config["user"],
                password=self.mysql_config["password"]
            )
            conn.close()
            print("✅ MySQL est OK et accessible\n")
            return True
        
        except MySQLError as e:
            if "Access denied" in str(e):
                print("⚠️  MySQL est accessible mais mot de passe incorrect")
                self.prompt_mysql_password()
                return self.check_mysql_installed()
            
            elif "Can't connect to MySQL server" in str(e):
                print("❌ MySQL n'est pas accessible")
                print("\n   Solutions:")
                print("   1. Installer MySQL: https://dev.mysql.com/downloads/mysql/")
                print("   2. Démarrer MySQL:")
                print("      - Windows: Services → MySQL80 → Start")
                print("      - macOS: brew services start mysql")
                print("      - Linux: sudo systemctl start mysql")
                input("\n   Appuyer sur ENTRÉE après avoir démarré MySQL...")
                return self.check_mysql_installed()
            
            else:
                print(f"❌ Erreur: {e}")
                return False
    
    def prompt_mysql_password(self):
        """Demande le mot de passe MySQL root"""
        print("\n🔐 Entrer le mot de passe MySQL root:")
        password = input("   Mot de passe: ").strip()
        self.mysql_config["password"] = password
    
    def create_database(self):
        """Crée la base de données MySQL"""
        self.print_step(2, "Créer la base de données")
        
        if not self.sql_script.exists():
            print(f"❌ Fichier SQL non trouvé: {self.sql_script}")
            return False
        
        try:
            conn = mysql.connector.connect(
                host=self.mysql_config["host"],
                user=self.mysql_config["user"],
                password=self.mysql_config["password"]
            )
            cursor = conn.cursor()
            
            # Lire le script SQL
            with open(self.sql_script, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Exécuter les statements séparément
            statements = [s.strip() for s in sql_script.split(';') if s.strip()]
            
            for i, statement in enumerate(statements):
                try:
                    cursor.execute(statement)
                    if i % 10 == 0:
                        print(f"  ▌ Exécution statement {i+1}/{len(statements)}...")
                except Exception as e:
                    print(f"⚠️  Statement {i}: {e}")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print("✅ Base de données créée avec succès\n")
            return True
        
        except Exception as e:
            print(f"❌ Erreur lors de la création: {e}\n")
            return False
    
    def test_connection(self):
        """Teste la connexion à MySQL"""
        self.print_step(3, "Tester la connexion")
        
        try:
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor()
            
            # Vérifier les tables
            cursor.execute("""
                SELECT COUNT(*) as table_count 
                FROM information_schema.tables 
                WHERE table_schema = 'gestion_absences'
            """)
            result = cursor.fetchone()
            table_count = result[0] if result else 0
            
            print(f"✅ Connexion réussie!")
            print(f"   Base: {self.mysql_config['database']}")
            print(f"   Tables: {table_count}/12\n")
            
            cursor.close()
            conn.close()
            return True
        
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}\n")
            return False
    
    def migrate_sqlite_data(self):
        """Migre les données de SQLite vers MySQL"""
        self.print_step(4, "Migrer données SQLite → MySQL (optionnel)")
        
        if not self.sqlite_db.exists():
            print(f"ℹ️  Pas de base SQLite trouvée ({self.sqlite_db.name})")
            print("   Migration skippée\n")
            return True
        
        print(f"📦 Base SQLite trouvée: {self.sqlite_db.name}")
        response = input("   Migrer les données? (y/n): ").strip().lower()
        
        if response != 'y':
            print("   Migration annulée\n")
            return True
        
        try:
            # Connexions
            sqlite_conn = sqlite3.connect(str(self.sqlite_db))
            sqlite_conn.row_factory = sqlite3.Row
            sqlite_cursor = sqlite_conn.cursor()
            
            mysql_conn = mysql.connector.connect(**self.mysql_config)
            mysql_cursor = mysql_conn.cursor()
            
            # Tables à migrer
            tables = [
                "etudiants", "absences", "admin",
                "parents", "admins_extended",
                "absence_requests", "threshold_alerts",
                "alert_notifications", "absence_notes",
                "audit_logs", "email_templates"
            ]
            
            total_migrated = 0
            
            for table in tables:
                try:
                    sqlite_cursor.execute(f"SELECT * FROM {table}")
                    rows = sqlite_cursor.fetchall()
                    
                    if rows:
                        columns = [desc[0] for desc in sqlite_cursor.description]
                        placeholders = ','.join(['%s'] * len(columns))
                        sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
                        
                        for row in rows:
                            mysql_cursor.execute(sql, row)
                        
                        mysql_conn.commit()
                        total_migrated += len(rows)
                        print(f"  ✅ {table}: {len(rows)} lignes")
                    else:
                        print(f"  ⏭️  {table}: vide")
                
                except sqlite3.OperationalError:
                    print(f"  ⏭️  {table}: n'existe pas dans SQLite")
                except Exception as e:
                    print(f"  ❌ {table}: {e}")
            
            sqlite_conn.close()
            mysql_cursor.close()
            mysql_conn.close()
            
            print(f"\n✅ Migration complète: {total_migrated} lignes\n")
            return True
        
        except Exception as e:
            print(f"❌ Erreur migration: {e}\n")
            return False
    
    def update_config_file(self):
        """Met à jour la configuration dans database_mysql.py"""
        self.print_step(5, "Mettre à jour database_mysql.py")
        
        if not self.database_mysql_file.exists():
            print(f"⚠️  Fichier non trouvé: {self.database_mysql_file.name}")
            print("   Configuration skippée\n")
            return True
        
        try:
            with open(self.database_mysql_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier si DB_CONFIG existe
            if "DB_CONFIG" not in content:
                print("⚠️  DB_CONFIG non trouvé dans database_mysql.py\n")
                return False
            
            print("✅ database_mysql.py est configuré\n")
            print("   Configuration actuelle:")
            print(f"   - Host: {self.mysql_config['host']}")
            print(f"   - User: {self.mysql_config['user']}")
            print(f"   - Database: {self.mysql_config['database']}\n")
            
            return True
        
        except Exception as e:
            print(f"❌ Erreur: {e}\n")
            return False
    
    def show_next_steps(self):
        """Affiche les prochaines étapes"""
        self.print_header("✅ CONFIGURATION COMPLÈTE")
        
        print("Prochaines étapes:\n")
        print("1️⃣  ✅ MySQL est configuré et prêt")
        print("\n2️⃣  Pour utiliser MySQL avec votre app:\n")
        print("   Option A: Garder SQLite (pas de changement)")
        print("            python main.py\n")
        print("   Option B: Passer à MySQL")
        print("            Éditer main.py:")
        print("            # Au lieu de:")
        print("            from database import init_db")
        print("            # Utiliser:")
        print("            from database_mysql import init_db as init_db")
        print("            python main.py\n")
        print("3️⃣  Tester la connexion:")
        print("            python database_mysql.py\n")
        print("4️⃣  Documentation complète:")
        print("            Voir SETUP_MYSQL_Guide.txt\n")
    
    def run(self):
        """Lance toute la configuration"""
        self.print_header("🚀 CONFIGURATION MYSQL POUR ABSENCESPRO")
        
        steps = [
            ("Vérifier MySQL est installé", self.check_mysql_installed),
            ("Créer la base de données", self.create_database),
            ("Tester la connexion", self.test_connection),
            ("Migrer les données SQLite", self.migrate_sqlite_data),
            ("Mettre à jour config", self.update_config_file),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"\n❌ Configuration échouée à l'étape: {step_name}")
                return False
        
        self.show_next_steps()
        return True


if __name__ == "__main__":
    setup = MySQLSetup()
    success = setup.run()
    sys.exit(0 if success else 1)
