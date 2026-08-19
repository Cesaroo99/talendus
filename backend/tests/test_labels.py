from app.models.enums import ApplicationStatus
from app.services.labels import application_status_label, lang_of


def test_application_status_labels_never_expose_enum_codes():
    assert application_status_label(ApplicationStatus.WITHDRAWN) == "Retirée"
    assert application_status_label("WITHDRAWN", locale="fr-CA") == "Retirée"
    assert application_status_label("withdrawn", locale="en-CA") == "Withdrawn"
    assert lang_of(locale="en") == "en"
    assert lang_of(locale="fr-CA") == "fr"
