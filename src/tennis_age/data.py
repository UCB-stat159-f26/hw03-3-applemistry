import json
import re

import pandas as pd


def _extract_matches(js_text):
    marker = js_text.find("var morematchmx")
    if marker == -1:
        raise ValueError("Could not find career match data.")
    start = js_text.find("[", marker)
    return json.JSONDecoder().raw_decode(js_text[start:])[0]


def _age_on_date(match_date, birth_date):
    match = pd.to_datetime(match_date, format="%Y%m%d")
    birth = pd.to_datetime(birth_date, format="%Y%m%d")
    return (match - birth).days / 365.25


def _opponent_age(row):
    value = row[16]
    if re.fullmatch(r"\d{8}", value):
        return _age_on_date(row[0], value)
    return float(value) if value else float("nan")


def _clean_match(row, player_birth_date):
    player_age = _age_on_date(row[0], player_birth_date)
    opponent_age = _opponent_age(row)
    return {
        "date": pd.to_datetime(row[0], format="%Y%m%d"),
        "opponent": row[11],
        "result": row[4],
        "player_age": player_age,
        "opponent_age": opponent_age,
        "age_difference": player_age - opponent_age,
    }


def _clean_career_js(js_text, player_birth_date):
    rows = _extract_matches(js_text)
    records = [_clean_match(row, player_birth_date) for row in rows]
    return pd.DataFrame(records)
