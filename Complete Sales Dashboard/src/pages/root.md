# Sales **Dashboard**{: .color-primary}

<|1 1 1|layout|
<total_sales|
# **Total**{: .color-primary} sales:
### US $ <|{int(data["Total"].sum())}|text|raw|>
|total_sales>

<average_rating|
# Average **Rating**{: .color-primary}:
### <|{round(data["Rating"].mean(), 1)}|text|raw|>
|average_rating>

<average_sale|
# Average **Sales**{: .color-primary}:
### US $ <|{round(data["Total"].mean(), 2)}|text|raw|>
|average_sale>
|>

<center>
<|navbar|>
</center>

<|Data|expandable|expanded=False|
<|{data}|table|>
|>

