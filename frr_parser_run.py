#!/usr/bin/env python
from pandas.core.groupby.generic import DataFrameGroupBy
import pandas as pd
from functools import reduce
from datetime import timedelta
import numpy as np
from col.common.frr_copy_parser import parse_file
from col.plot.plot import make_stage_plot_by_name2
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

def handle_egap(init_values: dict, name_group: DataFrameGroupBy):

    name, data = name_group
    unique_stages = init_values['unique']
    ax = init_values['ax']
    times = np.full(len(unique_stages), np.nan)
    rider_vals = reduce(handle_stage_name, unique_stages, {
        'data': data,
        'times': times,
        'index': 'egap_td'} )
    ax.plot(unique_stages, rider_vals['times'], 'o-', label=name[0])
    ax.set_xticks(unique_stages)
    ax.set_xlabel('Stages')
    set_ytick_time_label(ax)
    init_values[name[0]] = rider_vals['times']
    return init_values


def handle_stage_times(init_values: dict, name_group: DataFrameGroupBy):
    name, data = name_group
    unique_stages = init_values['unique']
    ax = init_values['ax']
    times = np.full(len(unique_stages), np.nan)

    rider_vals = reduce(handle_stage_name, unique_stages, {
        'data': data,
        'times': times,
        'index': 'time_delta'
    })

    ax.plot(unique_stages, rider_vals['times'], 'o-', label=name[0])
    ax.set_xticks(unique_stages)
    ax.set_xlabel('Stages')

    set_ytick_time_label(ax)

    init_values[name[0]] = rider_vals['times']
    return init_values

def handle_pos_name(init_values: dict, stage: pd.DataFrame):
    data = init_values['data']
    vals = init_values['times']
    index = init_values['index']
    stage_value = data[data['stage'] == stage][index]
    if len(stage_value) != 0:
        vals[int(stage) - 1] = int(stage_value.iloc[0])
    return init_values

def handle_polka(init_values: dict, name_group: DataFrameGroupBy):
    name, data = name_group
    unique_stages = init_values['unique']
    ax = init_values['ax']
    positions = np.full(len(unique_stages), np.nan)
    rider_vals = reduce(handle_pos_name, unique_stages, {
         'data': data,
        'times': positions,
        'index': 'total'} )
    ax.plot(unique_stages, rider_vals['times'], 'o-', label=name[0])
    ax.set_xticks(unique_stages)
    ax.set_xlabel('Stages')
    ax.set_ylabel('Polka')
    init_values[name[0]] = rider_vals['times']
    return init_values


def main():
    df=parse_file("tezt.txt")
    #set_trace()
    make_stage_plot_by_name2(df,'stage', 'name', "frr2_plot_rider_egap.svg", handle_egap)
    make_stage_plot_by_name2(df,'stage', 'name', "frr2_plot_rider_times.svg", handle_stage_times)
    make_stage_plot_by_name2(df,'stage', 'name', "frr2_plot_rider_polka.svg", handle_polka)


if __name__ == '__main__':
    main()
