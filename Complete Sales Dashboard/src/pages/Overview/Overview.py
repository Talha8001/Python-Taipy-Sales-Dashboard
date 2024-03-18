import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb

# Load the dataset
data = pd.read_csv('data/modified_supermarkt_sales_plus.csv')

def create_pie_figure(data, group_by):
    grouped_data = data.groupby(group_by)['Total'].sum().reset_index()
    grouped_data['Total'] = grouped_data['Total'].round(2)
    fig = px.pie(grouped_data, names=group_by, values='Total', title=f"Sales Performance by {group_by}", hole=0.3)
    return fig

def create_bar_figure(data, group_by):
    sales_over_time = data.groupby(group_by)['Total'].sum().reset_index()
    fig = px.bar(sales_over_time, x=group_by, y='Total', title='Sales Trends Over Time', color='Total')
    return fig

import os

def create_sales_by_city_map(data):
    mapbox_access_token = os.environ.get('MAPBOX_ACCESS_TOKEN')
    px.set_mapbox_access_token(mapbox_access_token)
    city_sales = data.groupby('City').agg({'Total': 'sum', 'Latitude': 'mean', 'Longitude': 'mean'}).reset_index()
    fig = px.scatter_mapbox(city_sales, lat="Latitude", lon="Longitude", size="Total", color="Total", text="City",
                            zoom=5, center={"lat": 18.7, "lon": 98.9}, mapbox_style="dark", title='Total Sales by City', size_max=50)
    fig.update_layout(title={'text': "Total Sales by City", 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

fig_product_line = create_pie_figure(data, 'Product_line')
fig_city = create_pie_figure(data, 'City')
fig_customer_type = create_pie_figure(data, 'Customer_type')

with tgb.Page() as Overview:
    # Sales by City Map
    tgb.chart(figure="{create_sales_by_city_map(data)}", height="600px")
    
    with tgb.layout(columns="1 1 1"):
        tgb.chart(figure="{fig_product_line}")
        tgb.chart(figure="{fig_city}")
        tgb.chart(figure="{fig_customer_type}")

    tgb.chart(figure="{create_bar_figure(data, 'Time')}")
        
    tgb.chart(figure="{create_bar_figure(data, 'Date')}")