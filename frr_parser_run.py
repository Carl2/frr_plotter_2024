#!/usr/bin/env python
from io import StringIO
import matplotlib.pyplot as plt
from pandas.core.groupby.generic import DataFrameGroupBy
import pandas as pd
from functools import reduce
from datetime import timedelta
import numpy as np
from col.common.frr_copy_parser import parse_file,parse_lines,make_performance_dataframe
from col.plot.plot import make_stage_plot_by_name2, PlotConfig, handle_generic_plot
from col.plot.plotter_fns import get_mpl_output
from pdb import set_trace
from icecream import ic
import streamlit as st




###############################################################################
#                           Create a matplot figure                           #
###############################################################################
def generate_matplot_handler(plot_config: PlotConfig) -> callable:
    """
    Generates a Matplotlib figure and axis for plotting with the specified plot configuration.

    Args:
        plot_config (PlotConfig): Configuration object containing properties for the plot,
                                   including figure size and other plot settings.

    Returns:
        tuple: A tuple containing:
            - fig (matplotlib.figure.Figure): The created figure object.
            - new_handler (callable): A handler function for the plot that can be used for
                                       creating generic plots with the specified configuration.
    """
    fig, ax = plt.subplots(figsize=plot_config.figsize, dpi=110)
    #ax.legend()
    plt.tight_layout()  # Adjust layout to prevent legend cutoff
    plotter_fn = get_mpl_output(ax) # This creates a matplot lib function
    new_handler = handle_generic_plot(plotter_fn, plot_config)
    return fig, new_handler


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



def fn_streamlit(fig: plt.Figure, header_text: str, tbl):

    def streamlit(df):
        st.header(header_text)
        st.pyplot(fig)
        # plt.plot(fig)
        # fig_html = mpld3.fig_to_html(fig)
        # components.html(fig_html, height=600)
        st.dataframe(df[["name","stage",tbl]].sort_values(by="stage"))


    return streamlit

###############################################################################
#                                   The rest                                  #
###############################################################################

def form_data():
    if 'frr_data' not in st.session_state:
        st.session_state.frr_data = ''

    # Use form to group input and submission
    with st.form("frr_form"):
        text_input = st.text_area(
            "FRR Data",
            value=st.session_state.frr_data,
            height=300,
            key="frr_input"
        )
        submitted = st.form_submit_button("Process Data")

        if submitted:
            if not text_input.strip():
                st.error("Please paste FRR data in the text box above")
            else:
                st.session_state.frr_data = text_input  # Persist data
                lines = text_input.strip().splitlines()
                lst = parse_lines(lines)
                df = make_performance_dataframe(lst)
                ic(df)
                return(df)
                # Proceed with data processing
                #process_data(text_input)  # Your processing function



def main():
    #st.title("FRR Parser")
    #st.write("Paste FRR data below (same format as tezt.txt):")
    # TODO: THis not complete.
    #df = form_data()

    # Add text area for input
    # text_input = st.text_area("FRR Data", height=300)

    # # Check if we have input
    # if not text_input:
    #     st.error("Please paste FRR data in the text box above")
    #     return

    # if st.button("Generate Plots"):
    df = parse_file("./tezt_world.txt")  # Commented out original file reading line
    #     #df = parse_file(text_stream)

    # Convert text input to a temporary file-like object
    # from io import StringIO
    # text_stream = StringIO(text_input)

    #df = parse_file("tezt.txt")  # Commented out original file reading line
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
    fig,handler = generate_matplot_handler(egap_config)
    df_data=make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit(fig,"Rider E-Gap Plot", "egap"),
        lambda x, y: handler(x, y),
        egap_config
    )

    fig,handler = generate_matplot_handler(egap_config_sum)
    _ =make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit(fig, "Rider E-Gap accumulated ", "egap"),
        lambda x, y: handler(x, y),
        egap_config_sum
    )

    fig,handler = generate_matplot_handler(times_config)
    _ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit(fig, "Rider times ", "time_delta"),
        lambda x, y: handler(x, y),
        times_config
    )

    fig,handler = generate_matplot_handler(polka_config)
    _ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit(fig, "Rider polka score ", "polka"),
        lambda x, y: handler(x, y),
        polka_config)

    fig,handler = generate_matplot_handler(polka_config_sum)
    _ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit(fig, "Rider polka score accum", "polka"),
        lambda x, y: handler(x, y),
        polka_config_sum)

    fig,handler = generate_matplot_handler(sprint_config)
    _ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit(fig, "Rider sprint score", "sprint"),
        lambda x, y: handler(x, y),
        sprint_config)

    fig,handler = generate_matplot_handler(sprint_config_sum)
    _ = make_stage_plot_by_name2(
        df, 'stage', 'name',
        fn_streamlit(fig, "Rider sprint score accumulated", "sprint"),
        lambda x, y: handler(x, y),
        sprint_config_sum)


    st.header("Data Table")
    st.dataframe(df_data)



if __name__ == '__main__':
    main()
