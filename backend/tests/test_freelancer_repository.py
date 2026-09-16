from app.database.connection import get_connection
from app.database.freelancer_repository import (
    create_freelancer,
    find_matching_freelancers,
    verify_freelancer,
    update_freelancer_availability,
)


def cleanup_database():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM freelancers;"
            )

        connection.commit()

    finally:
        connection.close()


def test_create_freelancer():
    cleanup_database()

    freelancer = create_freelancer(
        name="Ahmed",
        service="electrician",
        location="Kozhikode",
        phone="9876543210",
        verified=True,
        available=True,
    )

    assert freelancer is not None
    assert freelancer[1] == "Ahmed"
    assert freelancer[2] == "electrician"
    assert freelancer[3] == "Kozhikode"
    assert freelancer[5] is True
    assert freelancer[6] is True

    cleanup_database()

def test_find_matching_freelancers():
    cleanup_database()

    create_freelancer(
        name="Ahmed",
        service="electrician",
        location="Kozhikode",
        phone="9876543210",
        verified=True,
        available=True,
    )

    results = find_matching_freelancers(
        service="electrician",
        location="Kozhikode",
    )

    assert len(results) == 1
    assert results[0][1] == "Ahmed"

    cleanup_database()

def test_wrong_service_returns_no_freelancers():
    cleanup_database()

    create_freelancer(
        name="Ahmed",
        service="electrician",
        location="Kozhikode",
        phone="9876543210",
        verified=True,
        available=True,
    )

    results = find_matching_freelancers(
        service="plumber",
        location="Kozhikode",
    )

    assert results == []

    cleanup_database()

def test_wrong_location_returns_no_freelancers():
    cleanup_database()

    create_freelancer(
        name="Ahmed",
        service="electrician",
        location="Kozhikode",
        phone="9876543210",
        verified=True,
        available=True,
    )

    results = find_matching_freelancers(
        service="electrician",
        location="Kochi",
    )

    assert results == []

    cleanup_database()

def test_unavailable_freelancer_is_not_returned():
    cleanup_database()

    create_freelancer(
        name="Ahmed",
        service="electrician",
        location="Kozhikode",
        phone="9876543210",
        verified=True,
        available=False,
    )

    results = find_matching_freelancers(
        service="electrician",
        location="Kozhikode",
    )

    assert results == []

    cleanup_database()

def test_unverified_freelancer_is_not_returned():
    cleanup_database()

    create_freelancer(
        name="Ahmed",
        service="electrician",
        location="Kozhikode",
        phone="9876543210",
        verified=False,
        available=True,
    )

    results = find_matching_freelancers(
        service="electrician",
        location="Kozhikode",
    )

    assert results == []

    cleanup_database()


def test_verify_freelancer():

    cleanup_database()

    freelancer = create_freelancer(
        name="Ahmed",
        service="electrician",
        location="Kozhikode",
        phone="9876543210",
        verified=False,
        available=True,
    )

    freelancer_id = freelancer[0]

    verified_freelancer = verify_freelancer(freelancer_id)

    assert verified_freelancer is not None
    assert verified_freelancer[0] == freelancer_id
    assert verified_freelancer[1] == "Ahmed"
    assert verified_freelancer[5] is True

    cleanup_database()
    
def test_update_freelancer_availability():
    

    cleanup_database()

    freelancer = create_freelancer(
        name="Ahmed",
        service="electrician",
        location="Kozhikode",
        phone="9876543210",
        verified=True,
        available=True,
    )

    freelancer_id = freelancer[0]

    updated_freelancer = update_freelancer_availability(
        freelancer_id=freelancer_id,
        available=False,
    )

    assert updated_freelancer is not None
    assert updated_freelancer[0] == freelancer_id
    assert updated_freelancer[1] == "Ahmed"
    assert updated_freelancer[5] is True
    assert updated_freelancer[6] is False

    cleanup_database()



def test_update_freelancer_availability():

    cleanup_database()

    freelancer = create_freelancer(
        name="Ahmed",
        service="electrician",
        location="Kozhikode",
        phone="9876543210",
        verified=True,
        available=True,
    )

    freelancer_id = freelancer[0]

    updated_freelancer = update_freelancer_availability(
        freelancer_id=freelancer_id,
        available=False,
    )

    assert updated_freelancer is not None
    assert updated_freelancer[0] == freelancer_id
    assert updated_freelancer[1] == "Ahmed"
    assert updated_freelancer[5] is True
    assert updated_freelancer[6] is False

    cleanup_database()

