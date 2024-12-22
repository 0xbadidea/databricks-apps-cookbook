import os
import streamlit as st
import pandas as pd
from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal

st.header(body="Tables", divider=True)
st.subheader("Read a Table")
st.write("This recipe fetches and displays a Catalog table using Python SQL.")
tab_a, tab_b, tab_c = st.tabs(["Try It", "Code", "Troubleshoot"])

databricks_host = os.getenv("DATABRICKS_HOST")
databricks_client_id = os.getenv("DATABRICKS_CLIENT_ID")
databricks_client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")
databricks_http_path = os.getenv("DATABRICKS_HTTP_PATH")

def credential_provider():
    config = Config(
        host=databricks_host,
        client_id=databricks_client_id,
        client_secret=databricks_client_secret,
    )
    return oauth_service_principal(config)

with tab_a:
    table_name = st.text_input(
        "Specify a Catalog table name:", placeholder="catalog.schema.table"
    )

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

with tab_b:
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

    st.info(
        """
        Refer to the **[Databricks SQL Connector for Python documentation](https://docs.databricks.com/integrations/python/sql.html)** for further details.
        """
    )

with tab_c:
    st.write("This recipe needs:")
    st.checkbox("`DATABRICKS_HOST` set in the environment", value=bool(os.getenv("DATABRICKS_HOST")))
    st.checkbox(
        "`DATABRICKS_HTTP_PATH`, i.e., the **[SQL Warehouse endpoint](https://docs.databricks.com/en/compute/sql-warehouse/create.html)**, set in the environment",
        value=bool(os.getenv("DATABRICKS_HTTP_PATH")),
    )
    st.checkbox(
        "**[Databricks OAuth](https://docs.databricks.com/dev-tools/api/latest/authentication.html#using-oauth)** credentials set in the environment",
        value=bool(os.getenv("DATABRICKS_CLIENT_ID") and os.getenv("DATABRICKS_CLIENT_SECRET")),
    )
    st.write("Ensure the app has **[permissions](https://docs.databricks.com/en/dev-tools/databricks-apps/app-development.html#app-permissions)** to access the target Catalog table.")
