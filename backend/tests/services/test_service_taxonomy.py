import pytest

from app.services.service_taxonomy import normalize_service


def test_normalize_web_and_app_development():
    assert normalize_service(
        "web and app development"
    ) == "web and app"


def test_normalize_website_development():
    assert normalize_service(
        "website development"
    ) == "web and app"


def test_normalize_plumber():
    assert normalize_service(
        "plumber"
    ) == "plumbing"


def test_normalize_pipe_leakage():
    assert normalize_service(
        "pipe leakage"
    ) == "plumbing"


def test_normalize_electrician():
    assert normalize_service(
        "electrician"
    ) == "electrical"


def test_normalize_case_and_spaces():
    assert normalize_service(
        "  WEB AND APP DEVELOPMENT  "
    ) == "web and app"


def test_unknown_service_is_preserved():
    assert normalize_service(
        "solar panel installation"
    ) == "solar panel installation"


def test_empty_service_rejected():
    with pytest.raises(ValueError, match="Service is required"):
        normalize_service("")