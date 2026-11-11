-- ==========================================
-- 1. INSERTION DES ABONNES
-- ==========================================

INSERT INTO abonnes (numero, nom, forfait_quota_mb)
VALUES
    ('0740000001', 'Jean Mbala', 10240),
    ('0740000002', 'Sarah Mba', 5120),
    ('0740000003', 'David Nguema', 20480)
ON CONFLICT (numero) DO NOTHING;


-- ==========================================
-- 2. INSERTION DES APPLICATIONS
-- ==========================================

INSERT INTO applications (nom)
VALUES
    ('YouTube'),
    ('WhatsApp'),
    ('TikTok'),
    ('Instagram'),
    ('Chrome')
ON CONFLICT (nom) DO NOTHING;


-- ==========================================
-- 3. INSERTION DES PROTOCOLES
-- ==========================================

INSERT INTO protocoles (nom)
VALUES
    ('TCP'),
    ('UDP'),
    ('QUIC')
ON CONFLICT (nom) DO NOTHING;


-- ==========================================
-- 4. INSERTION DES SESSIONS
-- ==========================================

INSERT INTO sessions_consommation
    (abonne_id, application_id, protocole_id, volume_mb)

SELECT
    ab.id,
    app.id,
    p.id,
    data.volume_mb

FROM (
    VALUES
        ('0740000001', 'YouTube',   'QUIC', 450.50),
        ('0740000001', 'WhatsApp',  'TCP',  120.00),
        ('0740000001', 'TikTok',    'QUIC', 780.25),
        ('0740000001', 'Instagram', 'TCP',  230.75),
        ('0740000001', 'Chrome',    'TCP',   90.00),

        ('0740000002', 'YouTube',   'QUIC', 850.00),
        ('0740000002', 'WhatsApp',  'TCP',   75.50),
        ('0740000002', 'Instagram', 'TCP',  340.00),

        ('0740000003', 'YouTube',   'QUIC', 1250.00),
        ('0740000003', 'TikTok',    'QUIC', 920.00),
        ('0740000003', 'Chrome',    'TCP',  180.50)

) AS data(numero_abonne, nom_application, nom_protocole, volume_mb)

JOIN abonnes ab
    ON ab.numero = data.numero_abonne

JOIN applications app
    ON app.nom = data.nom_application

JOIN protocoles p
    ON p.nom = data.nom_protocole

WHERE NOT EXISTS (
    SELECT 1
    FROM sessions_consommation
);
