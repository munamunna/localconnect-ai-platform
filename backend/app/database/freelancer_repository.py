from app.database.connection import get_connection


def create_freelancer(
    name: str,
    service: str,
    location: str,
    phone: str | None = None,
    verified: bool = False,
    available: bool = True,
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO freelancers
                    (name, service, location, phone, verified, available)
                VALUES
                    (%s, %s, %s, %s, %s, %s)
                RETURNING
                    id,
                    name,
                    service,
                    location,
                    phone,
                    verified,
                    available,
                    created_at;
                """,
                (
                    name,
                    service,
                    location,
                    phone,
                    verified,
                    available,
                ),
            )

            freelancer = cursor.fetchone()

        connection.commit()

        return freelancer

    finally:
        connection.close()


def find_matching_freelancers(
    service: str,
    location: str,
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    service,
                    location,
                    phone,
                    verified,
                    available,
                    created_at
                FROM freelancers
                WHERE LOWER(service) = LOWER(%s)
                  AND LOWER(location) = LOWER(%s)
                  AND verified = TRUE
                  AND available = TRUE
                ORDER BY id;
                """,
                (service, location),
            )

            freelancers = cursor.fetchall()

        return freelancers

    finally:
        connection.close()


def verify_freelancer(freelancer_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE freelancers
                SET verified = TRUE
                WHERE id = %s
                RETURNING
                    id,
                    name,
                    service,
                    location,
                    phone,
                    verified,
                    available,
                    created_at;
                """,
                (freelancer_id,),
            )

            freelancer = cursor.fetchone()

        connection.commit()

        return freelancer

    finally:
        connection.close()