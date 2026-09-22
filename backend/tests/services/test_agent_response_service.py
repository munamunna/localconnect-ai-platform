from app.services.agent_response_service import (
    format_freelancer_search_response,
)


def test_format_freelancer_search_response_success():
    results = [
        (
            110,
            "muna",
            "web and app",
            "payyoli",
            "string",
            True,
            True,
            None,
        )
    ]

    response = format_freelancer_search_response(results)

    assert response.message == (
        "I found 1 freelancer matching your request."
    )

    assert len(response.freelancers) == 1

    freelancer = response.freelancers[0]

    assert freelancer.id == 110
    assert freelancer.name == "muna"
    assert freelancer.service == "web and app"
    assert freelancer.location == "payyoli"
    assert freelancer.phone == "string"
    assert freelancer.verified is True
    assert freelancer.available is True


def test_format_freelancer_search_response_multiple_results():
    results = [
        (
            110,
            "muna",
            "web and app",
            "payyoli",
            "string",
            True,
            True,
            None,
        ),
        (
            111,
            "Ahmed",
            "web and app",
            "payyoli",
            "9876543210",
            True,
            False,
            None,
        ),
    ]

    response = format_freelancer_search_response(results)

    assert response.message == (
        "I found 2 freelancers matching your request."
    )

    assert len(response.freelancers) == 2


def test_format_freelancer_search_response_empty():
    response = format_freelancer_search_response([])

    assert response.message == (
        "No matching freelancers were found."
    )

    assert response.freelancers == []


def test_format_freelancer_search_response_allows_missing_phone():
    results = [
        (
            110,
            "muna",
            "web and app",
            "payyoli",
            None,
            True,
            True,
            None,
        )
    ]

    response = format_freelancer_search_response(results)

    assert response.freelancers[0].phone is None