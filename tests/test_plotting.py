import matplotlib.pyplot as plt
import pandas as pd
import pytest

from tennis_age import plot_age_difference


def test_plot_age_difference():
    data = pd.DataFrame({
        "player_age": [20, 21, 22],
        "age_difference": [-2, 1, 3],
        "result": ["W", "L", "W"],
    })

    ax = plot_age_difference(data)

    assert ax.get_xlabel() == "Player age"
    assert ax.get_ylabel() == "Player age - opponent age"
    assert len(ax.collections) == 2
    plt.close(ax.figure)


def test_plot_missing_columns():
    data = pd.DataFrame({"player_age": [20]})

    with pytest.raises(ValueError, match="Missing required columns"):
        plot_age_difference(data)
