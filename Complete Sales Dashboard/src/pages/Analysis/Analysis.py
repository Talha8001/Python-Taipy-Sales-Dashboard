# Copyright 2021-2024 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""
A page of the application.
Page content is imported from the Analysis.md file.

Please refer to https://docs.taipy.io/en/latest/manuals/gui/pages for more details.
"""
from taipy.gui import Markdown
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb

# Assuming data is loaded from 'data/modified_supermarkt_sales_plus.csv'
data = pd.read_csv('data/modified_supermarkt_sales_plus.csv')

data['Date'] = pd.to_datetime(data['Date'])
data['Month_Year'] = data['Date'].dt.to_period('M').dt.to_timestamp()
    

def create_perc_fig(df, group_column):
    # Group, sum, and convert to percentage
    df = df.groupby(['Month_Year', group_column])['Total'].sum().unstack(fill_value=0)
    df = df.div(df.sum(axis=1), axis=0).reset_index().melt(id_vars='Month_Year', var_name=group_column, value_name='Percentage')
    df['Percentage'] = (df.loc[:, 'Percentage'].round(3) * 100)
    
    # Create and return the plot
    fig = px.bar(df, x='Month_Year', y='Percentage', color=group_column, title=f"Evolution of Sales by {group_column} over Time", labels={'Percentage': '% of Total'}, text_auto=True)
    return fig

fig_product_line = create_perc_fig(data, 'Product_line')
fig_city = create_perc_fig(data, 'City')
fig_gender = create_perc_fig(data, 'Gender')
fig_customer_type = create_perc_fig(data, 'Customer_type')

import time

def on_change(state, var_name, var_value):
    if var_name in ['city', 'customer_type', 'gender']:
        data = state.data.loc[
            state.data["City"].isin(state.city)
            & state.data["Customer_type"].isin(state.customer_type)
            & state.data["Gender"].isin(state.gender), :
        ]

        state.fig_product_line = create_perc_fig(data, 'Product_line')
        state.fig_city = create_perc_fig(data, 'City')
        state.fig_gender = create_perc_fig(data, 'Gender')
        state.fig_customer_type = create_perc_fig(data, 'Customer_type')


customer_type = ["Normal", "Member"]
gender = ["Male", "Female"]
city = ["Bangkok", "Chiang Mai", "Vientiane", "Luang Prabang"]

with tgb.Page() as Analysis:   
    with tgb.layout(columns="1 1 1"):
        tgb.selector(value="{customer_type}", lov=customer_type, multiple=True, dropdown=True, class_name="fullwidth", label="Customer Type")
        tgb.selector(value="{gender}", lov=gender, multiple=True, dropdown=True, class_name="fullwidth", label="Gender")
        tgb.selector(value="{city}", lov=city,  multiple=True, dropdown=True, class_name="fullwidth", label="City")


    with tgb.layout(columns="1 1"):
        tgb.chart(figure="{fig_customer_type}")
        tgb.chart(figure="{fig_city}")
        tgb.chart(figure="{fig_gender}")
        tgb.chart(figure="{fig_product_line}")
        

