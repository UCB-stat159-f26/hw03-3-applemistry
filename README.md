# Tennis Age

A Python package for retrieving a tennis player's career match data from Tennis Abstract and reproducing the age-difference scatter plot from HW2.

## Installation

Install the package directly from GitHub:

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-3-applemistry.git
```

## Usage

The package provides two public functions:

- `get_player_matches()` retrieves and cleans a player's career match data from Tennis Abstract.
- `plot_age_difference()` creates a scatter plot comparing the player's age with the age difference between the player and their opponent.

### Serena Williams

```python
from tennis_age import get_player_matches, plot_age_difference

serena = get_player_matches("Serena Williams")
plot_age_difference(serena)
```

The player name can be provided in multiple formats:

```python
get_player_matches("serena williams")
get_player_matches("Serena Williams")
get_player_matches("SerenaWilliams")
```

### Rafael Nadal

```python
rafa = get_player_matches("Rafael Nadal")
plot_age_difference(rafa)
```

If the player cannot be found, the function raises a meaningful error:

```python
get_player_matches("GastonSanchez")
```

## Output

`get_player_matches()` returns a pandas DataFrame containing:

- `date`: match date
- `opponent`: opponent name
- `result`: win or loss
- `player_age`: player's age at the time of the match
- `opponent_age`: opponent's age at the time of the match
- `age_difference`: player age minus opponent age

`plot_age_difference()` takes this DataFrame and produces a scatter plot with player age on the x-axis and age difference on the y-axis, with points separated by win/loss status.

## Testing

Automated tests use mock career JS files rather than making requests to Tennis Abstract's live servers.

Run the tests with:

```bash
python -m pytest -v
```

The tests cover both male and female career-file formats, data cleaning, player-name normalization, age calculations, error handling, and plotting.

## Project Structure

```text
src/tennis_age/
    __init__.py
    data.py
    plotting.py

tests/
    fixtures/
        FemalePlayerCareer.js
        MalePlayerCareer.js
    test_data.py
    test_plotting.py

pyproject.toml
README.md
```

## Personal Reflection

This assignment helped me understand how the data cleaning work from HW2 can be generalized into a reusable package instead of being written specifically for one player. One of the main challenges was handling the different formats used by Tennis Abstract for male and female players. Female career files provide opponents' dates of birth, while male career files provide their ages directly, so the package needed to recognize both formats and process them consistently. I also learned more about designing a package around a small public interface while keeping parsing and cleaning logic in private helper functions as well. Writing tests with mock JS files was useful because it allowed the data processing logic to be tested reliably without depending on the availability or behavior of a live website.
