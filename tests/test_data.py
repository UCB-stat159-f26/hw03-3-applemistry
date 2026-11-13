from pathlib import Path

import pytest

from tennis_age.data import _clean_career_js, _extract_matches


FIXTURES = Path(__file__).parent / "fixtures"


def _read_fixture(filename):
    return (FIXTURES / filename).read_text()


def test_extract_matches():
    text = _read_fixture("FemalePlayerCareer.js")
    rows = _extract_matches(text)
    assert len(rows) == 3
    assert rows[0][11] == "Anne Miller"


def test_clean_female_career():
    text = _read_fixture("FemalePlayerCareer.js")
    data = _clean_career_js(text, "19810926")
    assert len(data) == 3
    assert data.loc[0, "result"] == "L"
    assert data.loc[0, "opponent"] == "Anne Miller"
    assert data.loc[0, "player_age"] == pytest.approx(14.09, abs=0.01)
    assert data.loc[0, "opponent_age"] == pytest.approx(18.78, abs=0.01)


def test_clean_male_career():
    text = _read_fixture("MalePlayerCareer.js")
    data = _clean_career_js(text, "19860603")
    assert len(data) == 3
    assert data.loc[0, "result"] == "L"
    assert data.loc[0, "opponent"] == "Guillermo Platel"
    assert data.loc[0, "opponent_age"] == pytest.approx(22.2642, abs=0.0001)


def test_age_difference():
    text = _read_fixture("MalePlayerCareer.js")
    data = _clean_career_js(text, "19860603")
    expected = data.loc[0, "player_age"] - data.loc[0, "opponent_age"]
    assert data.loc[0, "age_difference"] == pytest.approx(expected)


def test_missing_match_data():
    with pytest.raises(ValueError, match="career match data"):
        _extract_matches("not valid tennis data")


from tennis_age.data import _extract_birth_date, _normalize_player_name


@pytest.mark.parametrize(
    "name, expected",
    [
        ("serena williams", "SerenaWilliams"),
        ("Serena Williams", "SerenaWilliams"),
        ("SerenaWilliams", "SerenaWilliams"),
        ("Rafael Nadal", "RafaelNadal"),
    ],
)
def test_normalize_player_name(name, expected):
    assert _normalize_player_name(name) == expected


def test_empty_player_name():
    with pytest.raises(ValueError, match="cannot be empty"):
        _normalize_player_name("")


def test_extract_birth_date():
    html = "var dob = 19860603;"
    assert _extract_birth_date(html) == "19860603"
