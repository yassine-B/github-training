def build_profile(user):
    """
    Build a public user profile without private account fields.
    """

    return {
        "id": user.id,
        "username": user.username,
        "display_name": user.display_name or user.username,
    }