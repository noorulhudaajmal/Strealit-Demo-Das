import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from utils import *
import streamlit as st

colors = ["#2a9d8f", "#264653", "#e9c46a", "#f4a261", "#e76f51", "#ef233c", "#f6bd60", "#84a59d", "#f95738"]

def product_mean_price_card(df, product):
    df["Year"] = df["Date"].dt.year
    yearly_avg_price = df.groupby("Year")[product].mean().reset_index()
    yearly_avg_price = yearly_avg_price.sort_values(by="Year", ascending=True)
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df[product].mean(),
            number={"prefix": "$"},
            title={"text": "Avg. Price", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=yearly_avg_price["Year"],
        y=yearly_avg_price[product],
        mode="lines",
        fill='tozeroy',
        name="Avg. Price/Year",
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig


def product_net_price_card(df, product):
    df["Year"] = df["Date"].dt.year
    yearly_avg_price = df.groupby("Year")[product].sum().reset_index()
    yearly_avg_price = yearly_avg_price.sort_values(by="Year", ascending=True)
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df[product].sum(),
            number={"prefix": "$"},
            title={"text": "Total Price", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=yearly_avg_price["Year"],
        y=yearly_avg_price[product],
        mode="lines",
        fill='tozeroy',
        name="Net Price/Year",
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig


def product_std_price_card(df, product):
    df["Year"] = df["Date"].dt.year
    yearly_std_price = df.groupby("Year")[product].std().reset_index()
    yearly_std_price = yearly_std_price.sort_values(by="Year", ascending=True)
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df[product].std(),
            number={"prefix": "$"},
            title={"text": "Price std. Dev", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    # Adding a box plot
    fig.add_trace(go.Box(
        x=df[product]),
    )
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig


def product_min_price_card(df, product):
    df["Year"] = df["Date"].dt.year
    yearly_min_price = df.groupby("Year")[product].min().reset_index()
    yearly_min_price = yearly_min_price.sort_values(by="Year", ascending=True)
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df[product].min(),
            number={"prefix": "$"},
            title={"text": "Min Price", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=yearly_min_price["Year"],
        y=yearly_min_price[product],
        mode="lines",
        fill='tozeroy',
        name="Min Price/Year",
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig


def product_max_price_card(df, product):
    df["Year"] = df["Date"].dt.year
    yearly_max_price = df.groupby("Year")[product].max().reset_index()
    yearly_max_price = yearly_max_price.sort_values(by="Year", ascending=True)
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df[product].max(),
            number={"prefix": "$"},
            title={"text": "Max Price", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=yearly_max_price["Year"],
        y=yearly_max_price[product],
        mode="lines",
        fill='tozeroy',
        name="Max Price/Year",
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig


def product_prices_overtime(df, product):
    df["Year"] = df["Date"].dt.year
    yearly_net_price = df.groupby("Year")[product].sum().reset_index()
    yearly_avg_price = df.groupby("Year")[product].mean().reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=yearly_net_price['Year'],
            y=yearly_net_price[product],
            name="Total Price",
            marker=dict(color="#264653")
        ), secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=yearly_avg_price['Year'],
            y=yearly_avg_price[product],
            name="Avg. Price",
            mode="lines+markers",
            marker=dict(color="#e76f51"),
        ), secondary_y=True
    )

    fig.update_layout(title=f"{product} Price Over the Years", xaxis_title="Year", yaxis_title="Price")
    fig = update_hover_layout(fig)
    return fig


def product_std_over_years(df, product):
    df["Year"] = df["Date"].dt.year
    yearly_std_price = df.groupby("Year")[product].std().reset_index()
    yearly_std_price = yearly_std_price.sort_values(by="Year", ascending=True)

    fig = go.Figure()

    # Adding a box plot for each year
    for year in yearly_std_price["Year"]:
        yearly_data = df[df["Year"] == year][product]
        fig.add_trace(go.Box(
            y=yearly_data,
            name=f"{year}"
        )
        )

    fig = update_hover_layout(fig)
    return fig


def price_by_countries(df):
    fig = go.Figure()
    for i in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[i],
                name=i,
                mode="lines"
            )
        )
    fig = update_hover_layout(fig)
    fig.update_layout(title=f"Price Comparison Overtime", xaxis_title="Year", yaxis_title="Price")

    return fig


def countries_yearly_price(df):
    # df["Time"] = df.index
    df["Year"] = df["Time"].dt.year
    df = df.groupby("Year").sum().reset_index()
    fig = go.Figure()
    for i in df.columns:
        fig.add_trace(
            go.Bar(
                x=df["Year"],
                y=df[i],
                name=i,
            )
        )
    fig.update_layout(title=f"Yearly Price by Counties", xaxis_title="Year", yaxis_title="Price")
    fig = update_hover_layout(fig)
    return fig
