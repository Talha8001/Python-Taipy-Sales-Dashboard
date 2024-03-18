<|layout|columns=2 9|gap=50px|
<sidebar|sidebar|
Create and select **scenarios**

<|{selected_scenario}|scenario_selector|>
|sidebar>

<scenario|part|render={selected_scenario}|
# **Prediction**{: .color-primary} page

<|1 1|layout|
<date|
#### Level

A parameter to choose how pessimistic or optimistic your predictions will be.

<|{selected_level}|slider|on_change=on_change_params|not continuous|min=70|max=150|>
|date>

<country|
#### **Holiday**{: .color-primary}

Choose if there is an holiday coming

<|{selected_holiday}|toggle|label=Holiday|on_change=on_change_params|>
|country>
|>

Run your scenario

<|{selected_scenario}|scenario|on_submission_change=on_submission_change|not expanded|>

---------------------------------------

## **Predictions**{: .color-primary} and explorer of data nodes

<|Data Nodes|expandable|
<|1 5|layout|
<|{selected_data_node}|data_node_selector|> 

<|{selected_data_node}|data_node|>
|>
|>

|scenario>
|>
