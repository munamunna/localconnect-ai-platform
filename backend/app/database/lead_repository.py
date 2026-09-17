from app.database.connection import get_connection


def create_lead(
    service: str | None = None,
    location: str | None = None,
    urgency: str | None = None,
    problem: str | None = None,
    budget: str | None = None,
    customer_intent: str | None = None,
    lead_priority: str | None = None,
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO leads
                    (
                        service,
                        location,
                        urgency,
                        problem,
                        budget,
                        customer_intent,
                        lead_priority
                    )
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
                RETURNING
                    id,
                    service,
                    location,
                    urgency,
                    problem,
                    budget,
                    customer_intent,
                    lead_priority,
                    status,
                    created_at;
                """,
                (
                    service,
                    location,
                    urgency,
                    problem,
                    budget,
                    customer_intent,
                    lead_priority,
                ),
            )

            lead = cursor.fetchone()

        connection.commit()

        return lead

    finally:
        connection.close()