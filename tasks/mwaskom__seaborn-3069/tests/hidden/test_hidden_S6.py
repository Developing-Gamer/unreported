import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


def test_brief_numeric_legend_includes_maximum_tick():
    fig, ax = plt.subplots()
    try:
        sns.scatterplot(
            x=[0, 1, 2, 3, 4, 5],
            y=[0, 1, 4, 9, 16, 25],
            hue=[0, 20, 40, 60, 80, 100],
            legend="brief",
            ax=ax,
        )
        labels = [text.get_text() for text in ax.get_legend().get_texts()]
        assert "100" in labels, labels
    finally:
        plt.close(fig)
