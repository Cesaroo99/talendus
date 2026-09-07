from app.services.contact_email import is_ready_to_contact, is_valid_public_email, matches_email_filter


def test_public_email_validation():
    assert is_valid_public_email("info@lamilanaise.com")
    assert not is_valid_public_email("")
    assert not is_valid_public_email("noreply@example.com")
    assert not is_valid_public_email("you@company.com")
    assert is_ready_to_contact("rh@melocheinc.com", "VERIFIED_MEDIUM")
    assert not is_ready_to_contact("info@x.com", "INVALID")


def test_email_filter_meanings():
    assert matches_email_filter("info@x.ca", wanted="with")
    assert not matches_email_filter("", wanted="with")
    assert matches_email_filter("", wanted="without")
    assert not matches_email_filter("info@x.ca", wanted="without")
    assert matches_email_filter("info@x.ca", wanted="verified", verified=True)
    assert matches_email_filter("info@x.ca", wanted="unverified", verified=False)
    assert matches_email_filter("info@x.ca", wanted="", ready="ready")
    assert not matches_email_filter("", wanted="", ready="ready")
