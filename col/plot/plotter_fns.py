import matplotlib.pyplot as plt
from typing import Sequence
#from col.plot.plot import PlotConfig

def get_mpl_output(ax: plt.Axes) -> callable:
    """Creates a matplotlib-specific output function."""
    def output_fn(x_values: Sequence[float],
                 y_values: Sequence[float],
                 label: str,
                 config) -> None:
        ax.plot(x_values, y_values, config.plot_style, label=label)
        ax.set_xticks(x_values)
        ax.set_xlabel('Stages')
        ax.set_ylabel(config.ylabel)
        if config.y_formatter:
            config.y_formatter(ax)
    return output_fn
