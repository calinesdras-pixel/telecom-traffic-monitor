from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app


client = TestClient(app)

def test_statistiques_applications():

    with patch("app.main.get_connection") as mock_connection:

        mock_conn = mock_connection.return_value.__enter__.return_value

        mock_cursor = MagicMock()

        mock_conn.execute.return_value = mock_cursor

        # Simuler l'existence de l'abonné
        mock_cursor.fetchone.return_value = {"id": 2}

        # Simuler ses statistiques
        mock_cursor.fetchall.return_value = [
            {"nom": "YouTube", "consommation_totale": 850.0},
            {"nom": "Instagram", "consommation_totale": 340.0}
        ]

        response = client.get("/api/statistiques/applications/0740000002")

        assert response.status_code == 200

        assert response.json() == [
            {"nom": "YouTube", "consommation_totale": 850.0},
            {"nom": "Instagram", "consommation_totale": 340.0}
        ]

def test_applications_sans_consommation():

    with patch("app.main.get_connection") as mock_connection:

        mock_conn = mock_connection.return_value.__enter__.return_value

        mock_cursor = MagicMock()

        mock_conn.execute.return_value = mock_cursor

        # L'abonné existe
        mock_cursor.fetchone.return_value = {"id": 4}

        # Aucune consommation enregistrée
        mock_cursor.fetchall.return_value = []

        response = client.get("/api/statistiques/applications/0740000004")

        assert response.status_code == 200
        assert response.json() == []

def test_applications_abonne_inexistant():

    with patch("app.main.get_connection") as mock_connection:

        mock_conn = mock_connection.return_value.__enter__.return_value

        mock_cursor = MagicMock()

        mock_conn.execute.return_value = mock_cursor

        # Aucun abonné trouvé
        mock_cursor.fetchone.return_value = None

        response = client.get("/api/statistiques/applications/079999999999")

        assert response.status_code == 404

        assert response.json() == {
            "detail": "Abonné introuvable"
        }

def test_statistiques_protocoles():

    with patch("app.main.get_connection") as mock_connection:

        mock_conn = mock_connection.return_value.__enter__.return_value

        mock_cursor = MagicMock()

        mock_conn.execute.return_value = mock_cursor

        # Simuler l'existence de l'abonné
        mock_cursor.fetchone.return_value = {"id": 2}

        # Simuler ses statistiques par protocole
        mock_cursor.fetchall.return_value = [
            {"nom": "QUIC", "consommation_totale": 850.0},
            {"nom": "TCP", "consommation_totale": 415.5}
        ]

        response = client.get("/api/statistiques/protocoles/0740000002")

        assert response.status_code == 200

        assert response.json() == [
            {"nom": "QUIC", "consommation_totale": 850.0},
            {"nom": "TCP", "consommation_totale": 415.5}
        ]

def test_protocoles_sans_consommation():

    with patch("app.main.get_connection") as mock_connection:

        mock_conn = mock_connection.return_value.__enter__.return_value

        mock_cursor = MagicMock()

        mock_conn.execute.return_value = mock_cursor

        # L'abonné existe
        mock_cursor.fetchone.return_value = {"id": 4}

        # Aucune consommation enregistrée
        mock_cursor.fetchall.return_value = []

        response = client.get("/api/statistiques/protocoles/0740000004")

        assert response.status_code == 200
        assert response.json() == []

def test_protocoles_abonne_inexistant():

    with patch("app.main.get_connection") as mock_connection:

        mock_conn = mock_connection.return_value.__enter__.return_value

        mock_cursor = MagicMock()

        mock_conn.execute.return_value = mock_cursor

        # Aucun abonné trouvé
        mock_cursor.fetchone.return_value = None

        response = client.get("/api/statistiques/protocoles/079999999999")

        assert response.status_code == 404

        assert response.json() == {
            "detail": "Abonné introuvable"
        }

def test_consommation_abonne():

    with patch("app.main.get_connection") as mock_connection:

        mock_conn = mock_connection.return_value.__enter__.return_value

        mock_cursor = MagicMock()

        mock_conn.execute.return_value = mock_cursor

        # Simuler les informations de consommation
        mock_cursor.fetchall.return_value = [
            {
                "numero": "0740000002",
                "nom": "Sarah Mba",
                "forfait_quota_mb": 5120.0,
                "consommation_totale": 1265.5,
                "volume_restant": 3854.5,
                "taux_de_consommation": 24.72
            }
        ]

        response = client.get("/api/consommation/0740000002")

        assert response.status_code == 200

        assert response.json() == [
            {
                "numero": "0740000002",
                "nom": "Sarah Mba",
                "forfait_quota_mb": 5120.0,
                "consommation_totale": 1265.5,
                "volume_restant": 3854.5,
                "taux_de_consommation": 24.72
            }
        ]

