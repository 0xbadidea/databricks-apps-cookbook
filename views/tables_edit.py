import os
import pandas as pd
import streamlit as st
from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal


st.header(body="Tables", divider=True)
st.subheader("Edit a Table")
st.write(
    "Streamline your **small** data workflows on Databricks by interactively editing a Catalog table and applying the changed rows directly back."
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


def read_table(table_name) -> pd.DataFrame:
    info = st.empty()
    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        credentials_provider=credential_provider,
    ) as conn:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM {table_name}"
            with info:
                st.info("Calling Databricks SQL...")
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall())
            info.empty()

        return df


def insert_overwrite_table(table_name, df):
    progress = st.empty()
    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        credentials_provider=credential_provider,
    ) as conn:
        with conn.cursor() as cursor:
            rows = list(edited_df.itertuples(index=False))
            values = ",".join([f"({','.join(map(repr, row))})" for row in rows])
            with progress:
                st.info("Calling Databricks SQL...")
            cursor.execute(
                f"INSERT OVERWRITE {table_name} VALUES {values}",
            )
            progress.empty()
            st.success(f"Changes saved")


tab_a, tab_b, tab_c = st.tabs(["**Try**", "**Implement**", "**Setup**"])

with tab_a:
    original_df = pd.DataFrame(
        {
            "customer_id": [f"cust_{i}" for i in range(1, 6)],
            "state": ["CA", "NY", "TX", "FL", "IL"],
            "review": [
                "Great product!",
                "Very satisfied",
                "Could be better",
                "Not what I expected",
                "Excellent service",
            ],
            "review_score": [5, 4, 3, 2, 5],
        }
    )

    table_name = st.text_input(
        "Specify a Catalog table name:",
        placeholder="catalog.schema.table",
        help="Copy the three-level table name from the [Catalog](https://docs.databricks.com/en/data-governance/unity-catalog/index.html#granting-and-revoking-access-to-database-objects-and-other-securable-objects-in-unity-catalog).",
    )
    if table_name:
        original_df = read_table(table_name)
    else:
        st.warning("Using mock data")

    edited_df = st.data_editor(original_df, num_rows="dynamic", hide_index=True)

    df_diff = pd.concat([original_df, edited_df]).drop_duplicates(keep=False)
    if not df_diff.empty:
        if st.button("Save"):
            insert_overwrite_table(table_name, edited_df)

with tab_b:
    st.code(
        """
        import os
        import pandas as pd
        from databricks import sql
        from databricks.sdk.core import Config, oauth_service_principal

        server_hostname = os.getenv("DATABRICKS_HOST")
        client_id = os.getenv("DATABRICKS_CLIENT_ID")
        client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")
        http_path = os.getenv("DATABRICKS_HTTP_PATH")


        def credential_provider():
        config = Config(
            host          = f"https://{server_hostname}",
            client_id     = client_id,
            client_secret = client_secret,
        )
        
        return oauth_service_principal(config)

        def read_table(table_name) -> pd.DataFrame:
            info = st.empty()
            with sql.connect(
                server_hostname=server_hostname,
                http_path=http_path,
                credentials_provider=credential_provider,
                ) as conn:
                    with conn.cursor() as cursor:
                        query = f"SELECT * FROM {table_name}"
                        with info:
                            st.info("Calling Databricks SQL...")
                        cursor.execute(query)
                        df = pd.DataFrame(cursor.fetchall())
                        info.empty()

                    return df


        def insert_overwrite_table(table_name, df):
            progress = st.empty()
            with sql.connect(
                    server_hostname=server_hostname,
                    http_path=http_path,
                    credentials_provider=credential_provider,
            ) as conn:
                with conn.cursor() as cursor:
                    rows = list(edited_df.itertuples(index=False))
                    values = ",".join(
                        [f"({','.join(map(repr, row))})" for row in rows]
                    )
                    with progress:
                        st.info("Calling Databricks SQL...")
                    cursor.execute(
                        f"INSERT OVERWRITE {table_name} VALUES {values}",
                    )
                    progress.empty()
                    st.success(f"Changes saved")

                    
        table_name = "catalog.schema.table_name"

        original_df = read_table(table_name)
        edited_df = st.data_editor(original_df, num_rows="dynamic", hide_index=True)
        insert_overwrite_table(table_name, edited_df)
        """
    )
    st.info(
        """
        #### Extensions
        - [Dash](https://dash.plotly.com/): Replace `st.data_editor` with Dash's [`DataTable`](https://dash.plotly.com/datatable) and implement callbacks for saving changes.
        - [Flask](https://flask.palletsprojects.com/): Use forms to input data and integrate Databricks SQL via Flask-[SQLAlchemy](https://docs.databricks.com/en/dev-tools/sqlalchemy.html).
        - [Shiny](https://shiny.posit.co/): Use [`tableOutput`](https://shiny.posit.co/r/reference/shiny/latest/tableOutput.html) and reactive expressions for dynamic data paired with Databricks SQL.

        Also, check out these guides: 
        - [Databricks SQL Connector for Python](https://docs.databricks.com/integrations/python/sql.html)
        - [A Powerful Spreadsheet in Streamlit](https://blog.streamlit.io/data-analysis-with-mito-a-powerful-spreadsheet-in-streamlit/)
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
        "can `MODIFY` the target table and `Can use` the SQL Warehouse."
    )
    st.checkbox(
        "[Databricks SQL Connector](https://docs.databricks.com/en/dev-tools/python-sql-connector.html) installed via `requirements.txt`",
        value=True,
    )
    st.checkbox(
        "`DATABRICKS_SERVER_HOSTNAME` set in the [environment](https://docs.databricks.com/en/dev-tools/databricks-apps/configuration.html#databricks-apps-environment-variables)",
        value=bool(server_hostname),
    )
    st.checkbox(
        "[Databricks OAuth](https://docs.databricks.com/dev-tools/api/latest/authentication.html#using-oauth) credentials set in the [environment](https://docs.databricks.com/en/dev-tools/databricks-apps/configuration.html#databricks-apps-environment-variables)",
        value=bool(client_id and client_secret),
    )
