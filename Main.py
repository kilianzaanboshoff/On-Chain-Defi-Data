import requests
import pandas as pd
import streamlit as st
import base64
import plotly.express as px

# Make an API request to retrieve TVL data
url = "https://api.llama.fi/chains"
response = requests.get(url)
data = response.json()

# Extract the TVL for each chain
chain_data = []
for chain in data:
    name = chain["name"]
    tvl = chain["tvl"]
    chain_data.append({"name": name, "tvl": tvl})

# Convert the data to a Pandas DataFrame and sort by TVL
df = pd.DataFrame(chain_data).sort_values("tvl", ascending=False)

# Add a title and image
st.title("DeFi Dashboard")

# Display a dividing line
st.markdown("---")

# Allow the user to filter by chain
protocols = ["All"] + sorted(df["name"].unique())
selected_protocol = st.selectbox("Select a chain to filter by:", protocols)

if selected_protocol != "All":
    # Filter the data by the selected chain
    filtered_df = df[df["name"] == selected_protocol]
else:
    # Show the entire table
    filtered_df = df

# Display the filtered data in a table
st.write(filtered_df)

# Allow the user to download the filtered data as a CSV file
csv = filtered_df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="defi_tvl.csv">Download CSV File</a>'
st.markdown(href, unsafe_allow_html=True)

# Display a dividing line
st.markdown("---")

# Create a bar chart to visualize TVL data by chain (top 10 only)
fig = px.bar(df.head(10), x="name", y="tvl", labels={"name": "Chain", "tvl": "TVL"})
fig.update_layout(
    title={
        "text": "Top 10 Chains by TVL",
        "font_size": 40,
        "x": 0.5,
        "y": 0.95,
        "xanchor": "center",
        "yanchor": "top"
    }
)

st.plotly_chart(fig)

# Add a new section for data on pools
st.markdown("---")
st.title("Data on Pools")

# Make an API request to retrieve pool data
pool_url = "https://yields.llama.fi/pools"
pool_response = requests.get(pool_url)
pool_data = pool_response.json()

# Extract the pool data
pool_list = []
for pool in pool_data:
    try:
        pool_dict = eval(pool)
        if "name" not in pool_dict or "symbol" not in pool_dict or "tvl" not in pool_dict:
            continue
        name = pool_dict.get("name")
        symbol = pool_dict.get("symbol")
        tvl = pool_dict.get("tvl")
        apr = pool_dict.get("apy")
        pool_list.append({"name": name, "symbol": symbol, "tvl": tvl, "apr": apr})
    except Exception as e:
        print(f"Error: {e}")
        print(f"Pool data: {pool}")


# Convert the data to a Pandas DataFrame and sort by TVL
pool_df = pd.DataFrame(pool_list).sort_values("tvl", ascending=False)

# Display the data in a table
st.write(pool_df)

# Allow the user to download the data as a CSV
csv = pool_df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="defi_pools.csv">Download CSV File</a>'
st.markdown(href, unsafe_allow_html=True)
