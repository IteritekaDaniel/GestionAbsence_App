-- ═════════════════════════════════════════════════════════════════════════════════
-- AbsencesPro v2.0 — Script SQL MySQL Complet
-- Base de données pour système de gestion des absences
-- ═════════════════════════════════════════════════════════════════════════════════

-- Créer la base de données
CREATE DATABASE IF NOT EXISTS gestion_absences;
USE gestion_absences;

-- ═════════════════════════════════════════════════════════════════════════════════
-- TABLE 1: ETUDIANTS
-- ═════════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS etudiants (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    classe VARCHAR(50) NOT NULL,
    email VARCHAR(150) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_classe (classe),
    INDEX idx_nom (nom, prenom)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════════════
-- TABLE 2: ABSENCES
-- ═════════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS absences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    etudiant_id INT NOT NULL,
    date DATE NOT NULL,
    statut ENUM('absent', 'present') NOT NULL,
    justification TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE,
    UNIQUE KEY unique_absence (etudiant_id, date),
    INDEX idx_date (date),
    INDEX idx_statut (statut)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════════════
-- TABLE 3: ADMIN (Legacy - Compatibilité)
-- ═════════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(150) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════════════
-- TABLE 4: PARENTS
-- ═════════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS parents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    etudiant_id INT NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) DEFAULT '',
    telephone VARCHAR(20) DEFAULT '',
    relation VARCHAR(50) DEFAULT 'parent',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════════════
