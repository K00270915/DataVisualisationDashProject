import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------
# 1) Loading and Processing My Data
# -----------------------------------------------------------

df = pd.read_csv("data/Coffee_Qlty.csv")

# df.info was done to observe the number of Null values. this was the result:
# #   Column                Non-Null Count  Dtype  
# ---  ------                --------------  -----  
#  0   REC_ID                1339 non-null   int64  
#  1   Species               1339 non-null   object 
#  2   Continent.of.Origin   1338 non-null   object 
#  3   Country.of.Origin     1338 non-null   object 
#  4   Harvest.Year          1279 non-null   float64
#  5   Expiration            1339 non-null   object 
#  6   Variety               1113 non-null   object 
#  7   Color                 1069 non-null   object 
#  8   Processing.Method     1169 non-null   object 
#  9   Aroma                 1339 non-null   float64
#  10  Flavor                1339 non-null   float64
#  11  Aftertaste            1339 non-null   float64
#  12  Acidity               1339 non-null   float64
#  13  Body                  1339 non-null   float64
#  14  Balance               1339 non-null   float64
#  15  Uniformity            1339 non-null   float64
#  16  Clean.Cup             1339 non-null   float64
#  17  Sweetness             1339 non-null   float64
#  18  Moisture              1339 non-null   float64
#  19  Quakers               1339 non-null   int64  
#  20  Category.One.Defects  1339 non-null   int64  
#  21  Category.Two.Defects  1339 non-null   int64  
# dtypes: float64(11), int64(4), object(7)

# Because of this, dropna() was used to get rid of all na values bringing the total varying amount of non 
# empty rows to a consistent amount of  946 non-null rows

df = df.dropna(axis=0, how='any')

species = sorted(df["Species"].unique())
continent = sorted(df["Continent.of.Origin"].unique())
country = sorted(df["Country.of.Origin"].unique())
years = sorted(int(year) for year in df["Harvest.Year"].unique())

# -----------------------------------------------------------
# 2) Create Dash App with Bootstrap Styling
# -----------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server  # Expose Flask app for deployment

# -----------------------------------------------------------
# 3) Layout and Components
# -----------------------------------------------------------
app.layout = dbc.Container([
    html.H2("Data Visualisation Project: An Analysis on Coffee Quality", className="mt-4 mb-4 text-center"),
################################### My Code ###################################

    dcc.Tabs(id="tabs-example", children=[

        # TAB 1: Species of Coffee Used Throughout The Years
        dcc.Tab(label="The Sweetness of Coffee in different regions", children=[
            html.Br(),
            html.P("Here is a visualisation on the sweetness of coffee in different regions throughout the years. Do you notice anything?"),
            
            dcc.Slider(
                id="year-slider",
                min=min(years),
                max=max(years),
                step=1,
                value=2011,
                marks={str(year): str(year) for year in years},
            ),

            dcc.Graph(id="speciesPYMap", style={"height": "600px"}),

            html.Br(),
        ])
    ])



################################### END OF ###################################
################################### JAMES'S CODE ###################################
#    dcc.Tabs(id="tabs-example", children=[

#          # ------ Tab 1: Choropleth ------
#         dcc.Tab(label="Global Life Expectancy (Choropleth Map)", children=[
#             html.Br(),
#             html.P("Explore global life expectancy by selecting a year."),
#             dcc.Slider(
#                 id="year-slider",
#                 min=min(years),
#                 max=max(years),
#                 step=5,
#                 value=2007,
#                 marks={str(year): str(year) for year in years},
#             ),
#             dcc.Graph(id="choropleth-map", style={"height": "600px"}),
#             html.Br(),
#         ]),

#         # ------ Tab 2: Interactive Charts ------
#         dcc.Tab(label="GDP & Life Expectancy Trends", children=[
#             html.Br(),
#             html.P("Filter by continent:"),
#             dcc.Dropdown(
#                 id="continent-dropdown",
#                 options=[{"label": c, "value": c} for c in continents],
#                 value="Asia",
#                 clearable=False,
#             ),
#             dbc.Row([
#                 dbc.Col(dcc.Graph(id="life-expectancy-line"), width=6),
#                 dbc.Col(dcc.Graph(id="gdp-bar-chart"), width=6),
#             ], className="mb-4"),
#         ]),

#         # ------ Tab 3: Animated GDP Over Time ------
#         dcc.Tab(label="GDP Growth Over Time (Animated)", children=[
#             html.Br(),
#             html.P("Click Play to animate GDP per capita changes over time."),
#             dcc.Graph(id="animated-gdp"),
#         ]),
#     ]),
################################### END OF ###################################


], fluid=True)



