import os
import streamlit as st
import pandas as pd
from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal

st.header(body="Tables", divider=True)
st.subheader("Read a Table")

tab1, tab2 = st.tabs(["Try It", "Code"])

with tab1:
    databricks_host = os.getenv("DATABRICKS_HOST")
    databricks_client_id = os.getenv("DATABRICKS_CLIENT_ID")
    databricks_client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")
    databricks_http_path = os.getenv("DATABRICKS_HTTP_PATH")

    assert databricks_http_path, "DATABRICKS_HTTP_PATH must be set in app.yaml."

    def credential_provider():
        config = Config(
            host=databricks_host,
            client_id=databricks_client_id,
            client_secret=databricks_client_secret,
        )
        return oauth_service_principal(config)

    table_name = st.text_input("Specify a three-level Unity Catalog table name (i.e., catalog.schema.table_name):")

    if table_name:
        try:
            with sql.connect(
                server_hostname=databricks_host,
                http_path=databricks_http_path,
                credentials_provider=credential_provider(),
            ) as conn:
                query = f"SELECT * FROM {table_name}"
                data = pd.read_sql(query, conn)
                st.write(f"Data from table: `{table_name}`")
                st.dataframe(data)
        except Exception as e:
            st.error(f"Failed to load table {table_name}: {e}")

with tab2:
    st.markdown(
        """This code snippet reads a table from the Databricks Unity Catalog. Provide the fully qualified table name in the format `catalog.schema.table_name`."""
    )

    st.code("""
    import os
    import pandas as pd
    from databricks import sql

    databricks_host = os.getenv("DATABRICKS_HOST")
    databricks_http_path = os.getenv("DATABRICKS_HTTP_PATH")

    table_name = "catalog.schema.table_name"

    with sql.connect(
        server_hostname=databricks_host,
        http_path=databricks_http_path,
    ) as conn:
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, conn)
        print(data)
    """)
