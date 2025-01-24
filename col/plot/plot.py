#!/usr/bin/env python
import numpy as np
from pandas.core.groupby.generic import DataFrameGroupBy
from functools import reduce
import pandas as pd
import matplotlib.pyplot as plt
from typing import Callable

T = TypeVar('T')
U = TypeVar('U')
def make_plot_handler(converter: Callable[[U],T])->Callable:

    def handler_fn(init_values: dict, name_group: DataFrameGroupBy):
        data = init_values['data']
        vals = init_values['times']
        index = init_values['index']
        stage_value = data[data['stage'] == stage][index]
        if len(stage_value) != 0:
            vals[int(stage) - 1] = converter(stage_value.iloc[0])
        return init_values
    # TODO: NOT DONE!


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
                             file_name: str,
                             handler: callable):
    """
    Generate a stage plot by grouping a DataFrame and applying a handler function to each group.


    Parameters:
    df_orig (pd.DataFrame): The original DataFrame to be plotted.
    unique_field (str): The field in the DataFrame to identify unique values.
    group_field (str): The field in the DataFrame to group by.
    file_name (str): The file name to save the generated plot.
    handler (callable): A function to handle each group and plot it.


    Returns:
    None

    TODO: This should probably be split up into something else sometime in the future.
    """
    fig, ax = plt.subplots(figsize=(20, 16))
    df = df_orig.copy()
    sorted_unique = np.sort(df[unique_field].unique())
    group_by_field = df.groupby(group_field)
    reduce(handler, group_by_field, {'unique': sorted_unique, 'ax': ax})
    ax.legend()
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()