# -----------------------------------------------------------
# 4) Callbacks for Interactivity
# -----------------------------------------------------------
################################### MY CALLBACKS ###################################

# Callback: Calback For Updating Coffee Type Map based on Year Selection

@app.callback(
    Output("speciesPYMap", "figure"),
    Input("year-slider", "value")
)
def updateSpeciesPYMap(selected_year):
    df_filtered = df[df["Harvest.Year"].astype(int) == selected_year]
    fig = px.choropleth(
        df_filtered,
        locations="Country.of.Origin",
        locationmode="country names", 
        color="Sweetness",
        hover_name="Country.of.Origin",
        color_continuous_scale=px.colors.sequential.Plasma,
        projection="orthographic",
        title=f"Sweetness of Coffee Throughout The Year ({selected_year})",
    )
    print(df_filtered[["Country.of.Origin", "Species"]])
    print(df["Harvest.Year"].unique())  # See available years

    return fig
################################### END OF ###################################
################################### JAMES'S CALLBACKS ###################################
# # Callback: Update Choropleth Map based on Year Selection
# @app.callback(
#     Output("choropleth-map", "figure"),
#     Input("year-slider", "value")
# )
# def update_choropleth(selected_year):
#     df_filtered = gapminder[gapminder["year"] == selected_year]
#     fig = px.choropleth(
#         df_filtered,
#         locations="iso_alpha",
#         color="lifeExp",
#         hover_name="country",
#         color_continuous_scale=px.colors.sequential.Plasma,
#         projection="orthographic",
#         title=f"Life Expectancy by Country ({selected_year})",
#         # Set the range from 0 to 90 so the color scale remains constant
#         range_color=[0, 90]
#     )
#     return fig


# # Callback: Update Line Chart & Bar Chart based on Continent Selection
# @app.callback(
#     [Output("life-expectancy-line", "figure"),
#      Output("gdp-bar-chart", "figure")],
#     Input("continent-dropdown", "value")
# )
# def update_charts(selected_continent):
#     # Line Chart: Life Expectancy Trends
#     df_continent = gapminder[gapminder["continent"] == selected_continent]
#     df_life = df_continent.groupby("year", as_index=False)["lifeExp"].mean()
#     fig_life = px.line(
#         df_life,
#         x="year", y="lifeExp",
#         title=f"Avg Life Expectancy in {selected_continent} Over Time"
#     )

#     # Bar Chart: Avg GDP per Country (Latest Year in Dataset)
#     df_gdp = df_continent[df_continent["year"] == 2007]
#     fig_gdp = px.bar(
#         df_gdp,
#         x="country", y="gdpPercap",
#         title=f"GDP Per Capita by Country ({selected_continent}, 2007)"
#     )

#     return fig_life, fig_gdp


# # Callback: Animated Scatter Plot for GDP Growth
# @app.callback(
#     Output("animated-gdp", "figure"),
#     Input("tabs-example", "value")
# )
# def update_animated_chart(tab):
#     fig = px.scatter(
#         gapminder,
#         x="gdpPercap", y="lifeExp",
#         size="pop", color="continent",
#         hover_name="country",
#         animation_frame="year",
#         animation_group="country",
#         log_x=True,
#         size_max=55,
#         title="GDP per Capita vs. Life Expectancy Over Time",
#         # Extend lifeExp axis to 100
#         range_y=[0, 100]
#     )
#     return fig
################################### END OF ###################################
# -----------------------------------------------------------
# 5) Run Server
# -----------------------------------------------------------
#if __name__ == "__main__":
#    app.run_server(debug=True)
server = app.server  # Expose the Flask app for WSGI