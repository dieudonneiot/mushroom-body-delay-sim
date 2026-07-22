from mbsim.i18n import STRINGS, t


def test_every_string_has_english_and_turkish():
    for key, entry in STRINGS.items():
        assert "en" in entry and entry["en"].strip(), f"{key} missing English text"
        assert "tr" in entry and entry["tr"].strip(), f"{key} missing Turkish text"


def test_t_formats_placeholders():
    assert t("err_load_data", "en", error="boom") == "Could not load data: boom"
    assert t("err_load_data", "tr", error="boom") == "Veri yüklenemedi: boom"


def test_t_falls_back_to_key_for_unknown_entry():
    assert t("no_such_key", "en") == "no_such_key"
