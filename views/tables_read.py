import os
import streamlit as st
import pandas as pd
from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal

st.header(body="Tables", divider=True)
st.subheader("Read a Table")
st.write(
    "This recipe retrieves a Catalog table using [Databricks SQL](https://docs.databricks.com/integrations/python/sql.html)."
)

server_hostname = os.getenv("DATABRICKS_HOST")
client_id = os.getenv("DATABRICKS_CLIENT_ID")
client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")
http_path = os.getenv("DATABRICKS_HTTP_PATH")


def credential_provider():
    config = Config(
        host=f"https://{server_hostname}",
        client_id=client_id,
        client_secret=client_secret,
    )
    return oauth_service_principal(config)


def read_table(table_name):
    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        credentials_provider=credential_provider,
    ) as conn:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            return pd.DataFrame(cursor.fetchall())


tab_a, tab_b, tab_c = st.tabs(["**Try**", "**Implement**", "**Setup**"])

with tab_a:
    table_name = st.text_input(
        "Specify a Catalog table name:",
        placeholder="catalog.schema.table",
        help="Copy the three-level table name from the [Catalog](https://docs.databricks.com/en/data-governance/unity-catalog/index.html#granting-and-revoking-access-to-database-objects-and-other-securable-objects-in-unity-catalog).",
    )
    if table_name:
        df = read_table(table_name)
        st.dataframe(df)

with tab_b:
    st.code(
        """
        import os
        import pandas as pd
        import streamlit as st
        from databricks import sql
        from databricks.sdk.core import Config, oauth_service_principal

        server_hostname = os.getenv("DATABRICKS_HOST")
        client_id = os.getenv("DATABRICKS_CLIENT_ID")
        client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")
        http_path = os.getenv("DATABRICKS_HTTP_PATH")

        def credential_provider():
            config = Config(
                host=f"https://{server_hostname}",
                client_id=client_id,
                client_secret=client_secret,
            )
            return oauth_service_principal(config)

        def read_table(table_name):
            with sql.connect(
                server_hostname=server_hostname,
                http_path=http_path,
                credentials_provider=credential_provider,
            ) as conn:
                with conn.cursor() as cursor:
                    query = f"SELECT * FROM {table_name}"
                    cursor.execute(query)
                    return pd.DataFrame(cursor.fetchall())

        table_name = st.text_input("Specify a Catalog table name:", placeholder="catalog.schema.table")
        if table_name:
            df = read_table(table_name)
            st.dataframe(df)
        """
    )
    st.info(
        """
        #### Extensions
        Check out these guides:
        - [Databricks SQL Connector for Python](https://docs.databricks.com/en/dev-tools/python-sql-connector.html)
        - [Use SQLAlchemy with Databricks](https://docs.databricks.com/en/dev-tools/sqlalchemy.html): It enables the use of Pandas' [`to_sql`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html) and [`read_sql`](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html). Keep in mind, however, the App service principal access token can't be generated.
        """,
        icon="ℹ️",
    )

with tab_c:
    st.write(
        "- Ensure `DATABRICKS_HTTP_PATH`, i.e., **your** [SQL Warehouse endpoint](https://docs.databricks.com/en/compute/sql-warehouse/create.html), is set in [`app.yaml`](https://docs.databricks.com/en/dev-tools/databricks-apps/configuration.html#databricks-apps-environment-variables)",
        value=bool(http_path),
    )
    st.write(
        "- Ensure the [App principal](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html#how-does-databricks-apps-manage-authorization) "
        "can `SELECT` from the target table and `Can use` the SQL Warehouse."
    )
    st.checkbox(
        "[Databricks SQL Connector](https://docs.databricks.com/en/dev-tools/python-sql-connector.html) installed via `requirements.txt`",
        value=True,
    )
    st.checkbox(
        "`DATABRICKS_HOST` set in the [environment](https://docs.databricks.com/en/dev-tools/databricks-apps/configuration.html#databricks-apps-environment-variables)",
        value=bool(server_hostname),
    )
    st.checkbox(
        "[Databricks OAuth](https://docs.databricks.com/dev-tools/api/latest/authentication.html#using-oauth) credentials set in the [environment](https://docs.databricks.com/en/dev-tools/databricks-apps/configuration.html#databricks-apps-environment-variables)",
        value=bool(client_id and client_secret),
    )
