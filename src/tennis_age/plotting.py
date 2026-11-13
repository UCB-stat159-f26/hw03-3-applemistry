import matplotlib.pyplot as plt


def plot_age_difference(data):
    required = {"player_age", "age_difference", "result"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    fig, ax = plt.subplots(figsize=(10, 6))
    for result, label in [("W", "Win"), ("L", "Loss")]:
        subset = data[data["result"] == result]
        ax.scatter(subset["player_age"], subset["age_difference"], label=label, alpha=0.7)

    ax.axhline(0, color="black", linewidth=1)
    ax.set_xlabel("Player age")
    ax.set_ylabel("Player age - opponent age")
    ax.legend()
    fig.tight_layout()
    return ax
