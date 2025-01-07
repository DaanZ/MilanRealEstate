import streamlit as st
import pandas as pd

from util import json_read_file

# Sample JSON data
json_data = json_read_file("properties.json")

# Average price per square meter for the area
average_price_per_m2 = 12966

# Convert JSON data to a pandas DataFrame
data = []
for link, details in json_data.items():
    details["link"] = link
    details["price"] = int(details["price"].replace(" ", ""))
    details["m2"] = int(details["m2"].strip())
    details["price/m2"] = int(details["price"] / details["m2"])
    data.append(details)

df = pd.DataFrame(data)

# Add a column for difference from average price per square meter
df["difference_from_avg"] = df["price/m2"] - average_price_per_m2

# Add a column for percentage difference from average price per square meter
df["percentage_diff"] = ((df["difference_from_avg"] / average_price_per_m2) * 100).round(1)

# Sort DataFrame by price per square meter
df = df.sort_values(by="price/m2")

# Streamlit app
st.title("Property Listings")
st.markdown("This app displays properties sorted by price per square meter and their comparison to the area's average price (12,966 price/m²).")

# Prepare DataFrame for display
display_df = df[["name", "rooms", "floor", "m2", "price", "price/m2", "difference_from_avg", "percentage_diff", "link"]]
display_df = display_df.rename(columns={
    "name": "Property Name",
    "rooms": "Rooms",
    "floor": "Floor",
    "m2": "Size (m²)",
    "price": "Total Price (EUR)",
    "price/m2": "Price per m² (EUR/m²)",
    "difference_from_avg": "Difference from Avg (EUR/m²)",
    "percentage_diff": "Percentage Diff (%)",
    "link": "Link"
})

# Convert links to clickable URLs for Streamlit
for i, row in display_df.iterrows():
    display_df.at[i, "Link"] = f"{row['Link']}"

# Display the table
st.dataframe(display_df)
