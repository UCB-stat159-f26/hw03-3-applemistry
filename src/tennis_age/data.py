import json
import re

import pandas as pd
import requests


BASE_URL = "https://www.tennisabstract.com"


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


def _normalize_player_name(name):
    name = name.strip()
    if not name:
        raise ValueError("Player name cannot be empty.")
    if " " not in name and any(char.isupper() for char in name[1:]):
        return name
    parts = re.findall(r"[A-Za-z]+", name)
    return "".join(part.capitalize() for part in parts)


def _extract_birth_date(html):
    match = re.search(r"var\s+dob\s*=\s*['\"]?(\d{8})['\"]?\s*;", html)
    if not match:
        raise ValueError("Could not determine player's birth date.")
    return match.group(1)


def _is_female_career(js_text):
    rows = _extract_matches(js_text)
    return bool(rows and re.fullmatch(r"\d{8}", rows[0][16]))


def _profile_url(player, female):
    endpoint = "wplayer.cgi" if female else "player-classic.cgi"
    return f"{BASE_URL}/cgi-bin/{endpoint}?p={player}"


def _download(url):
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        raise ValueError("Player not found on Tennis Abstract.")
    return response.text


def get_player_matches(name):
    player = _normalize_player_name(name)
    career_url = f"{BASE_URL}/jsmatches/{player}Career.js"
    try:
        career_js = _download(career_url)
        female = _is_female_career(career_js)
        profile_html = _download(_profile_url(player, female))
        birth_date = _extract_birth_date(profile_html)
        return _clean_career_js(career_js, birth_date)
    except (requests.RequestException, ValueError) as error:
        raise ValueError(f"Could not retrieve data for '{name}'.") from error
