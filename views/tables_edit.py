from os import getenv
import pandas as pd
from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal
import streamlit as st

st.header(body="Tables", divider=True)
st.subheader("Edit a Table")

assert getenv("DATABRICKS_HTTP_PATH"), "DATABRICKS_HTTP_PATH must be set in app.yaml."

def credential_provider():
    """Provide OAuth credentials for Databricks connection."""
    config = Config(
        host=getenv("DATABRICKS_HOST"),
        client_id=getenv("DATABRICKS_CLIENT_ID"),
        client_secret=getenv("DATABRICKS_CLIENT_SECRET"),
    )
    return oauth_service_principal(config)

# Default mock data
data = pd.DataFrame({
    "customer_id": [f"cust_{i}" for i in range(1, 6)],
    "state": ["CA", "NY", "TX", "FL", "IL"],
    "review": ["Great product!", "Very satisfied", "Could be better", "Not what I expected", "Excellent service"],
    "review_score": [5, 4, 3, 2, 5],
})

table_name = st.text_input("Specify a three-level Unity Catalog table name (i.e., catalog.schema.table_name):")

if table_name:
    try:
        with sql.connect(
            server_hostname=getenv("DATABRICKS_HOST"),
            http_path=getenv("DATABRICKS_HTTP_PATH"),
            credentials_provider=credential_provider(),
        ) as conn:
            query = f"SELECT * FROM {table_name}"
            data = pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Failed to load table {table_name}: {e}")
        st.write("Using mock data instead.")

st.data_editor(data, num_rows="dynamic", hide_index=True)

if st.button("Save Changes"):
    st.write("Changes saved in memory only. Implement persistence as needed.")