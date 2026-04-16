"""
database_mysql.py — Connecteur MySQL pour AbsencesPro
Alternative à SQLite pour deployments multi-utilisateurs
"""

import mysql.connector
from mysql.connector import Error
import hashlib
from typing import Optional, Dict, List

# ═══════════════════════════════════════════════════════════════════════════════
#   CONFIGURATION (À adapter selon votre environnement)
# ═══════════════════════════════════════════════════════════════════════════════

DB_CONFIG = {
    "host": "localhost",           # Adresse du serveur MySQL
    "user": "root",                # Utilisateur MySQL
    "password": "",                # Mot de passe MySQL (vide pour XAMPP)
    "database": "gestion_absences",    # Nom de la base créée par le script SQL
    "port": 3306,                  # Port MySQL (par défaut 3306)
    "charset": "utf8mb4",
    "use_unicode": True,
    "autocommit": True             # Auto-commit des changements
}


class MySQLConnection:
    """Gestionnaire de connexion MySQL pour AbsencesPro."""
    
    def __init__(self):
        self.connection = None
    
    def connect(self) -> bool:
        """Établit la connexion à MySQL."""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print(f"[DB] Connecté à MySQL Server version {db_info}")
                return True
        except Error as e:
            if e.errno == 2003:
                print("[ERROR] Impossible de se connecter à MySQL. Vérifiez:")
                print("  1. MySQL est démarré")
                print("  2. Host/Port/User/Password sont corrects")
                print(f"  3. The database '{DB_CONFIG['database']}' existe")
            else:
                print(f"[ERROR] Erreur de connexion: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("[DB] Déconnecté de MySQL")
    
    def execute_query(self, query: str, params: tuple = None, fetch_all: bool = True):
        """
        Exécute une requête SELECT.
        
        Args:
            query: Requête SQL
            params: Paramètres pour la requête (tuple)
            fetch_all: Récupérer tous les résultats ou seulement un
        
        Returns:
            Liste de tuples ou tuple simple
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
            
            cursor.close()
            return result
        except Error as e:
            print(f"[ERROR] Erreur requête: {e}")
            return [] if fetch_all else None
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """
        Exécute une requête INSERT/UPDATE/DELETE.
        
        Args:
            query: Requête SQL
            params: Paramètres
        
        Returns:
            Nombre de lignes affectées
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            affected = cursor.rowcount
            last_id = cursor.lastrowid
            cursor.close()
            
            self.connection.commit()
            return last_id if last_id else affected
        except Error as e:
            print(f"[ERROR] Erreur update: {e}")
            self.connection.rollback()
            return 0
    
    def execute_procedure(self, procedure: str, params: tuple = None):
        """Exécute une procédure stockée."""
        try:
            cursor = self.connection.cursor()
            cursor.callproc(procedure, params or ())
            result = cursor.fetchall() if cursor.description else None
            cursor.close()
            return result
        except Error as e:
            print(f"[ERROR] Erreur procédure: {e}")
            return None


# ═══════════════════════════════════════════════════════════════════════════════
#   WRAPPER MYSQL (compatible avec services.py)
# ═══════════════════════════════════════════════════════════════════════════════

db = MySQLConnection()


def init_db_mysql():
    """Initialise la connexion MySQL."""
    if db.connect():
        print("[DB] ✅ Base MySQL initialisée")
        return True
    else:
        print("[DB] ❌ Échec de connexion à MySQL")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
#   FONCTIONS ADMIN (Exemples d'utilisation)
# ═══════════════════════════════════════════════════════════════════════════════

def verify_login(username: str, password: str) -> bool:
    """Vérifie les identifiants admin."""
    hashed = hashlib.sha256(password.encode()).hexdigest()
    result = db.execute_query(
        "SELECT id FROM admin WHERE username = %s AND password = %s",
        (username, hashed),
        fetch_all=False
    )
    return result is not None


def get_all_students(search: str = "", classe: str = "") -> List[Dict]:
    """Retourne tous les étudiants avec filtres optionnels."""
    query = "SELECT * FROM etudiants WHERE 1=1"
    params = []
    
    if search:
        query += " AND (nom LIKE %s OR prenom LIKE %s)"
        params += [f"%{search}%", f"%{search}%"]
    if classe:
        query += " AND classe = %s"
        params.append(classe)
    
    query += " ORDER BY nom, prenom"
    return db.execute_query(query, tuple(params))


def add_student(nom: str, prenom: str, classe: str, email: str = "") -> int:
    """Ajoute un étudiant. Retourne l'ID créé."""
    return db.execute_update(
        "INSERT INTO etudiants (nom, prenom, classe, email) VALUES (%s, %s, %s, %s)",
        (nom.strip(), prenom.strip(), classe.strip(), email.strip())
    )


def get_stats_by_student(classe: str = "") -> List[Dict]:
    """Retourne les stats par étudiant (absences, présences)."""
    query = """
        SELECT
            e.id,
            e.nom,
            e.prenom,
            e.classe,
            COUNT(CASE WHEN a.statut='absent'  THEN 1 END) AS nb_absences,
            COUNT(CASE WHEN a.statut='present' THEN 1 END) AS nb_presences
        FROM etudiants e
        LEFT JOIN absences a ON a.etudiant_id = e.id
    """
    params = []
    
    if classe:
        query += " WHERE e.classe = %s"
        params.append(classe)
    
    query += " GROUP BY e.id ORDER BY nb_absences DESC"
    return db.execute_query(query, tuple(params) if params else None)


def get_global_stats() -> Dict:
    """Retourne les KPIs globaux."""
    result = db.execute_query(
        """
        SELECT
            (SELECT COUNT(*) FROM etudiants) AS nb_etudiants,
            (SELECT COUNT(*) FROM absences WHERE statut='absent') AS nb_absences_total,
            (SELECT COUNT(DISTINCT classe) FROM etudiants) AS nb_classes
        """
    )
    if result:
        return result[0]
    return {}


# ═══════════════════════════════════════════════════════════════════════════════
#   GESTION MYSQL (Migration, backup, etc.)
# ═══════════════════════════════════════════════════════════════════════════════

def export_config() -> Dict:
    """Exporte la configuration actuelle."""
    return {
        "db_type": "MySQL",
        "host": DB_CONFIG["host"],
        "database": DB_CONFIG["database"],
        "port": DB_CONFIG["port"]
    }


def test_connection() -> bool:
    """Teste la connexion à MySQL."""
    try:
        test_db = mysql.connector.connect(**DB_CONFIG)
        if test_db.is_connected():
            test_db.close()
            print("✅ Connexion MySQL réussie!")
            return True
    except Error as e:
        print(f"❌ Erreur connexion: {e}")
        return False


if __name__ == "__main__":
    print("═" * 70)
    print("AbsencesPro — MySQL Connection Tester")
    print("═" * 70)
    
    print("\n📋 Configuration actuelle:")
    for key, value in DB_CONFIG.items():
        if key != "password":
            print(f"  {key}: {value}")
    
    print("\n🧪 Test de connexion...")
    if test_connection():
        print("\n✅ Vous pouvez maintenant utiliser la base MySQL!")
    else:
        print("\n❌ Veuillez vérifier la configuration:")
        print("  1. Installez MySQL: https://dev.mysql.com/downloads/mysql/")
        print("  2. Exécutez le script SQL: SQL_MySQL_Complete.sql")
        print("  3. Mettez à jour DB_CONFIG avec vos identifiants")
        print("  4. Installez le driver: pip install mysql-connector-python")
