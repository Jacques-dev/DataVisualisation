import streamlit as st
from src.graph_controls import graph_controls
from src.utility import load_dataframe
from streamlit.components.v1 import iframe


def fixed_content():
    """
    Contains fixed content visible across different links
    :return:
    """


def views(link):
    """
    Helper function for directing users to various pages.
    :param link: str, option selected from the radio button
    :return:
    """
    if link == 'Home':

        uploaded_file = "uber-raw-data-apr14.csv"

        fixed_content()
        if uploaded_file is not None:
            df, columns = load_dataframe(uploaded_file=uploaded_file)

            st.sidebar.subheader("Visualize your data")

            show_data = st.sidebar.checkbox(label='Show data')

            if show_data:
                try:
                    st.subheader("Data view")
                    number_of_rows = st.sidebar.number_input(label='Select number of rows', min_value=2)

                    st.dataframe(df.head(number_of_rows))
                except Exception as e:
                    print(e)

            st.sidebar.subheader("Theme selection")

            theme_selection = st.sidebar.selectbox(label="Select your themes",
                                                   options=['plotly', 'plotly_white',
                                                            'ggplot2',
                                                            'seaborn', 'simple_white'])
            st.sidebar.subheader("Chart selection")
            chart_type = st.sidebar.selectbox(label="Select your chart type.",
                                              options=['Scatter plots', 'Density contour',
                                                       'Sunburst','Pie Charts','Density heatmaps',
                                                       'Histogram', 'Box plots','Tree maps',
                                                       'Violin plots', ])  # 'Line plots',

            graph_controls(chart_type=chart_type, df=df, dropdown_options=columns, template=theme_selection)






