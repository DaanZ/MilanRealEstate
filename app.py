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
    data.append(details)

df = pd.DataFrame(data)

# Add a column for difference from average price per square meter
df["difference_from_avg"] = df["price/m2"] - average_price_per_m2

# Sort DataFrame by price per square meter
df = df.sort_values(by="price/m2")

# Streamlit app
st.title("Property Listings")
st.markdown("This app displays properties sorted by price per square meter and their comparison to the area's average price (12,966 price/m²).")

# Display the sorted properties
for _, row in df.iterrows():
    st.markdown(f"### [{row['name']}]({row['href']})")
    col1, col2 = st.columns([1,1])
    with col1:
        st.write(f"- **Rooms:** {row['rooms']}")
        st.write(f"- **Floor:** {row['floor']}")
        st.write(f"- **Size:** {row['m2']} m²")

    with col2:
        st.write(f"- **Total Price:** {row['price']} EUR")
        st.write(f"- **Price per m²:** {row['price/m2']:.2f} EUR/m²")
        difference = row["difference_from_avg"]
        if difference > 0:
            st.write(f"- **Above Average:** +{difference:.2f} EUR/m²")
        else:
            st.write(f"- **Below Average:** {difference:.2f} EUR/m²")
    st.write("---")
