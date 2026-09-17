from app.database.connection import get_connection
from app.database.lead_repository import create_lead


def cleanup_database():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM leads;")

        connection.commit()

    finally:
        connection.close()


def test_create_lead():
    cleanup_database()

    lead = create_lead(
        service="electrician",
        location="Kozhikode",
        urgency="tomorrow",
        problem="wiring problem",
        budget=None,
        customer_intent="service_request",
        lead_priority="high",
    )

    assert lead is not None
    assert lead[0] is not None
    assert lead[1] == "electrician"
    assert lead[2] == "Kozhikode"
    assert lead[3] == "tomorrow"
    assert lead[4] == "wiring problem"
    assert lead[5] is None
    assert lead[6] == "service_request"
    assert lead[7] == "high"
    assert lead[8] == "NEW"
    assert lead[9] is not None

    cleanup_database()