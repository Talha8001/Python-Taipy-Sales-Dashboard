import numpy as np
import pandas as pd 
import string
import random


# Seed for reproducibility
np.random.seed(42)

data = pd.read_csv('data/supermarkt_sales_clean.csv')

def generate_invoice_id(n):
    """Generate n unique Invoice IDs in the format 'XXX-XX-XXXX'."""
    invoice_ids = set()
    while len(invoice_ids) < n:
        # Generate parts of the Invoice ID
        part1 = ''.join(random.choices(string.ascii_uppercase, k=3))
        part2 = ''.join(random.choices(string.digits, k=2))
        part3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        
        # Combine parts into one ID
        invoice_id = f"{part1}-{part2}-{part3}"
        
        # Add to the set of Invoice IDs
        invoice_ids.add(invoice_id)
    
    return list(invoice_ids)

num_entries = 5_000
new_branches = np.random.choice(['A', 'B', 'C', 'D', 'E', 'F'], size=num_entries)
new_invoice = generate_invoice_id(num_entries)
new_products = np.random.choice(list(data['Product line'].unique()), size=num_entries)
new_customer_types = np.random.choice(['Member', 'Normal'], size=num_entries)
new_genders = np.random.choice(['Male', 'Female'], size=num_entries)
new_unit_prices = np.random.uniform(10, 100, size=num_entries)
new_quantities = np.random.randint(1, 10, size=num_entries)
new_tax = new_unit_prices * new_quantities * 0.05
new_totals = new_unit_prices * new_quantities + new_tax
new_cogs = new_unit_prices * new_quantities
new_gross_margin_percentage = np.full(shape=num_entries, fill_value=4.761905)
new_gross_income = new_tax
new_ratings = np.random.uniform(1, 10, size=num_entries)
new_dates = np.random.choice(pd.date_range(start='2021-01-01', end='2021-12-31'), size=num_entries)
new_times = [f"{np.random.randint(10, 19)}:{np.random.randint(0, 59):02d}:00" for _ in range(num_entries)]
new_payments = np.random.choice(['Cash', 'Ewallet', 'Credit card'], size=num_entries)


cities_latitudes = {
    'Bangkok': (13.736717, 100.523186),
    'Chiang Mai': (18.796143, 98.979263),
    'Vientiane': (17.974855, 102.630867),
    'Luang Prabang': (19.889271, 102.133453),
}

# Select a city for each new entry and retrieve its latitude
new_cities = np.random.choice(list(cities_latitudes.keys()), size=num_entries)
new_latitudes = np.array([cities_latitudes[city][0] for city in new_cities])
new_longitudes = np.array([cities_latitudes[city][1] for city in new_cities])

# Create DataFrame for additional data
additional_data = pd.DataFrame({
    'Invoice ID': new_invoice,
    'Branch': new_branches,
    'City': new_cities,
    'Customer_type': new_customer_types,
    'Gender': new_genders,
    'Product_line': new_products,
    'Unit price': new_unit_prices,
    'Quantity': new_quantities,
    'Tax 5%': new_tax,
    'Total': new_totals,
    'Date': new_dates,
    'Time': new_times,
    'Payment': new_payments,
    'cogs': new_cogs,
    'gross_margin_percentage': new_gross_margin_percentage,
    'gross_income': new_gross_income,
    'Rating': new_ratings,
    'Latitude': new_latitudes,
    'Longitude': new_longitudes
})

# Concatenate the additional data with the existing dataset
augmented_data = pd.concat([data, additional_data]).reset_index(drop=True)


augmented_data.to_csv('data/modified_supermarkt_sales_plus.csv')