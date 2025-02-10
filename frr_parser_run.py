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
import streamlit as st
import mpld3

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


def egap_sum_handler(init_values: dict, stage: int) -> dict:
    data = init_values['data']
    vals = init_values['times']
    index = init_values['index']
    stage_value = data[data['stage'] == stage][index]

    if len(stage_value) != 0:
        val = stage_value.dt.total_seconds().iloc[0]
        stage_index = int(stage) - 1

        # Calculate cumulative sum
        if stage_index > 0:
            prev_val = vals[stage_index - 1]
            if not np.isnan(prev_val):
                val += prev_val

        vals[stage_index] = val

    return init_values

def polka_sum_handler(init_values: dict, stage: int) -> dict:
    data = init_values['data']
    vals = init_values['times']
    index = init_values['index']
    stage_value = data[data['stage'] == stage][index]

    if len(stage_value) != 0:
        val = stage_value.iloc[0]
        stage_index = int(stage) - 1

        # Calculate cumulative sum
        if stage_index > 0:
            prev_val = vals[stage_index - 1]
            if not np.isnan(prev_val):
                val += prev_val

        vals[stage_index] = val

    return init_values



def main():
    df = parse_file("tezt.txt")

    # Configure different plot types using PlotConfig
    egap_config = PlotConfig(
        index_field='egap_td',
        ylabel='Gap',
        y_formatter=set_ytick_time_label
    )

    egap_config_sum = PlotConfig(
        index_field='egap_td',
        ylabel='Gap',
        y_formatter=set_ytick_time_label,
        stage_name_handler=egap_sum_handler
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

    polka_config_sum = PlotConfig(
        index_field='total',
        ylabel='Polka',
        stage_name_handler=polka_sum_handler
    )

    # Create plots using the generic handler
    fig_egap,df_data=make_stage_plot_by_name2(
        df, 'stage', 'name',
        "frr2_plot_rider_egap.svg",
        lambda x, y: handle_generic_plot(x, y, egap_config),
        egap_config
    )

    fig_egap_sum,_ =make_stage_plot_by_name2(
        df, 'stage', 'name',
        "frr2_plot_rider_egap.svg",
        lambda x, y: handle_generic_plot(x, y, egap_config_sum),
        egap_config_sum
    )


    fig_times,_ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        "frr2_plot_rider_times.svg",
        lambda x, y: handle_generic_plot(x, y, times_config),
        times_config
    )

    fig_polka,_ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        "frr2_plot_rider_polka.svg",
        lambda x, y: handle_generic_plot(x, y, polka_config),
        polka_config)

    fig_polka_sum,_ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        "frr2_plot_rider_polka_sum.svg",
        lambda x, y: handle_generic_plot(x, y, polka_config_sum),
        polka_config_sum)

    st.header("Rider E-Gap Plot")
    st.pyplot(fig_egap)

    st.header("Rider SUM E-Gap Plot")
    st.pyplot(fig_egap_sum)

    st.header("Rider Times Plot")
    st.pyplot(fig_times)

    st.header("Rider Polka Plot")
    st.pyplot(fig_polka)

    st.header("Rider Polka Plot")
    st.pyplot(fig_polka_sum)

    st.header("Data Table")
    st.dataframe(df_data)



if __name__ == '__main__':
    main()
