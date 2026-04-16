"""
database.py — Couche base de données
Responsable de : connexion SQLite, création des tables, données initiales.
"""

import sqlite3
import hashlib

DB_PATH = "absences.db"


def get_conn() -> sqlite3.Connection:
    """Retourne une connexion SQLite avec row_factory (accès par nom de colonne)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")   # cascade suppression activée
    return conn


def init_db():
    """Crée les tables si elles n'existent pas + admin par défaut."""
    conn = get_conn()
    c = conn.cursor()

    # ── Table étudiants ──────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS etudiants (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nom         TEXT    NOT NULL,
            prenom      TEXT    NOT NULL,
            classe      TEXT    NOT NULL,
            email       TEXT    DEFAULT '',
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    # ── Table absences ───────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS absences (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            etudiant_id   INTEGER NOT NULL,
            date          TEXT    NOT NULL,
            statut        TEXT    NOT NULL CHECK(statut IN ('absent','present')),
            justification TEXT    DEFAULT '',
            FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE
        )
    """)

    # ── Table admin ──────────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email    TEXT DEFAULT ''
        )
    """)

    # ── Table parents (NEW) ──────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS parents (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            etudiant_id   INTEGER NOT NULL UNIQUE,
            nom           TEXT    NOT NULL,
            prenom        TEXT    NOT NULL,
            email         TEXT    DEFAULT '',
            telephone     TEXT    DEFAULT '',
            relation      TEXT    DEFAULT 'parent',
            created_at    TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE
        )
    """)

    # ── Table admins_extended (multi-admin avec rôles) ────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS admins_extended (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    NOT NULL UNIQUE,
            password      TEXT    NOT NULL,
            email         TEXT    DEFAULT '',
            role          TEXT    NOT NULL DEFAULT 'viewer' CHECK(role IN ('admin','editor','viewer')),
            last_login    TEXT    DEFAULT NULL,
            created_at    TEXT    DEFAULT (datetime('now')),
            is_2fa_enabled INTEGER DEFAULT 0
        )
    """)

    # ── Table two_fa_tokens (2FA) ────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS two_fa_tokens (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id    INTEGER NOT NULL UNIQUE,
            secret_key  TEXT    NOT NULL,
            backup_codes TEXT DEFAULT '',
            created_at  TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (admin_id) REFERENCES admins_extended(id) ON DELETE CASCADE
        )
    """)

    # ── Table absence_requests (demandes de validation) ──────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS absence_requests (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            etudiant_id    INTEGER NOT NULL,
            date           TEXT    NOT NULL,
            raison         TEXT    NOT NULL,
            documents      TEXT    DEFAULT '',
            statut         TEXT    NOT NULL DEFAULT 'pending' CHECK(statut IN ('pending','approved','rejected')),
            reviewed_by    INTEGER DEFAULT NULL,
            reviewed_at    TEXT    DEFAULT NULL,
            created_at     TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE,
            FOREIGN KEY (reviewed_by) REFERENCES admins_extended(id)
        )
    """)

    # ── Table threshold_alerts (règles d'alerte) ─────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS threshold_alerts (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nom             TEXT    NOT NULL,
            classe          TEXT    DEFAULT '',
            max_absences    INTEGER NOT NULL DEFAULT 10,
            periode_jours   INTEGER NOT NULL DEFAULT 30,
            is_active       INTEGER DEFAULT 1,
            created_at      TEXT    DEFAULT (datetime('now'))
        )
    """)

    # ── Table alert_notifications (notifications d'alerte) ────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS alert_notifications (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            etudiant_id     INTEGER NOT NULL,
            alert_id        INTEGER NOT NULL,
            message         TEXT    NOT NULL,
            email_sent      INTEGER DEFAULT 0,
            sent_date       TEXT    DEFAULT NULL,
            created_at      TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE,
            FOREIGN KEY (alert_id) REFERENCES threshold_alerts(id) ON DELETE CASCADE
        )
    """)

    # ── Table absence_notes (notes détaillées) ───────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS absence_notes (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            absence_id    INTEGER NOT NULL UNIQUE,
            type_absence  TEXT    DEFAULT 'non_justifiée',
            notes_admin   TEXT    DEFAULT '',
            created_at    TEXT    DEFAULT (datetime('now')),
            updated_at    TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (absence_id) REFERENCES absences(id) ON DELETE CASCADE
        )
    """)

    # ── Table audit_logs (journaux d'audit) ──────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id    INTEGER DEFAULT NULL,
            action      TEXT    NOT NULL,
            table_name  TEXT    NOT NULL,
            record_id   INTEGER DEFAULT NULL,
            old_values  TEXT    DEFAULT '',
            new_values  TEXT    DEFAULT '',
            ip_address  TEXT    DEFAULT '',
            timestamp   TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (admin_id) REFERENCES admins_extended(id) ON DELETE SET NULL
        )
    """)

    # ── Table email_templates (templates d'email) ────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS email_templates (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nom         TEXT    NOT NULL UNIQUE,
            sujet       TEXT    NOT NULL,
            contenu     TEXT    NOT NULL,
            variables   TEXT    DEFAULT '',
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    # Admin par défaut : admin / admin123 (créé seulement si vide)
    if c.execute("SELECT COUNT(*) FROM admin").fetchone()[0] == 0:
        hashed = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO admin (username, password) VALUES ('admin', ?)", (hashed,))

    # Créer un premier admin extended aussi
    if c.execute("SELECT COUNT(*) FROM admins_extended").fetchone()[0] == 0:
        hashed = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO admins_extended (username, password, email, role) VALUES (?, ?, ?, ?)",
                  ("admin", hashed, "admin@absencespro.local", "admin"))

    # Templates d'email par défaut
    default_templates = [
        ("alert_absence", "Alerte : Absences élevées de {etudiant_nom}", 
         "Bonjour,\n\nL'étudiant {etudiant_nom} a dépassé le seuil d'absences ({nb_absences} absences en {periode} jours).\n\nCordialement"),
        ("approval_request", "Demande de validation d'absence",
         "Bonjour {admin},\n\nL'étudiant {etudiant_nom} a demandé la validation d'une absence du {date}.\nRaison: {raison}\n\nVeuillez examiner sa demande."),
        ("parent_notification", "Notification d'absence",
         "Bonjour,\n\nVotre enfant {etudiant_nom} a été marqué absent le {date}.\n\nJustification: {justification}\n\nCordialement"),
    ]
    for nom, sujet, contenu in default_templates:
        if not c.execute("SELECT id FROM email_templates WHERE nom=?", (nom,)).fetchone():
            c.execute("INSERT INTO email_templates (nom, sujet, contenu) VALUES (?,?,?)",
                      (nom, sujet, contenu))

    conn.commit()
    conn.close()
    print("[DB] Base de données initialisée avec toutes les tables.")
