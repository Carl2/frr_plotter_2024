#!/usr/bin/env python
import numpy as np
from functools import reduce
import pandas as pd
import matplotlib.pyplot as plt

def make_stage_plot_by_name(df_orig: pd.DataFrame,
                            file_name: str,
                            handler: callable):
    """Generates a stage plot for each rider based on their times in different stages.

    Args:
        df_orig (pd.DataFrame): The original dataframe containing rider data.
        file_name (str): The name of the file where the plot will be saved.
        handler (callable): A function to handle the grouping and plotting for each rider.

    """
    fig, ax = plt.subplots(figsize=(20, 16))
    df = df_orig.copy()
    unique_stages = df['Stage'].unique()
    name_group = df.groupby(['Name'])
    reduce(handler, name_group, {'stages': unique_stages, 'ax': ax})
    ax.legend()
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()
