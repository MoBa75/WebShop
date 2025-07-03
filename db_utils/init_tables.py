from datamanager.database import engine
from datamanager.models import Base


def init_db():
    """
    Reinitialisiert die Datenbank:
    - Löscht alle vorhandenen Tabellen.
    - Erstellt alle Tabellen basierend auf den SQLAlchemy-Modellen neu.

    Diese Methode eignet sich für Entwicklungs- und Testumgebungen,
    in denen ein frischer Datenbankzustand gewünscht ist.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    # Führt die Datenbank-Initialisierung aus, wenn dieses Skript direkt gestartet wird
    init_db()
