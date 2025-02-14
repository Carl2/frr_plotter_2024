#!/usr/bin/env python
import numpy as np
from pandas.core.groupby.generic import DataFrameGroupBy
from functools import reduce
import pandas as pd
import matplotlib.pyplot as plt
from typing import Callable, TypeVar, Optional
from copy import deepcopy
from dataclasses import dataclass

T = TypeVar('T')
U = TypeVar('U')

def handle_stage_name(init_values: dict, stage: int) -> dict:
    """Handle data processing for a single stage.

    Args:
        init_values: Dictionary containing data and configuration
        stage: Stage number to process

    Returns:
        dict: Updated initialization values
    """
    data = init_values['data']
    vals = init_values['times']
    index = init_values['index']
    stage_value = data[data['stage'] == stage][index]

    if len(stage_value) != 0:
        if hasattr(stage_value, 'dt'):
            val = stage_value.dt.total_seconds().iloc[0]
        else:
            val = stage_value.iloc[0]
        vals[int(stage)-1] = val
    return init_values




@dataclass
class PlotConfig:
    """Configuration for plot generation.

    This class encapsulates the configuration needed to generate different types
    of plots in the cycling race analysis system.

    Attributes:
        index_field: Field name in the DataFrame to use for plotting.
        ylabel: Label for the y-axis.
        y_formatter: Optional function to format y-axis ticks.
        plot_style: Style string for plot (default: 'o-').
        figsize: Tuple defining figure dimensions (default: (20, 16)).

    Example:
        >>> time_config = PlotConfig(
        ...     index_field='time_delta',
        ...     ylabel='Time',
        ...     y_formatter=set_ytick_time_label
        ... )
    """

    index_field: str
    ylabel: str
    y_formatter: Optional[Callable[[plt.Axes], None]] = None
    plot_style: str = 'o-'
    figsize: tuple[int, int] = (24, 12)
    stage_name_handler: Callable[[ dict, int], dict] = handle_stage_name

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if not isinstance(self.index_field, str):
            raise TypeError("index_field must be a string")
        if not isinstance(self.ylabel, str):
            raise TypeError("ylabel must be a string")
        if (self.y_formatter is not None and
            not callable(self.y_formatter)):
            raise TypeError("y_formatter must be callable or None")

# This function returns a function which
# will get the value for a certain stage.
# But the value tends to need to be converted.
# So the added functionality is the coverter.
# So for example to get the Times
# index - The field in question  watt, egap, totals ....
# data - the dataframe in question
# value - the value to be inserted into the array ,
# From the start value is an array with nan values



def handle_generic_plot(init_values: dict,
                       name_group: DataFrameGroupBy,
                       plot_config: PlotConfig) -> dict:
    """Handle generic plotting for different race metrics.

    Args:
        init_values: Dictionary containing plot initialization values.
        name_group: Grouped DataFrame containing race data.
        plot_config: PlotConfig instance with plotting configuration.

    Returns:
        dict: Updated initialization values dictionary.

    Example:
        >>> config = PlotConfig(index_field='time_delta', ylabel='Time')
        >>> result = handle_generic_plot(init_vals, group_data, config)
    """
    name, data = name_group
    #print(f"Debug - name type: {type(name)}, name value: {name}")  # Debug print
    unique_stages = init_values['unique']
    ax = init_values['ax']
    values = np.full(len(unique_stages), np.nan)

    rider_vals = reduce(plot_config.stage_name_handler,
                        unique_stages, {
                            'data': data,
                            'times': values,
                            'index': plot_config.index_field
                        })

    full_name = name[0] if isinstance(name, tuple) else name
    #ic(full_name)
    ax.plot(unique_stages, rider_vals['times'],
            plot_config.plot_style, label=full_name)
    ax.set_xticks(unique_stages)
    ax.set_xlabel('Stages')
    ax.set_ylabel(plot_config.ylabel)

    if plot_config.y_formatter:
        plot_config.y_formatter(ax)

    init_values[name[0]] = rider_vals['times']
    return init_values


def make_plot_handler(converter: Callable[[U],T], df_filter: Callable)->Callable:

    def handler_fn(init_values: dict, name_group: DataFrameGroupBy):
        data = init_values['data']
        vals = init_values['value']
        index = init_values['index']
        stage = data['stage'].iloc[0]  # Get stage from the data
        stage_value = df_filter(data, index)
        if len(stage_value) != 0:
            vals[int(stage) - 1] = converter(stage_value.iloc[0])
        return init_values

    return handler_fn


def filter_by(*, match_field: str, output_field: str ):
    def filter_fn(df: pd.DataFrame, match_val: T):
            out =  df[df[match_field] == match_val][output_field]
            return deepcopy(out)
    return filter_fn


# def make_stage_plot_by_name(df_orig: pd.DataFrame,
#                             file_name: str,
#                             handler: callable):
#     """Generates a stage plot for each rider based on their times in different stages.

#     Args:
#         df_orig (pd.DataFrame): The original dataframe containing rider data.
#         file_name (str): The name of the file where the plot will be saved.
#         handler (callable): A function to handle the grouping and plotting for each rider.

#     """
#     fig, ax = plt.subplots(figsize=(20, 16))
#     df = df_orig.copy()
#     unique_stages = df['Stage'].unique()
#     group_by_field = df.groupby(['Name'])
#     reduce(handler, group_by_field, {'stages': unique_stages, 'ax': ax})
#     ax.legend()
#     plt.savefig(file_name, bbox_inches='tight')
#     plt.close()


def make_stage_plot_by_name2(df_orig: pd.DataFrame,
                            unique_field: str,
                            group_field: str,
                            output_handler: Callable[[plt.Figure, pd.DataFrame],None],
                            handler: Callable,
                            plot_config: PlotConfig) -> None:
    """Generate a stage plot by grouping a DataFrame and applying a handler function.

    Args:
        df_orig: The original DataFrame to be plotted.
        unique_field: Field in the DataFrame to identify unique values.
        group_field: Field in the DataFrame to group by.
        file_name: File name to save the generated plot.
        handler: Function to handle each group and plot it.
        plot_config: PlotConfig instance with plotting configuration.

    Returns:
        None
    """
    fig, ax = plt.subplots(figsize=plot_config.figsize, dpi=110)
    df = df_orig.copy()
    sorted_unique = np.sort(df[unique_field].unique())
    group_by_field = df.groupby(group_field)
    reduce(handler, group_by_field, {'unique': sorted_unique, 'ax': ax})
    # plt.legend(fontsize=14)
    # plt.legend(loc='best')ccb
    # Single legend call with customization
    ax.legend(bbox_to_anchor=(1.05, 1),
             loc='upper left',
             fontsize=12,
             borderaxespad=0.)

    #ax.legend()
    plt.tight_layout()  # Adjust layout to prevent legend cutoff
    output_handler(fig, df)
    return fig,df
    #plt.savefig(file_name, bbox_inches='tight')
    #plt.close()
