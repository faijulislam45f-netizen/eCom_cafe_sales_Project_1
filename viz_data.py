import pandas as pd
import plotly.express as px

df = pd.read_csv('final_result.csv')

cat_sales = df.groupby('product_category')['total_amount'].sum().reset_index()

fig = px.bar(cat_sales, 
x='product_category', 
y='total_amount', 
title="Total Revenue By Product Category", 
color='product_category', 
template='plotly_dark')
fig.show()
