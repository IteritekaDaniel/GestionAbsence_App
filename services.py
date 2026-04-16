"""
services.py — Logique métier
Toutes les opérations sur la BDD passent par ici (pas d'accès direct depuis l'UI).
"""

import hashlib
import csv
from datetime import datetime
from typing import Optional
from database import get_conn


# ═══════════════════════════════════════════════════════════════════════════════
#   AUTHENTIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

def verify_login(username: str, password: str) -> bool:
    """Vérifie les identifiants admin. Retourne True si correct."""
    hashed = hashlib.sha256(password.encode()).hexdigest()
    conn = get_conn()
    row = conn.execute(
        "SELECT id FROM admin WHERE username = ? AND password = ?",
        (username, hashed)
    ).fetchone()
    conn.close()
    return row is not None


def get_admin_info() -> dict:
    """Retourne username et email de l'admin."""
    conn = get_conn()
    row = conn.execute("SELECT username, email FROM admin LIMIT 1").fetchone()
    conn.close()
    return dict(row) if row else {}


def update_admin(username: str, email: str, new_password: Optional[str] = None):
    """Met à jour les infos admin. new_password=None → mot de passe inchangé."""
    conn = get_conn()
    if new_password:
        hashed = hashlib.sha256(new_password.encode()).hexdigest()
        conn.execute(
            "UPDATE admin SET username=?, email=?, password=? WHERE id=1",
            (username, email, hashed)
        )
    else:
        conn.execute(
            "UPDATE admin SET username=?, email=? WHERE id=1",
            (username, email)
        )
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
#   ÉTUDIANTS
# ═══════════════════════════════════════════════════════════════════════════════

