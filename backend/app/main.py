from fastapi import FastAPI, HTTPException

from app.database import get_connection


app = FastAPI(
    title="Telecom Traffic Monitor API",
    description="API de surveillance et d'analyse de la consommation télécom.",
    version="1.0.0"
)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Telecom Traffic Monitor API"
    }


@app.get("/api/abonnes")
def get_abonnes():

    query = """
        SELECT
            ab.id,
            ab.numero,
            ab.nom,
            ab.forfait_quota_mb,

            COALESCE(SUM(sc.volume_mb), 0) AS consommation_totale,

            ab.forfait_quota_mb -
            COALESCE(SUM(sc.volume_mb), 0) AS volume_restant

        FROM abonnes ab

        LEFT JOIN sessions_consommation sc
            ON ab.id = sc.abonne_id

        GROUP BY
            ab.id,
            ab.numero,
            ab.nom,
            ab.forfait_quota_mb

        ORDER BY ab.id;
    """

    with get_connection() as conn:
        abonnes = conn.execute(query).fetchall()

    return abonnes

@app.get("/api/abonnes/{abonne_id}")
def get_abonne(abonne_id: int):

    query = """
        SELECT
            ab.id,
            ab.numero,
            ab.nom,
            ab.forfait_quota_mb,
            COALESCE(SUM(sc.volume_mb), 0) AS consommation_totale,
            ab.forfait_quota_mb - COALESCE(SUM(sc.volume_mb), 0) AS volume_restant

        FROM abonnes ab

        LEFT JOIN sessions_consommation sc
            ON ab.id = sc.abonne_id

        WHERE ab.id = %s

        GROUP BY
            ab.id,
            ab.numero,
            ab.nom,
            ab.forfait_quota_mb;
    """

    with get_connection() as conn:
        abonne = conn.execute(query, (abonne_id,)).fetchone()

    if abonne is None:
        raise HTTPException(status_code=404, detail="Abonné introuvable")

    return abonne

@app.get("/api/statistiques/applications/{numero}")
def get_statistiques_applications(numero: str):

    query = """
        SELECT
            ap.nom,
            SUM(sc.volume_mb) AS consommation_totale

        FROM sessions_consommation sc

        JOIN abonnes ab
            ON sc.abonne_id = ab.id

        JOIN applications ap
            ON sc.application_id = ap.id

        WHERE ab.numero = %s

        GROUP BY
            ap.id,
            ap.nom

        ORDER BY consommation_totale DESC;
    """

    with get_connection() as conn:

        # Vérifier l'existence de l'abonné
        abonne = conn.execute(
            "SELECT id FROM abonnes WHERE numero = %s",
            (numero,)
        ).fetchone()

        if abonne is None:
            raise HTTPException(
                status_code=404,
                detail="Abonné introuvable"
            )

        # Récupérer les statistiques
        statistiques = conn.execute(
            query,
            (numero,)
        ).fetchall()

    return statistiques

@app.get("/api/statistiques/protocoles/{numero}")
def get_statistiques_protocoles(numero: str):

    query = """
        SELECT
            p.nom,
            SUM(sc.volume_mb) AS consommation_totale

        FROM sessions_consommation sc

        JOIN abonnes ab
            ON ab.id = sc.abonne_id

        JOIN protocoles p
            ON p.id = sc.protocole_id

        WHERE ab.numero = %s

        GROUP BY
            p.nom,
            p.id

        ORDER BY consommation_totale DESC;
    """

    with get_connection() as conn:

        # Vérifier l'existence de l'abonné
        abonne = conn.execute(
            "SELECT id FROM abonnes WHERE numero = %s",
            (numero,)
        ).fetchone()

        if abonne is None:
            raise HTTPException(
                status_code=404,
                detail="Abonné introuvable"
            )

        # Récupérer les statistiques
        statistiques = conn.execute(
            query,
            (numero,)
        ).fetchall()

    return statistiques



@app.get("/api/consommation/{numero}")
def get_statistiques_synthese(numero: str):

    query = """
        SELECT
    ab.numero,
    ab.nom,
    ab.forfait_quota_mb,

    COALESCE(SUM(sc.volume_mb), 0) AS consommation_totale,

    ab.forfait_quota_mb -
    COALESCE(SUM(sc.volume_mb), 0) AS volume_restant,

    ROUND(
        (
            COALESCE(SUM(sc.volume_mb), 0)
            / NULLIF(ab.forfait_quota_mb, 0)
        ) * 100,
        2
    ) AS taux_de_consommation

FROM abonnes ab

LEFT JOIN sessions_consommation sc
    ON ab.id = sc.abonne_id

WHERE ab.numero = %s

GROUP BY
    ab.id,
    ab.numero,
    ab.nom,
    ab.forfait_quota_mb;   
    """
    with get_connection() as conn:
        statistiques = conn.execute(query, (numero,)).fetchall()

    if not statistiques:
        raise HTTPException(
            status_code=404,
            detail="Abonné introuvable"
        )

    return statistiques
