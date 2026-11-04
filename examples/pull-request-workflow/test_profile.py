from types import SimpleNamespace

from profile import build_profile


def test_build_profile_returns_public_fields():
    user = SimpleNamespace(
        id=1,
        username="adam",
        display_name="Adam",
        email="adam@example.com",
        is_staff=True,
    )

    result = build_profile(user)

    assert result == {
        "id": 1,
        "username": "adam",
        "display_name": "Adam",
    }


def test_build_profile_uses_username_as_fallback():
    user = SimpleNamespace(
        id=2,
        username="yassine",
        display_name=None,
        email="yassine@example.com",
        is_staff=False,
    )

    result = build_profile(user)

    assert result["display_name"] == "yassine"


def test_build_profile_uses_username_for_empty_display_name():
    user = SimpleNamespace(
        id=3,
        username="developer",
        display_name="",
        email="developer@example.com",
        is_staff=False,
    )

    result = build_profile(user)

    assert result["display_name"] == "developer"