def test_consommation_nulle():

    with patch("app.main.get_connection") as mock_connection:

        mock_conn = mock_connection.return_value.__enter__.return_value

        mock_cursor = MagicMock()

        mock_conn.execute.return_value = mock_cursor

        # Abonné avec un forfait, mais aucune consommation
        mock_cursor.fetchall.return_value = [
            {
                "numero": "0740000004",
                "nom": "Azaria",
                "forfait_quota_mb": 2048.0,
                "consommation_totale": 0.0,
                "volume_restant": 2048.0,
                "taux_de_consommation": 0.0
            }
        ]

        response = client.get("/api/consommation/0740000004")

        assert response.status_code == 200

        assert response.json() == [
            {
                "numero": "0740000004",
                "nom": "Azaria",
                "forfait_quota_mb": 2048.0,
                "consommation_totale": 0.0,
                "volume_restant": 2048.0,
                "taux_de_consommation": 0.0
            }
        ]

def test_consommation_abonne_inexistant():

    with patch("app.main.get_connection") as mock_connection:

        mock_conn = mock_connection.return_value.__enter__.return_value

        mock_cursor = MagicMock()

        mock_conn.execute.return_value = mock_cursor

        # Aucun résultat : l'abonné n'existe pas
        mock_cursor.fetchall.return_value = []

        response = client.get("/api/consommation/079999999999")

        assert response.status_code == 404

        assert response.json() == {
            "detail": "Abonné introuvable"
        }

def test_health_check():

    response = client.get("/api/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy",
        "application": "Telecom Traffic Monitor API"
    }

def test_liste_abonnes():

    with patch("app.main.get_connection") as mock_connection:

        mock_conn = mock_connection.return_value.__enter__.return_value

        mock_cursor = MagicMock()

        mock_conn.execute.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            {
                "id": 2,
                "numero": "0740000002",
                "nom": "Sarah Mba",
                "forfait_quota_mb": 5120.0,
                "consommation_totale": 1265.5,
                "volume_restant": 3854.5
            },
            {
                "id": 4,
                "numero": "0740000004",
                "nom": "Azaria",
                "forfait_quota_mb": 2048.0,
                "consommation_totale": 0.0,
                "volume_restant": 2048.0
            }
        ]

        response = client.get("/api/abonnes")

        assert response.status_code == 200

        assert response.json() == [
            {
                "id": 2,
                "numero": "0740000002",
                "nom": "Sarah Mba",
                "forfait_quota_mb": 5120.0,
                "consommation_totale": 1265.5,
                "volume_restant": 3854.5
            },
            {
                "id": 4,
                "numero": "0740000004",
                "nom": "Azaria",
                "forfait_quota_mb": 2048.0,
                "consommation_totale": 0.0,
                "volume_restant": 2048.0
            }
        ]

def test_recuperer_abonne():

    with patch("app.main.get_connection") as mock_connection:

        mock_conn = mock_connection.return_value.__enter__.return_value

        mock_cursor = MagicMock()

        mock_conn.execute.return_value = mock_cursor

        mock_cursor.fetchone.return_value = {
            "id": 2,
            "numero": "0740000002",
            "nom": "Sarah Mba",
            "forfait_quota_mb": 5120.0,
            "consommation_totale": 1265.5,
            "volume_restant": 3854.5
        }

        response = client.get("/api/abonnes/2")

        assert response.status_code == 200

        assert response.json() == {
            "id": 2,
            "numero": "0740000002",
            "nom": "Sarah Mba",
            "forfait_quota_mb": 5120.0,
            "consommation_totale": 1265.5,
            "volume_restant": 3854.5
        }

def test_recuperer_abonne_inexistant():

    with patch("app.main.get_connection") as mock_connection:

        mock_conn = mock_connection.return_value.__enter__.return_value

        mock_cursor = MagicMock()

        mock_conn.execute.return_value = mock_cursor

        # Aucun abonné trouvé
        mock_cursor.fetchone.return_value = None

        response = client.get("/api/abonnes/9999")

        assert response.status_code == 404

        assert response.json() == {
            "detail": "Abonné introuvable"
        }