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

        # TAB 1: About The dataset
        dcc.Tab(label="About Dataset", children=[
            html.Br(),
            html.P("Coffee quality can vary significantly based on its origin, processing methods, and environmental factors. By analysing coffee quality data from different regions, we can uncover patterns that highlight which countries or continents produce the highest-rated coffee, what factors contribute to better flavor and aroma, and how processing methods affect overall taste. This dataset provides valuable insights into aspects like acidity, sweetness, and body, allowing us to compare coffee quality across different origins. Through this analysis, we might discover trends such as whether Arabica or Robusta beans score higher on average, how moisture levels impact quality, or if certain defects are more common in specific regions. Understanding these factors can benefit coffee producers, roasters, and enthusiasts who want to learn more about what makes a great cup of coffee."),
            html.Br(),
            html.H2("Dataset Columns"),
            html.Ul([
                html.Li("REC_ID: Refers to the unique database ID"),
                html.Li("Species: Refers to the botanical species of the coffee beans, such as Arabica or Robusta."),
                html.Li("Continent.of.Origin: Refers to the continent of origin for the respective coffee lot record."),
                html.Li("Country.of.Origin: Refers to the country of origin for the respective coffee lot record."),
                html.Li("Harvest.Year: Refers to the year harvested for the respective coffee lot record."),
                html.Li("Expiration: Refers to the assigned expiration date for the respective coffee lot record."),
                html.Li("Variety: Refers to the specific cultivar or type of coffee plant from which the beans are harvested."),
                html.Li("Color: Refers to the observed color of raw coffee beans. Typically blue, green, or mixed."),
                html.Li("Processing.Method: Describes the method used to process the coffee beans after harvesting."),
                html.Li("Aroma: Refers to the scent or fragrance of the coffee."),
                html.Li("Flavor: Evaluated based on the taste, including any sweetness, bitterness, acidity, and other flavor notes."),
                html.Li("Aftertaste: Refers to the lingering taste that remains in the mouth after swallowing the coffee."),
                html.Li("Acidity: Refers to the brightness or liveliness of the taste."),
                html.Li("Body: Refers to the thickness or viscosity of the coffee in the mouth."),
                html.Li("Balance: Refers to how well the different flavor components of the coffee work together."),
                html.Li("Uniformity: Refers to the consistency of the coffee from cup to cup."),
                html.Li("Clean.Cup: Refers to a coffee that is free of any off-flavors or defects, such as sourness, mustiness, or staleness."),
                html.Li("Sweetness: Refers to the palate of sweetness offered by its taste."),
                html.Li("Moisture: Represents the moisture content of the coffee beans, typically measured as a percentage."),
                html.Li("Quakers: Indicates the presence of quaker beans, which are unripe or defective beans that fail to roast properly."),
                html.Li("Category.One.Defects: Refers to the total number of first-level defects, such as black or sour beans."),
                html.Li("Category.Two.Defects: Refers to the total number of second-level defects, including more severe defects like moldy, insect-damaged, or perforated beans."),
                html.Li("Rec_Cnt (Grouped by datasets only): Refers to the total record count for each of the respective location bins."),
            ]),
        ]),

        # TAB 2: Species of Coffee Used Throughout The Years
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
    df_avg = df_filtered.groupby("Country.of.Origin", as_index=False)["Sweetness"].mean()

    fig = px.choropleth(
        df_avg,
        locations="Country.of.Origin",
        locationmode="country names", 
        color="Sweetness",
        hover_name="Country.of.Origin",
        color_continuous_scale=px.colors.sequential.Plasma,
        projection="orthographic",
        title=f"Sweetness of Coffee Throughout The Year ({selected_year})",
    )

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