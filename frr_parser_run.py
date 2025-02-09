#!/usr/bin/env python
from pandas.core.groupby.generic import DataFrameGroupBy
import pandas as pd
from functools import reduce
from datetime import timedelta
import numpy as np
from col.common.frr_copy_parser import parse_file
from col.plot.plot import make_stage_plot_by_name2, PlotConfig, handle_generic_plot
from pdb import set_trace
from icecream import ic

def convert_to_time_repr(seconds: float):
    return str(timedelta(seconds=seconds))



def set_ytick_time_label(ax):
    yticks = ax.get_yticks()
    ax.set_yticks(yticks)  # Set the tick positions first
    tm_arr = map(convert_to_time_repr, yticks)
    ax.set_yticklabels(tm_arr, ha='right' )

def handle_stage_name(init_values, stage):
    data = init_values['data']
    vals = init_values['times']
    index = init_values['index']
    stage_value = data[data['stage'] == stage][index]

    if len(stage_value) != 0:
        val = stage_value.dt.total_seconds().iloc[0]
        vals[int(stage)-1] = val
    return init_values



def main():
    df = parse_file("tezt.txt")
    
    # Configure different plot types using PlotConfig
    egap_config = PlotConfig(
        index_field='egap_td',
        ylabel='Gap',
        y_formatter=set_ytick_time_label
    )
    
    times_config = PlotConfig(
        index_field='time_delta',
        ylabel='Time',
        y_formatter=set_ytick_time_label
    )
    
    polka_config = PlotConfig(
        index_field='total',
        ylabel='Polka'
    )

    # Create plots using the generic handler
    make_stage_plot_by_name2(
        df, 'stage', 'name',
        "frr2_plot_rider_egap.svg",
        lambda x, y: handle_generic_plot(x, y, egap_config),
        egap_config
    )
    
    make_stage_plot_by_name2(
        df, 'stage', 'name',
        "frr2_plot_rider_times.svg",
        lambda x, y: handle_generic_plot(x, y, times_config),
        times_config
    )
    
    make_stage_plot_by_name2(
        df, 'stage', 'name',
        "frr2_plot_rider_polka.svg",
        lambda x, y: handle_generic_plot(x, y, polka_config),
        polka_config
    )


if __name__ == '__main__':
    main()
