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
#import mpld3

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

###############################################################################
#                                Output handler                               #
###############################################################################



def fn_streamlit(header_text: str, tbl):

    def streamlit(fig,df ):
        st.header(header_text)
        st.pyplot(fig)
        st.dataframe(df[["name","stage",tbl]].sort_values(by="stage"))

    return streamlit

###############################################################################
#                                   The rest                                  #
###############################################################################

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
        index_field='polka',
        ylabel='Polka'
    )

    polka_config_sum = PlotConfig(
        index_field='polka',
        ylabel='Polka',
        stage_name_handler=polka_sum_handler
    )

    sprint_config = PlotConfig(
        index_field='sprint',
        ylabel='Polka'
    )

    sprint_config_sum = PlotConfig(
        index_field='sprint',
        ylabel='Polka',
        stage_name_handler=polka_sum_handler
    )

    total_config = PlotConfig(
        index_field='total',
        ylabel='Total',
    )

    total_config_sum = PlotConfig(
        index_field='total',
        ylabel='Total accumulated',
        stage_name_handler=polka_sum_handler
    )


    ###########################################################################
    #                              Createing data                             #
    ###########################################################################
    # Create plots using the generic handler
    fig_egap,df_data=make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit("Rider E-Gap Plot", "egap"),
        lambda x, y: handle_generic_plot(x, y, egap_config),
        egap_config
    )

    fig_egap_sum,_ =make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit("Rider E-Gap accumulated ", "egap"),
        lambda x, y: handle_generic_plot(x, y, egap_config_sum),
        egap_config_sum
    )


    fig_times,_ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit("Rider times ", "time_delta"),
        lambda x, y: handle_generic_plot(x, y, times_config),
        times_config
    )

    fig_polka,_ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit("Rider polka score ", "polka"),
        lambda x, y: handle_generic_plot(x, y, polka_config),
        polka_config)

    fig_polka_sum,_ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit("Rider polka score accum", "polka"),
        lambda x, y: handle_generic_plot(x, y, polka_config_sum),
        polka_config_sum)

    fig_sprint,_ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit("Rider sprint score", "sprint"),
        lambda x, y: handle_generic_plot(x, y, sprint_config),
        sprint_config)


    fig_sprint_sum,_ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit("Rider sprint score accumulated", "sprint"),
        lambda x, y: handle_generic_plot(x, y, sprint_config_sum),
        sprint_config_sum)

    # fig_total,_ = make_stage_plot_by_name2(
    #     df, 'stage', 'name',
    #     "frr2_plot_rider_total.svg",
    #     lambda x, y: handle_generic_plot(x, y, total_config),
    #     total_config)

    # fig_total_sum,_ = make_stage_plot_by_name2(
    #     df, 'stage', 'name',
    #     "frr2_plot_rider_total.svg",
    #     lambda x, y: handle_generic_plot(x, y, total_config_sum),
    #     total_config_sum)


    ###########################################################################
    #                                Printouts                                #
    ###########################################################################
    #fn_streamlit("Rider E-Gap Plot", "egap")(fig_egap, df)
    # st.header("Rider E-Gap Plot")
    # st.pyplot(fig_egap)

    # st.header("Rider SUM E-Gap Plot")
    # st.pyplot(fig_egap_sum)

    # st.header("Rider Times Plot")
    # st.pyplot(fig_times)

    # st.header("Rider Polka Plot")
    # st.pyplot(fig_polka)

    # st.header("Rider Polka Plot accumulated")
    # st.pyplot(fig_polka_sum)

    # st.header("Rider sprint Plot")
    # st.pyplot(fig_sprint)

    # st.header("Rider sprint Plot accumulated")
    # st.pyplot(fig_sprint_sum)

    # st.header("Total pts / stage")
    # st.pyplot(fig_total)

    # st.header("Total pts accumulated")
    # st.pyplot(fig_total_sum)

    st.header("Data Table")
    st.dataframe(df_data)

#    plt.savefig(, bbox_inches='tight')


if __name__ == '__main__':
    main()
