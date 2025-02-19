import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------
# 1) Load and Process Data (Using Gapminder)
# -----------------------------------------------------------
gapminder = px.data.gapminder()

# Unique years for the slider
years = sorted(gapminder["year"].unique())

# Unique continents for the dropdown filter
continents = sorted(gapminder["continent"].unique())

# -----------------------------------------------------------
# 2) Create Dash App with Bootstrap Styling
# -----------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server  # Expose Flask app for deployment

# -----------------------------------------------------------
# 3) Layout and Components
# -----------------------------------------------------------
app.layout = dbc.Container([
    html.H2("Global Economic and Health Insights (Gapminder)", className="mt-4 mb-4 text-center"),

    dcc.Tabs(id="tabs-example", children=[

        # ------ Tab 1: Choropleth ------
        dcc.Tab(label="Global Life Expectancy (Choropleth Map)", children=[
            html.Br(),
            html.P("Explore global life expectancy by selecting a year."),
            dcc.Slider(
                id="year-slider",
                min=min(years),
                max=max(years),
                step=5,
                value=2007,
                marks={str(year): str(year) for year in years},
            ),
            dcc.Graph(id="choropleth-map", style={"height": "600px"}),
            html.Br(),
        ]),

        # ------ Tab 2: Interactive Charts ------
        dcc.Tab(label="GDP & Life Expectancy Trends", children=[
            html.Br(),
            html.P("Filter by continent:"),
            dcc.Dropdown(
                id="continent-dropdown",
                options=[{"label": c, "value": c} for c in continents],
                value="Asia",
                clearable=False,
            ),
            dbc.Row([
                dbc.Col(dcc.Graph(id="life-expectancy-line"), width=6),
                dbc.Col(dcc.Graph(id="gdp-bar-chart"), width=6),
            ], className="mb-4"),
        ]),

        # ------ Tab 3: Animated GDP Over Time ------
        dcc.Tab(label="GDP Growth Over Time (Animated)", children=[
            html.Br(),
            html.P("Click Play to animate GDP per capita changes over time."),
            dcc.Graph(id="animated-gdp"),
        ]),
    ]),
], fluid=True)

# -----------------------------------------------------------
# 4) Callbacks for Interactivity
# -----------------------------------------------------------

# Callback: Update Choropleth Map based on Year Selection
@app.callback(
    Output("choropleth-map", "figure"),
    Input("year-slider", "value")
)
def update_choropleth(selected_year):
    df_filtered = gapminder[gapminder["year"] == selected_year]
    fig = px.choropleth(
        df_filtered,
        locations="iso_alpha",
        color="lifeExp",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Plasma,
        projection="orthographic",
        title=f"Life Expectancy by Country ({selected_year})",
        # Set the range from 0 to 90 so the color scale remains constant
        range_color=[0, 90]
    )
    return fig


# Callback: Update Line Chart & Bar Chart based on Continent Selection
@app.callback(
    [Output("life-expectancy-line", "figure"),
     Output("gdp-bar-chart", "figure")],
    Input("continent-dropdown", "value")
)
def update_charts(selected_continent):
    # Line Chart: Life Expectancy Trends
    df_continent = gapminder[gapminder["continent"] == selected_continent]
    df_life = df_continent.groupby("year", as_index=False)["lifeExp"].mean()
    fig_life = px.line(
        df_life,
        x="year", y="lifeExp",
        title=f"Avg Life Expectancy in {selected_continent} Over Time"
    )

    # Bar Chart: Avg GDP per Country (Latest Year in Dataset)
    df_gdp = df_continent[df_continent["year"] == 2007]
    fig_gdp = px.bar(
        df_gdp,
        x="country", y="gdpPercap",
        title=f"GDP Per Capita by Country ({selected_continent}, 2007)"
    )

    return fig_life, fig_gdp


# Callback: Animated Scatter Plot for GDP Growth
@app.callback(
    Output("animated-gdp", "figure"),
    Input("tabs-example", "value")
)
def update_animated_chart(tab):
    fig = px.scatter(
        gapminder,
        x="gdpPercap", y="lifeExp",
        size="pop", color="continent",
        hover_name="country",
        animation_frame="year",
        animation_group="country",
        log_x=True,
        size_max=55,
        title="GDP per Capita vs. Life Expectancy Over Time",
        # Extend lifeExp axis to 100
        range_y=[0, 100]
    )
    return fig

# -----------------------------------------------------------
# 5) Run Server
# -----------------------------------------------------------
#if __name__ == "__main__":
#    app.run_server(debug=True)
server = app.server  # Expose the Flask app for WSGI