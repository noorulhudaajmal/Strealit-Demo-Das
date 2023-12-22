import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from plots.plots import *

# ------------------------------ Page Configuration------------------------------
st.set_page_config(page_title="Demo", page_icon="📊", layout="wide")
# ----------------------------------- Page Styling ------------------------------

with open("css/style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<style>
    [data-testid=stHeader] {
        display:none;
    }
    [data-testid=block-container] {
        padding-top: 0px;
        # background:#eff0d1;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
  <style>
   [data-testid=stSidebarUserContent]{
      margin-top: -75px;
      margin-top: -75px;
      fontsize=100px;
    }
    .logo{
        font-size:3rem !important;
    }
  </style>
""", unsafe_allow_html=True)
# st.title('Country and Product Analysis Dashboard')


def load_data(file_name):
    # Load each sheet into a dictionary of dataframes
    return pd.read_excel(file_name, sheet_name=None)


# Load data
data = load_data('./data/Demo_data.xlsx')

menu = option_menu(menu_title=None, options=["Product Analysis", "Price Comparison"], orientation="horizontal")

if menu == "Product Analysis":
    filters_row = st.columns((1, 1, 2))
    # Country and product selection
    country = filters_row[0].selectbox('Select a Country', options=list(data.keys()))
    product = filters_row[1].selectbox('Select a Product', options=data[country].columns[1:])

    df = data[country]
    df["Date"] = pd.to_datetime(df["Date"])

    # Date range selection
    start_date, end_date = filters_row[2].select_slider(
        'Select a date range',
        options=df['Date'].dt.date,
        value=(df['Date'].min(), df['Date'].max())
    )

    # Filter data
    df_filtered = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

    # ------------------------------------------------------------------------------------------------------

    kpis_row = st.columns(5)
    kpis_row[0].plotly_chart(product_mean_price_card(df_filtered, product), use_container_width=True)
    kpis_row[1].plotly_chart(product_net_price_card(df_filtered, product), use_container_width=True)
    kpis_row[2].plotly_chart(product_std_price_card(df_filtered, product), use_container_width=True)
    kpis_row[3].plotly_chart(product_min_price_card(df_filtered, product), use_container_width=True)
    kpis_row[4].plotly_chart(product_max_price_card(df_filtered, product), use_container_width=True)

    charts_row = st.columns(2)

    charts_row[0].plotly_chart(product_prices_overtime(df_filtered, product), use_container_width=True)
    charts_row[1].plotly_chart(product_std_over_years(df_filtered, product), use_container_width=True)

if menu == "Price Comparison":
    row_1 = st.columns((1,2,2))
    # Select product for comparison
    comparison_product = row_1[0].selectbox('Select a Product for Comparison',
                                      options=data[next(iter(data))].columns[1:])

    # Aggregating data
    comparison_data = {}
    for country, df in data.items():
        df_agg = df[['Date', comparison_product]].dropna()
        comparison_data[country] = df_agg.set_index('Date').rename(columns={comparison_product: country})

    comparison_df = pd.concat(comparison_data.values(), axis=1)
    comparison_df["Time"] = comparison_df.index
    # Date range selection
    start_date, end_date = row_1[1].select_slider(
        'Select a date range',
        options=comparison_df["Time"].dt.date,
        value=(comparison_df['Time'].min(), comparison_df['Time'].max())
    )

    # Filter data
    comparison_df = comparison_df[(comparison_df['Time'] >= pd.to_datetime(start_date)) &
                                  (comparison_df['Time'] <= pd.to_datetime(end_date))]

    # figures
    row_2 = st.columns(2)
    row_2[0].plotly_chart(price_by_countries(comparison_df), use_container_width=True)
    row_2[1].plotly_chart(countries_yearly_price(comparison_df), use_container_width=True)