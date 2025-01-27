#!/usr/bin/env python
import numpy as np
from pandas.core.groupby.generic import DataFrameGroupBy
from functools import reduce
import pandas as pd
import matplotlib.pyplot as plt
from typing import Callable,TypeVar
from copy import deepcopy

T = TypeVar('T')
U = TypeVar('U')

# This function returns a function which
# will get the value for a certain stage.
# But the value tends to need to be converted.
# So the added functionality is the coverter.
# So for example to get the Times
# index - The field in question  watt, egap, totals ....
# data - the dataframe in question
# value - the value to be inserted into the array ,
# From the start value is an array with nan values

def make_plot_handler(converter: Callable[[U],T], df_filter: Callable)->Callable:

    def handler_fn(init_values: dict, name_group: DataFrameGroupBy):
        data = init_values['data']
        vals = init_values['value']
        index = init_values['index']
        stage_value = df_filter(data, index)
        if len(stage_value) != 0:
            # This int(stage-1) needs to be rewritten.
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
