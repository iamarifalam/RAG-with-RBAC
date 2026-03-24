from atlas_rag.auth import decode_token, issue_token, seed_users, verify_password


def test_seeded_user_password_verifies() -> None:
    users = seed_users()
    assert verify_password("FinanceDemo123", users["alice.finance"].password_hash)


def test_issue_and_decode_token_round_trip() -> None:
    token, _ = issue_token("alice.finance", "finance", ttl_minutes=5)
    payload = decode_token(token)
    assert payload["sub"] == "alice.finance"
    assert payload["role"] == "finance"