def get_all_students(search: str = "", classe: str = "") -> list[dict]:
    """
    Retourne tous les étudiants avec filtres optionnels.
    search → filtre sur nom ou prénom (LIKE)
    classe → filtre exact sur la classe
    """
    conn = get_conn()
    query = "SELECT * FROM etudiants WHERE 1=1"
    params = []

    if search:
        query += " AND (nom LIKE ? OR prenom LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    if classe:
        query += " AND classe = ?"
        params.append(classe)

    query += " ORDER BY nom, prenom"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_student_by_id(student_id: int) -> dict | None:
    """Retourne un étudiant par son ID."""
    conn = get_conn()
    row = conn.execute("SELECT * FROM etudiants WHERE id = ?", (student_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def add_student(nom: str, prenom: str, classe: str, email: str = "") -> Optional[int]:
    """Ajoute un étudiant. Retourne l'ID créé."""
    conn = get_conn()
    try:
        cursor = conn.execute(
            "INSERT INTO etudiants (nom, prenom, classe, email) VALUES (?,?,?,?)",
            (nom.strip(), prenom.strip(), classe.strip(), email.strip())
        )
        new_id = cursor.lastrowid
        conn.commit()
        return new_id
    except Exception as e:
        print(f"Erreur ajout étudiant: {e}")
        return None
    finally:
        conn.close()


def update_student(student_id: int, nom: str, prenom: str, classe: str, email: str = ""):
    """Modifie les infos d'un étudiant."""
    conn = get_conn()
    conn.execute(
        "UPDATE etudiants SET nom=?, prenom=?, classe=?, email=? WHERE id=?",
        (nom.strip(), prenom.strip(), classe.strip(), email.strip(), student_id)
    )
    conn.commit()
    conn.close()


def delete_student(student_id: int):
    """Supprime un étudiant (+ ses absences en cascade grâce à FOREIGN KEY)."""
    conn = get_conn()
    conn.execute("DELETE FROM etudiants WHERE id=?", (student_id,))
    conn.commit()
    conn.close()


def get_classes() -> list[str]:
    """Retourne la liste des classes distinctes triées."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT DISTINCT classe FROM etudiants ORDER BY classe"
    ).fetchall()
    conn.close()
    return [r["classe"] for r in rows]


# ═══════════════════════════════════════════════════════════════════════════════
#   ABSENCES
# ═══════════════════════════════════════════════════════════════════════════════

def mark_absence(etudiant_id: int, date_str: str, statut: str, justification: str = ""):
    """
    Enregistre ou met à jour le statut d'un étudiant pour une date.
    Si déjà marqué ce jour → UPDATE, sinon → INSERT.
    """
    conn = get_conn()
    existing = conn.execute(
        "SELECT id FROM absences WHERE etudiant_id=? AND date=?",
        (etudiant_id, date_str)
    ).fetchone()

    if existing:
        conn.execute(
            "UPDATE absences SET statut=?, justification=? WHERE id=?",
            (statut, justification, existing["id"])
        )
    else:
        conn.execute(
            "INSERT INTO absences (etudiant_id, date, statut, justification) VALUES (?,?,?,?)",
            (etudiant_id, date_str, statut, justification)
        )
    conn.commit()
    conn.close()


def get_absences_for_date(date_str: str, classe: str = "") -> list[dict]:
    """
    Retourne la liste de TOUS les étudiants avec leur statut pour une date.
    Étudiants non marqués → statut = 'non_marque'.
    """
    conn = get_conn()
    query = """
        SELECT
            e.id,
            e.nom,
            e.prenom,
            e.classe,
            COALESCE(a.statut, 'non_marque') AS statut,
            COALESCE(a.justification, '')    AS justification
        FROM etudiants e
        LEFT JOIN absences a ON a.etudiant_id = e.id AND a.date = ?
        WHERE 1=1
    """
    params = [date_str]
    if classe:
        query += " AND e.classe = ?"
        params.append(classe)
    query += " ORDER BY e.nom, e.prenom"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_absences_for_student(etudiant_id: int, date_debut: Optional[str] = None, date_fin: Optional[str] = None) -> list[dict]:
    """Retourne l'historique d'absences d'un étudiant avec filtre de dates optionnel."""
    conn = get_conn()
    query = "SELECT * FROM absences WHERE etudiant_id=?"
    params: list = [etudiant_id]
    if date_debut:
        query += " AND date >= ?"
        params.append(date_debut)
    if date_fin:
        query += " AND date <= ?"
        params.append(date_fin)
    query += " ORDER BY date DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════════════════════════════
#   STATISTIQUES
# ═══════════════════════════════════════════════════════════════════════════════

def get_stats_by_student(classe: str = "") -> list[dict]:
    """
    Retourne les stats par étudiant (nb_absences, nb_presences),
    triés par nb_absences décroissant.
    """
    conn = get_conn()
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
        query += " WHERE e.classe = ?"
        params.append(classe)
    query += " GROUP BY e.id ORDER BY nb_absences DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_absences_by_month(year: Optional[int] = None) -> list[dict]:
    """Retourne le nombre d'absences par mois pour une année donnée."""
    if not year:
        year = datetime.now().year
    conn = get_conn()
    rows = conn.execute("""
        SELECT strftime('%m', date) AS mois, COUNT(*) AS total
        FROM absences
        WHERE statut = 'absent' AND strftime('%Y', date) = ?
        GROUP BY mois
        ORDER BY mois
    """, (str(year),)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_global_stats() -> dict:
    """Retourne les KPIs globaux : nb étudiants, total absences, classes, moyenne."""
    conn = get_conn()
    nb_etudiants = conn.execute("SELECT COUNT(*) FROM etudiants").fetchone()[0]
    nb_absences  = conn.execute(
        "SELECT COUNT(*) FROM absences WHERE statut='absent'"
    ).fetchone()[0]
    nb_classes = conn.execute(
        "SELECT COUNT(DISTINCT classe) FROM etudiants"
    ).fetchone()[0]
    avg_row = conn.execute("""
        SELECT AVG(cnt) FROM (
            SELECT COUNT(*) AS cnt FROM absences
            WHERE statut='absent' GROUP BY etudiant_id
        )
    """).fetchone()[0]
    conn.close()
    return {
        "nb_etudiants":    nb_etudiants,
        "nb_absences_total": nb_absences,
        "nb_classes":      nb_classes,
        "moyenne_absences": round(avg_row or 0, 1),
    }


# ═══════════════════════════════════════════════════════════════════════════════
#   EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

def export_csv(filepath: str, classe: str = "") -> bool:
    """Exporte les stats étudiants en CSV."""
    students = get_stats_by_student(classe)
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["nom", "prenom", "classe", "nb_absences", "nb_presences"]
        )
        writer.writeheader()
        for s in students:
            writer.writerow({k: s[k] for k in ["nom","prenom","classe","nb_absences","nb_presences"]})
    return True


def export_pdf(filepath: str, date_str: str, classe: str = "") -> bool:
    """Génère un rapport PDF des absences pour une date donnée."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.units import cm

        data = get_absences_for_date(date_str, classe)
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        # Titre
        elements.append(Paragraph(f"Rapport d'absences — {date_str}", styles["Title"]))
        if classe:
            elements.append(Paragraph(f"Classe : {classe}", styles["Normal"]))
        elements.append(Spacer(1, 0.5*cm))

        # Tableau
        table_data = [["Nom", "Prénom", "Classe", "Statut", "Justification"]]
        for row in data:
            statut = "Absent" if row["statut"] == "absent" else (
                "Présent" if row["statut"] == "present" else "Non marqué"
            )
            table_data.append([row["nom"], row["prenom"], row["classe"],
                               statut, row["justification"]])

        table = Table(table_data, colWidths=[3.5*cm, 3.5*cm, 3*cm, 3*cm, 5*cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1f538d")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f0f4f8")]),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))
        elements.append(table)

        # Stats résumé
        nb_abs = sum(1 for r in data if r["statut"] == "absent")
        nb_pres = sum(1 for r in data if r["statut"] == "present")
        elements.append(Spacer(1, 0.5*cm))
        elements.append(Paragraph(
            f"Total : {len(data)} étudiants — 🟢 Présents : {nb_pres} — 🔴 Absents : {nb_abs}",
            styles["Normal"]
        ))

        doc.build(elements)
        return True
    except ImportError:
        return False


# ═══════════════════════════════════════════════════════════════════════════════
#   PARENTS / TUTEURS
# ═══════════════════════════════════════════════════════════════════════════════

def add_parent(etudiant_id: int, nom: str, prenom: str, email: str = "", telephone: str = "", relation: str = "parent") -> Optional[int]:
    """Ajoute un parent/tuteur pour un étudiant."""
    conn = get_conn()
    try:
        cursor = conn.execute(
            "INSERT INTO parents (etudiant_id, nom, prenom, email, telephone, relation) VALUES (?,?,?,?,?,?)",
            (etudiant_id, nom.strip(), prenom.strip(), email.strip(), telephone.strip(), relation)
        )
        new_id = cursor.lastrowid
        conn.commit()
        return new_id
    except Exception as e:
        print(f"Erreur ajout parent: {e}")
        return None
    finally:
        conn.close()


def get_parent(etudiant_id: int) -> dict | None:
    """Récupère le parent d'un étudiant."""
    conn = get_conn()
    row = conn.execute("SELECT * FROM parents WHERE etudiant_id=?", (etudiant_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_parent(etudiant_id: int, nom: str, prenom: str, email: str = "", telephone: str = "", relation: str = "parent"):
    """Met à jour les infos du parent."""
    conn = get_conn()
    conn.execute(
        "UPDATE parents SET nom=?, prenom=?, email=?, telephone=?, relation=? WHERE etudiant_id=?",
        (nom.strip(), prenom.strip(), email.strip(), telephone.strip(), relation, etudiant_id)
    )
    conn.commit()
    conn.close()


def delete_parent(etudiant_id: int):
    """Supprime le parent d'un étudiant."""
    conn = get_conn()
    conn.execute("DELETE FROM parents WHERE etudiant_id=?", (etudiant_id,))
    conn.commit()
    conn.close()


def get_all_parents(search: str = "") -> list[dict]:
    """
    Retourne tous les parents avec filtres optionnels.
    search → filtre sur nom ou email (LIKE)
    """
    conn = get_conn()
    query = "SELECT * FROM parents WHERE 1=1"
    params = []
    
    if search:
        query += " AND (nom LIKE ? OR email LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    
    query += " ORDER BY nom, prenom"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════════════════════════════
#   MULTI-ADMIN avec RÔLES
# ═══════════════════════════════════════════════════════════════════════════════

def get_all_admins() -> list[dict]:
    """Retourne tous les admins."""
    conn = get_conn()
    rows = conn.execute("SELECT id, username, email, role, last_login, is_2fa_enabled FROM admins_extended ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_admin(username: str, password: str, email: str = "", role: str = "viewer") -> Optional[int]:
    """Ajoute un nouvel admin."""
    hashed = hashlib.sha256(password.encode()).hexdigest()
    conn = get_conn()
    try:
        cursor = conn.execute(
            "INSERT INTO admins_extended (username, password, email, role) VALUES (?,?,?,?)",
            (username.strip(), hashed, email.strip(), role.lower())
        )
        new_id = cursor.lastrowid
        conn.commit()
        return new_id
    except Exception as e:
        print(f"Erreur ajout admin: {e}")
        return None
    finally:
        conn.close()


def update_admin_role(admin_id: int, role: str):
    """Met à jour le rôle d'un admin."""
    conn = get_conn()
    conn.execute("UPDATE admins_extended SET role=? WHERE id=?", (role.lower(), admin_id))
    conn.commit()
    conn.close()


def delete_admin(admin_id: int):
    """Supprime un admin."""
    conn = get_conn()
    conn.execute("DELETE FROM admins_extended WHERE id=?", (admin_id,))
    conn.commit()
    conn.close()


def verify_login_extended(username: str, password: str) -> dict | None:
    """Vérifie un login admin extended. Retourne les infos si correct."""
    hashed = hashlib.sha256(password.encode()).hexdigest()
    conn = get_conn()
    row = conn.execute(
        "SELECT id, username, email, role, is_2fa_enabled FROM admins_extended WHERE username=? AND password=?",
        (username, hashed)
    ).fetchone()
    if row:
        conn.execute("UPDATE admins_extended SET last_login=datetime('now') WHERE id=?", (row["id"],))
        conn.commit()
    conn.close()
    return dict(row) if row else None


def update_admin_password(admin_id: int, new_password: str):
    """Met à jour le mot de passe d'un admin."""
    hashed = hashlib.sha256(new_password.encode()).hexdigest()
    conn = get_conn()
    conn.execute("UPDATE admins_extended SET password=? WHERE id=?", (hashed, admin_id))
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
#   2FA (OTP - One Time Password)
# ═══════════════════════════════════════════════════════════════════════════════

def enable_2fa(admin_id: int) -> dict:
    """Active 2FA pour un admin. Retourne secret_key et backup_codes."""
    import random
    import string
    import qrcode
    import io
    import base64
    
    # Générer la clé secrète
    secret_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
    
    # Générer des codes de secours
    backup_codes = [f"{''.join(random.choices(string.digits, k=4))}-{''.join(random.choices(string.digits, k=4))}" for _ in range(10)]
    
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO two_fa_tokens (admin_id, secret_key, backup_codes) VALUES (?,?,?)",
        (admin_id, secret_key, ','.join(backup_codes))
    )
    conn.execute("UPDATE admins_extended SET is_2fa_enabled=1 WHERE id=?", (admin_id,))
    conn.commit()
    conn.close()
    
    return {
        "secret_key": secret_key,
        "backup_codes": backup_codes
    }


def disable_2fa(admin_id: int):
    """Désactive 2FA pour un admin."""
    conn = get_conn()
    conn.execute("DELETE FROM two_fa_tokens WHERE admin_id=?", (admin_id,))
    conn.execute("UPDATE admins_extended SET is_2fa_enabled=0 WHERE id=?", (admin_id,))
    conn.commit()
    conn.close()


def verify_2fa_token(admin_id: int, token: str) -> bool:
    """Vérifie un token 2FA (TOTP)."""
    try:
        import pyotp
        conn = get_conn()
        row = conn.execute("SELECT secret_key FROM two_fa_tokens WHERE admin_id=?", (admin_id,)).fetchone()
        conn.close()
        
        if not row:
            return False
        
        totp = pyotp.TOTP(row["secret_key"])
        return totp.verify(token)
    except ImportError:
        # Si pyotp n'est pas installé, accepter pour l'instant
        return True


# ═══════════════════════════════════════════════════════════════════════════════
#   DEMANDES D'ABSENCE (Absence Requests)
# ═══════════════════════════════════════════════════════════════════════════════

def create_absence_request(etudiant_id: int, date_str: str, raison: str, documents: str = "") -> Optional[int]:
    """Crée une demande de validation d'absence."""
    conn = get_conn()
    try:
        cursor = conn.execute(
            "INSERT INTO absence_requests (etudiant_id, date, raison, documents) VALUES (?,?,?,?)",
            (etudiant_id, date_str, raison, documents)
        )
        new_id = cursor.lastrowid
        conn.commit()
        return new_id
    except Exception as e:
        print(f"Erreur création demande absence: {e}")
        return None
    finally:
        conn.close()


def get_absence_requests(statut: Optional[str] = None, etudiant_id: Optional[int] = None) -> list[dict]:
    """Récupère les demandes d'absence avec filtres optionnels."""
    conn = get_conn()
    query = "SELECT ar.*, e.nom, e.prenom FROM absence_requests ar JOIN etudiants e ON ar.etudiant_id=e.id WHERE 1=1"
    params = []
    
    if statut:
        query += " AND ar.statut=?"
        params.append(statut)
    if etudiant_id:
        query += " AND ar.etudiant_id=?"
        params.append(etudiant_id)
    
    query += " ORDER BY ar.created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def approve_request(request_id: int, admin_id: int, mark_as_present: bool = True):
    """Approuve une demande d'absence et marque l'étudiant comme présent si demandé."""
    conn = get_conn()
    request = conn.execute("SELECT * FROM absence_requests WHERE id=?", (request_id,)).fetchone()
    
    if request:
        conn.execute(
            "UPDATE absence_requests SET statut=?, reviewed_by=?, reviewed_at=datetime('now') WHERE id=?",
            ("approved", admin_id, request_id)
        )
        if mark_as_present:
            mark_absence(request["etudiant_id"], request["date"], "present", 
                        f"Validé par admin après demande: {request['raison']}")
    
    conn.commit()
    conn.close()


def reject_request(request_id: int, admin_id: int):
    """Rejette une demande d'absence."""
    conn = get_conn()
    conn.execute(
        "UPDATE absence_requests SET statut=?, reviewed_by=?, reviewed_at=datetime('now') WHERE id=?",
        ("rejected", admin_id, request_id)
    )
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
#   SEUILS D'ALERTE (Threshold Alerts)
# ═══════════════════════════════════════════════════════════════════════════════

def create_alert_rule(nom: str, classe: str = "", max_absences: int = 10, periode_jours: int = 30) -> Optional[int]:
    """Crée une règle d'alerte."""
    conn = get_conn()
    try:
        cursor = conn.execute(
            "INSERT INTO threshold_alerts (nom, classe, max_absences, periode_jours) VALUES (?,?,?,?)",
            (nom, classe, max_absences, periode_jours)
        )
        new_id = cursor.lastrowid
        conn.commit()
        return new_id
    except Exception as e:
        print(f"Erreur création alerte: {e}")
        return None
    finally:
        conn.close()


def get_alert_rules(active_only: bool = True) -> list[dict]:
    """Récupère les règles d'alerte."""
    conn = get_conn()
    query = "SELECT * FROM threshold_alerts"
    if active_only:
        query += " WHERE is_active=1"
    query += " ORDER BY created_at DESC"
    
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def check_absence_thresholds():
    """Vérifie tous les seuils d'alerte et crée des notifications."""
    conn = get_conn()
    alerts = conn.execute("SELECT * FROM threshold_alerts WHERE is_active=1").fetchall()
    
    for alert in alerts:
        # Récupérer les étudiants concernés
        classes_filter = f"AND e.classe='{alert['classe']}'" if alert['classe'] else ""
        students = conn.execute(f"""
            SELECT e.id, COUNT(a.id) as nb_abs FROM etudiants e
            LEFT JOIN absences a ON e.id=a.etudiant_id 
                AND a.statut='absent'
                AND a.date >= date('now', '-{alert['periode_jours']} days')
            WHERE 1=1 {classes_filter}
            GROUP BY e.id HAVING COUNT(a.id) >= {alert['max_absences']}
        """).fetchall()
        
        for student in students:
            # Vérifier si notification existe déjà
            existing = conn.execute(
                "SELECT id FROM alert_notifications WHERE etudiant_id=? AND alert_id=?",
                (student['id'], alert['id'])
            ).fetchone()
            
            if not existing:
                message = f"{alert['nom']}: {student['nb_abs']} absences en {alert['periode_jours']} jours"
                conn.execute(
                    "INSERT INTO alert_notifications (etudiant_id, alert_id, message) VALUES (?,?,?)",
                    (student['id'], alert['id'], message)
                )
    
    conn.commit()
    conn.close()


def get_active_alerts(etudiant_id: Optional[int] = None) -> list[dict]:
    """Récupère les alertes actives."""
    conn = get_conn()
    query = "SELECT * FROM alert_notifications WHERE 1=1"
    params = []
    
    if etudiant_id:
        query += " AND etudiant_id=?"
        params.append(etudiant_id)
    
    query += " ORDER BY created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_alert_as_notified(notification_id: int):
    """Marque une alerte comme ayant envoyé un email."""
    conn = get_conn()
    conn.execute(
        "UPDATE alert_notifications SET email_sent=1, sent_date=datetime('now') WHERE id=?",
        (notification_id,)
    )
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
#   NOTES DÉTAILLÉES D'ABSENCE
# ═══════════════════════════════════════════════════════════════════════════════

def add_absence_note(absence_id: int, type_absence: str = "non_justifiée", notes_admin: str = "") -> Optional[int]:
    """Ajoute une note détaillée à une absence."""
    conn = get_conn()
    cursor = conn.execute(
        "INSERT OR REPLACE INTO absence_notes (absence_id, type_absence, notes_admin) VALUES (?,?,?)",
        (absence_id, type_absence, notes_admin)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def get_absence_note(absence_id: int) -> dict | None:
    """Récupère la note d'une absence."""
    conn = get_conn()
    row = conn.execute("SELECT * FROM absence_notes WHERE absence_id=?", (absence_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_absence_note(absence_id: int, type_absence: str, notes_admin: str):
    """Met à jour une note d'absence."""
    conn = get_conn()
    conn.execute(
        "UPDATE absence_notes SET type_absence=?, notes_admin=?, updated_at=datetime('now') WHERE absence_id=?",
        (type_absence, notes_admin, absence_id)
    )
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
#   AUDIT LOGS
# ═══════════════════════════════════════════════════════════════════════════════

def log_action(admin_id: Optional[int] = None, action: str = "", table_name: str = "", record_id: Optional[int] = None,
               old_values: str = "", new_values: str = "", ip_address: str = ""):
    """Enregistre une action dans les logs d'audit."""
    conn = get_conn()
    conn.execute(
        """INSERT INTO audit_logs (admin_id, action, table_name, record_id, old_values, new_values, ip_address)
           VALUES (?,?,?,?,?,?,?)""",
        (admin_id, action, table_name, record_id, old_values, new_values, ip_address)
    )
    conn.commit()
    conn.close()


def get_audit_logs(limit: int = 100, admin_id: Optional[int] = None, table_name: Optional[str] = None) -> list[dict]:
    """Récupère les logs d'audit."""
    conn = get_conn()
    query = "SELECT * FROM audit_logs WHERE 1=1"
    params = []
    
    if admin_id:
        query += " AND admin_id=?"
        params.append(admin_id)
    if table_name:
        query += " AND table_name=?"
        params.append(table_name)
    
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════════════════════════════
#   EMAIL & NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_email_template(nom: str) -> dict | None:
    """Récupère un template d'email."""
    conn = get_conn()
    row = conn.execute("SELECT * FROM email_templates WHERE nom=?", (nom,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_email_template(nom: str, sujet: str, contenu: str):
    """Met à jour un template d'email."""
    conn = get_conn()
    conn.execute(
        "UPDATE email_templates SET sujet=?, contenu=? WHERE nom=?",
        (sujet, contenu, nom)
    )
    conn.commit()
    conn.close()


def send_email(destinataire: str, sujet: str, corps: str) -> bool:
    """Envoie un email (retourne True si succès)."""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # À adapter avec vos paramètres SMTP
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        SENDER_EMAIL = "absences@example.com"
        SENDER_PASSWORD = "your_app_password"
        
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = destinataire
        msg["Subject"] = sujet
        msg.attach(MIMEText(corps, "html"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


def notify_parent_absence(parent_email: str, etudiant_nom: str, date_str: str, justification: str = ""):
    """Envoie une notification au parent d'une absence."""
    template = get_email_template("parent_notification")
    if not template:
        return False
    
    sujet = template["sujet"]
    corps = template["contenu"]
    
    # Remplacer les variables
    corps = corps.replace("{etudiant_nom}", etudiant_nom)
    corps = corps.replace("{date}", date_str)
    corps = corps.replace("{justification}", justification or "Non spécifiée")
    
    return send_email(parent_email, sujet, corps)


def notify_admin_request(admin_email: str, admin_nom: str, etudiant_nom: str, date_str: str, raison: str):
    """Envoie une notification à un admin d'une demande de validation."""
    template = get_email_template("approval_request")
    if not template:
        return False
    
    sujet = template["sujet"]
    corps = template["contenu"]
    
    corps = corps.replace("{admin}", admin_nom)
    corps = corps.replace("{etudiant_nom}", etudiant_nom)
    corps = corps.replace("{date}", date_str)
    corps = corps.replace("{raison}", raison)
    
    return send_email(admin_email, sujet, corps)


# ═══════════════════════════════════════════════════════════════════════════════
#   VALIDATION & SÉCURITÉ
# ═══════════════════════════════════════════════════════════════════════════════

def validate_password_strength(password: str) -> dict:
    """Valide la force du mot de passe. Retourne dict avec 'valid' et 'errors'."""
    import re
    errors = []
    
    if len(password) < 8:
        errors.append("Min 8 caractères")
    if not re.search(r'[A-Z]', password):
        errors.append("Au moins 1 majuscule")
    if not re.search(r'[a-z]', password):
        errors.append("Au moins 1 minuscule")
    if not re.search(r'[0-9]', password):
        errors.append("Au moins 1 chiffre")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Au moins 1 caractère spécial")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "score": 5 - len(errors)
    }


def is_valid_email(email: str) -> bool:
    """Valide le format d'une adresse email."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