-- TABLE 5: ADMINS_EXTENDED (Multi-admin avec rôles)
-- ═════════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS admins_extended (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(150) DEFAULT '',
    role ENUM('admin', 'editor', 'viewer') NOT NULL DEFAULT 'viewer',
    last_login DATETIME DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_2fa_enabled TINYINT(1) DEFAULT 0,
    INDEX idx_username (username),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════════════
-- TABLE 6: TWO_FA_TOKENS (2FA - TOTP secrets)
-- ═════════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS two_fa_tokens (
    id INT PRIMARY KEY AUTO_INCREMENT,
    admin_id INT NOT NULL UNIQUE,
    secret_key VARCHAR(255) NOT NULL,
    backup_codes LONGTEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins_extended(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════════════
-- TABLE 7: ABSENCE_REQUESTS (Demandes de validation)
-- ═════════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS absence_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    etudiant_id INT NOT NULL,
    date DATE NOT NULL,
    raison TEXT NOT NULL,
    documents LONGTEXT DEFAULT '',
    statut ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
    reviewed_by INT DEFAULT NULL,
    reviewed_at DATETIME DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES admins_extended(id) ON DELETE SET NULL,
    INDEX idx_statut (statut),
    INDEX idx_etudiant (etudiant_id),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════════════
-- TABLE 8: THRESHOLD_ALERTS (Règles d'alerte)
-- ═════════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS threshold_alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(150) NOT NULL,
    classe VARCHAR(50) DEFAULT '',
    max_absences INT NOT NULL DEFAULT 10,
    periode_jours INT NOT NULL DEFAULT 30,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_active (is_active),
    INDEX idx_classe (classe)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════════════
-- TABLE 9: ALERT_NOTIFICATIONS (Alertes actives)
-- ═════════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS alert_notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    etudiant_id INT NOT NULL,
    alert_id INT NOT NULL,
    message TEXT NOT NULL,
    email_sent TINYINT(1) DEFAULT 0,
    sent_date DATETIME DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE,
    FOREIGN KEY (alert_id) REFERENCES threshold_alerts(id) ON DELETE CASCADE,
    INDEX idx_etudiant (etudiant_id),
    INDEX idx_email_sent (email_sent)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════════════
-- TABLE 10: ABSENCE_NOTES (Notes détaillées)
-- ═════════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS absence_notes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    absence_id INT NOT NULL UNIQUE,
    type_absence VARCHAR(100) DEFAULT 'non_justifiée',
    notes_admin TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (absence_id) REFERENCES absences(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════════════
-- TABLE 11: AUDIT_LOGS (Journaux d'audit)
-- ═════════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    admin_id INT DEFAULT NULL,
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    record_id INT DEFAULT NULL,
    old_values LONGTEXT DEFAULT '',
    new_values LONGTEXT DEFAULT '',
    ip_address VARCHAR(45) DEFAULT '',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins_extended(id) ON DELETE SET NULL,
    INDEX idx_timestamp (timestamp),
    INDEX idx_action (action),
    INDEX idx_table (table_name),
    INDEX idx_admin (admin_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════════════
-- TABLE 12: EMAIL_TEMPLATES (Templates d'email)
-- ═════════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS email_templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL UNIQUE,
    sujet VARCHAR(255) NOT NULL,
    contenu LONGTEXT NOT NULL,
    variables VARCHAR(500) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═════════════════════════════════════════════════════════════════════════════════
-- DONNÉES INITIALES
-- ═════════════════════════════════════════════════════════════════════════════════

-- Admin par défaut (admin / admin123)
INSERT INTO admin (username, password, email) VALUES 
('admin', SHA2('admin123', 256), 'admin@absencespro.local');

-- Admin extended (multi-admin avec rôles)
INSERT INTO admins_extended (username, password, email, role) VALUES 
('admin', SHA2('admin123', 256), 'admin@absencespro.local', 'admin');

-- Templates d'email par défaut
INSERT INTO email_templates (nom, sujet, contenu) VALUES 
(
    'alert_absence',
    'Alerte : Absences élevées de {etudiant_nom}',
    'Bonjour,\n\nL''étudiant {etudiant_nom} a dépassé le seuil d''absences ({nb_absences} absences en {periode} jours).\n\nVeuillez prendre les mesures nécessaires.\n\nCordialement,\nAbsencesPro'
),
(
    'approval_request',
    'Demande de validation d''absence',
    'Bonjour {admin},\n\nL''étudiant {etudiant_nom} a demandé la validation d''une absence du {date}.\n\nRaison: {raison}\n\nVeuillez examiner sa demande dans la section "Demandes".\n\nCordialement'
),
(
    'parent_notification',
    'Notification d''absence - {etudiant_nom}',
    'Bonjour,\n\nVotre enfant {etudiant_nom} a été marqué absent le {date}.\n\nJustification: {justification}\n\nSi vous avez des questions, n''hésitez pas à contacter l''établissement.\n\nCordialement'
);

-- ═════════════════════════════════════════════════════════════════════════════════
-- VUES UTILES (OPTIONNEL)
-- ═════════════════════════════════════════════════════════════════════════════════

-- Vue: Statistiques par étudiant
CREATE OR REPLACE VIEW v_stats_etudiants AS
SELECT
    e.id,
    e.nom,
    e.prenom,
    e.classe,
    COUNT(CASE WHEN a.statut='absent' THEN 1 END) AS nb_absences,
    COUNT(CASE WHEN a.statut='present' THEN 1 END) AS nb_presences,
    COUNT(a.id) AS total_marques
FROM etudiants e
LEFT JOIN absences a ON e.id = a.etudiant_id
GROUP BY e.id, e.nom, e.prenom, e.classe
ORDER BY nb_absences DESC;

-- Vue: Alertes actives avec détails
CREATE OR REPLACE VIEW v_alertes_actives AS
SELECT
    an.id,
    e.id AS etudiant_id,
    CONCAT(e.nom, ' ', e.prenom) AS etudiant_nom,
    e.classe,
    an.message,
    ta.nom AS alert_rule,
    an.email_sent,
    an.created_at
FROM alert_notifications an
JOIN etudiants e ON an.etudiant_id = e.id
JOIN threshold_alerts ta ON an.alert_id = ta.id
ORDER BY an.created_at DESC;

-- Vue: Demandes en attente
CREATE OR REPLACE VIEW v_demandes_en_attente AS
SELECT
    ar.id,
    CONCAT(e.nom, ' ', e.prenom) AS etudiant,
    e.classe,
    ar.date,
    ar.raison,
    ar.created_at,
    'pending' AS statut
FROM absence_requests ar
JOIN etudiants e ON ar.etudiant_id = e.id
WHERE ar.statut = 'pending'
ORDER BY ar.created_at ASC;

-- ═════════════════════════════════════════════════════════════════════════════════
-- UTILITAIRES
-- ═════════════════════════════════════════════════════════════════════════════════

-- Stocker pour obtenir les stats globales
DELIMITER $$

CREATE PROCEDURE sp_stats_globales()
BEGIN
    SELECT
        (SELECT COUNT(*) FROM etudiants) AS nb_etudiants,
        (SELECT COUNT(*) FROM absences WHERE statut='absent') AS nb_absences_total,
        (SELECT COUNT(DISTINCT classe) FROM etudiants) AS nb_classes,
        ROUND(
            (SELECT AVG(cnt) FROM (
                SELECT COUNT(*) AS cnt FROM absences
                WHERE statut='absent'
                GROUP BY etudiant_id
            ) t), 1
        ) AS moyenne_absences;
END$$

DELIMITER ;

-- Procédure pour vérifier les seuils d'alerte
DELIMITER $$

CREATE PROCEDURE sp_check_thresholds()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_alert_id INT;
    DECLARE v_classe VARCHAR(50);
    DECLARE v_max_absences INT;
    DECLARE v_periode_jours INT;
    
    DECLARE alert_cursor CURSOR FOR
        SELECT id, classe, max_absences, periode_jours
        FROM threshold_alerts
        WHERE is_active = 1;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    OPEN alert_cursor;
    
    read_loop: LOOP
        FETCH alert_cursor INTO v_alert_id, v_classe, v_max_absences, v_periode_jours;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Insérer les alertes pour certains seuils
        INSERT IGNORE INTO alert_notifications (etudiant_id, alert_id, message)
        SELECT
            e.id,
            v_alert_id,
            CONCAT('Alerte: ', COUNT(*), ' absences en ', v_periode_jours, ' jours')
        FROM etudiants e
        LEFT JOIN absences a ON e.id = a.etudiant_id
            AND a.statut = 'absent'
            AND a.date >= DATE_SUB(CURDATE(), INTERVAL v_periode_jours DAY)
        WHERE (v_classe = '' OR e.classe = v_classe)
        GROUP BY e.id
        HAVING COUNT(*) >= v_max_absences;
        
    END LOOP;
    
    CLOSE alert_cursor;
END$$

DELIMITER ;

-- ═════════════════════════════════════════════════════════════════════════════════
-- Fin du script
-- ═════════════════════════════════════════════════════════════════════════════════

-- Afficher le résumé
SELECT '✅ Base de données AbsencesPro créée avec succès!' AS status;
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'gestion_absences' ORDER BY TABLE_NAME;
