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

# Throughout the code, you will see that 'Harvest.Year' was converted to an integer as the original values in the dataset were floats.

species = sorted(df["Species"].unique())
continent = sorted(df["Continent.of.Origin"].unique())
country = sorted(df["Country.of.Origin"].unique())
years = [2012, 2013, 2014, 2015, 2016, 2017]

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

        # TAB 1: The Sweetness Of Throughout The Years
        dcc.Tab(label="The Sweetness of Coffee in different regions", children=[
            html.Br(),
            html.P("Here is a visualisation on the sweetness of coffee in different regions throughout the years. Do you notice anything?"),
            
            dcc.Slider(
                id="year-slider",
                min=min(years),
                max=max(years),
                step=1,
                value=2012,
                marks={str(year): str(year) for year in years},
            ),

            dcc.Graph(id="speciesPYMap", style={"height": "600px"}),
            html.Br(),
            html.H2("CONTEXT - Sweetness: Refers to the palate of sweetness offered by its taste."),
            html.Br(),
            html.P("OBSERVATION: From looking at this chloropleth map, we can see that South America and Africa generally have higher sweetness levels compared to the other continents. This could be due to the type of coffee species grown in these regions or the processing methods used. To be more country specific, Brazil has consistently high scores across years, which aligns with its reputation as one of the largest and most reliable coffee producers. Overall, however sweetness scores are generally high with the lowest recorded sweetness scores still being relatively high, never dropping below 7.8 (India, 2015). So next questions would be, what factors contribute to the sweetness of coffee and how can one maintain or improve these scores?"),
        ]),

        # TAB 2: The Species of Coffee Used In Different Regions and The Flavour per Continent
        dcc.Tab(label="Coffee Varieties & Types", children=[
            html.Br(),
            html.P("See the popularity of different coffee varieties and types throughout the years."),
            dcc.Dropdown(
                id="continent-dropdown",
                options=[{"label": c, "value": c} for c in continent],
                value="Africa",
                clearable=False,
            ),
            dbc.Row([
                dbc.Col(dcc.Graph(id="coffee-variety-line"), width=6),
                dbc.Col(dcc.Graph(id="flavor-bar-chart"), width=6),
            ], className="mb-4"),
            html.Br(),
            html.H2("CONTEXT"),
            html.P("Variety: Refers to the specific cultivar or type of coffee plant from which the beans are harvested."),
            html.P("Flavor: Evaluated based on the taste, including any sweetness, bitterness, acidity, and other flavor notes."),
            html.P(id="country-count-text"),
            html.Br(),
            html.P("OBSERVATION: With the line chart, we can see the most popular coffee varieties used per continent over the years (Africa: Bourbon / Gesha, Asia: Catimor / Java / undocumented, North America: Caturra / Catuai, South America: Caturra. From what we see in the chloropleth map in the first tab, we can presume that Caturra and Bourbon may be key contributors to the sweetness of coffee in South America and Africa."),
            html.P("The bar chart - representing the year with the most countries recorded in the dataset - further give more context to the flavours of these popular coffee varieties. Africa's average flavour score is the highest, followed by South America, Asia, and North America. Africa's lead is Ethiopia with a flavor score of 8.5 which gives a helpful description of Bourbon having a great blend of sweetness, bitterness, acidity, and other flavor notes. Fluctuations in the flavor scores do not differ significantly between continents, which insinuates that although the sweetness of coffee may vary, the overall flavor of the coffee remains consistent and wouldn't be a deciding factor on what makes coffee a good coffee. So what does?....."),
        ]),

        # ------ Tab 3: Animated Coffee Qualities Over Time ------
        dcc.Tab(label="Quality Of Coffee Over Time (Animated)", children=[
            html.Br(),
            html.P("Click Play to on the below graphs to see how the coffee quality fared in different countries over time."),
            dcc.Graph(id="animated-cq-1"),
            html.Br(),
            dcc.Graph(id="animated-cq-2"),
            html.Br(),
            dcc.Graph(id="animated-cq-3"),
            html.Br(),
            html.H2("CONTEXT"),
            html.P("Body:  Refers to the thickness or viscosity of the coffee in the mouth."),
            html.P("Balance: Refers to how well the different flavor components of the coffee work together."),
            html.P("Aroma: Refers to the scent or fragrance of the coffee."),
            html.P("Acidity: Refers to the brightness or liveliness of the taste."),
            html.Br(),
            html.P("OBSERVATION: With coffee sweetness vs acidity over time, we don't see much changes throughout the years apart from Brazil showing a slight increase in sweetness and acidity in 2016, however there seems to be a slight relationship between sweetness and acidicity with coffee getting sweeter as it gets more acidic. The coffee aroma vs flavor over time shows some countries like Guatemala and Mexico actually regressing in the coffee aroma which also displays a reduction in flavor as well, there for the opposite is true: The stronger the aroma for the coffee, the stronger its flavor. In our final animated chart we can see coffee thickness vs blend over time, with countries like Ethiopia and Nicaragua showing a decrease in thickness and balance over time. This could be due to the processing methods used in these countries."),
        ]),

        # TAB 5: About The dataset
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
        ])
    ])

], fluid=True)

# -----------------------------------------------------------
# 4) Callbacks for Interactivity
# -----------------------------------------------------------

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
        range_color=[7.5, 10]
    )

    return fig

# Callback: Update Line Chart & Bar Chart based on Continent Selection
@app.callback(
    [Output("coffee-variety-line", "figure"),
     Output("flavor-bar-chart", "figure"),
     Output("country-count-text", "children")],
    Input("continent-dropdown", "value")
)
def update_charts(selected_continent):
    df_continent = df[df["Continent.of.Origin"] == selected_continent]
    
    df_species = df_continent.groupby(["Harvest.Year", "Variety"])\
        ["Country.of.Origin"].nunique().reset_index()
    
    fig_variety = px.line(
        df_species,
        x="Harvest.Year", y="Country.of.Origin", color="Variety",
        title=f"Countries Using a Coffee Variety in {selected_continent} Over Time",
        labels={"Country.of.Origin": "Number of Countries", "Harvest.Year": "Year"}
    )
    fig_variety.update_yaxes(range=[0, 6])
    
    df_flavor = df_continent[df_continent["Harvest.Year"] == 2014]\
        .groupby("Country.of.Origin", as_index=False)["Flavor"].mean()
    
    df_2014 = df_continent[df_continent["Harvest.Year"] == 2014]
    df_flavor = df_2014.groupby("Country.of.Origin", as_index=False)["Flavor"].mean()
    fig_flavour = px.bar(
        df_flavor,
        x="Country.of.Origin", y="Flavor",
        title=f"Avg Coffee Flavor Score by Country ({selected_continent}, 2014)",
    )
    fig_flavour.update_yaxes(range=[0, 10])

    num_countries = df_2014["Country.of.Origin"].nunique()
    paragraph_text = f"These values are based on the total of {num_countries} countries recorded in {selected_continent} in 2014."

    return fig_variety, fig_flavour, paragraph_text

    # Callback: Animated Scatter Plots for Coffee Qualities
@app.callback(
    Output("animated-cq-1", "figure"),
    Output("animated-cq-2", "figure"),
    Output("animated-cq-3", "figure"),
    Input("tabs-example", "value")
)
def update_animated_chart(tab):
    fig = px.scatter(
        df,
        x="Sweetness", y="Acidity",
        size="Body", color="Country.of.Origin",
        hover_name="Country.of.Origin",
        animation_frame=years,
        animation_group="Country.of.Origin",
        size_max=55,
        title="Coffee Sweetness vs. Acidity Over Time",
        range_x=[0, 10],
        range_y=[5, 9]
    )

    fig_2 = px.scatter(
        df,
        x="Aroma", y="Flavor",
        size="Acidity", color="Country.of.Origin",
        hover_name="Country.of.Origin",
        animation_frame=years,
        animation_group="Country.of.Origin",
        size_max=55,
        title="Coffee Aroma vs. Flavor Over Time",
        range_x=[5, 9],
        range_y=[5, 9]
    )

    fig_3 = px.scatter(
        df,
        x="Body", y="Balance",
        size="Sweetness", color="Country.of.Origin",
        hover_name="Country.of.Origin",
        animation_frame=years,
        animation_group="Country.of.Origin",
        size_max=55,
        title="Coffee Thickness vs. Blend Over Time",
        range_x=[5, 9],
        range_y=[5, 9]
    )
    return fig, fig_2, fig_3

server = app.server 