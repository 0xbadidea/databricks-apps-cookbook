import os
import pandas as pd
import streamlit as st
from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal

config = Config(
    host=os.getenv("DATABRICKS_HOST"),
    client_id=os.getenv("DATABRICKS_CLIENT_ID"),
    client_secret=os.getenv("DATABRICKS_CLIENT_SECRET"),
)
http_path = os.getenv("DATABRICKS_HTTP_PATH")

st.header(body="Tables", divider=True)
st.subheader("Edit a Table")
st.write(
    "Streamline your data workflows on Databricks by interactively editing a Catalog table and saving the changes directly back."
)
tab_a, tab_b, tab_c = st.tabs(["Try", "Code", "Troubleshoot"])

def execute_sql_query(query, fetch=True):
    try:
        with sql.connect(
            server_hostname=config.host,
            http_path=http_path,
            credentials_provider=oauth_service_principal(config),
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                if fetch:
                    return pd.DataFrame(
                        cursor.fetchall(), columns=[desc[0] for desc in cursor.description]
                    )
    except Exception as e:
        st.error(
            f"Check your query, connection settings, and permissions. An error occurred: {e}."
        )
    return None

def load_table_data_or_mock(table_name):
    if table_name:
        data = execute_sql_query(f"SELECT * FROM {table_name}")
        if data is not None:
            return data
    st.warning("Using mock data")
    return pd.DataFrame(
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

def save_table_data(table_name, edited_data):
    if table_name:
        rows = [
            (
                ', '.join(row.index),
                ', '.join(f"'{v}'" if isinstance(v, str) else str(v) for v in row.values),
            )
            for _, row in edited_data.iterrows()
        ]
        for columns, values in rows:
            query = (
                f"INSERT INTO {table_name} ({columns}) VALUES ({values}) "
                f"ON DUPLICATE KEY UPDATE {', '.join(f'{col}=VALUES({col})' for col in columns.split(', '))}"
            )
            execute_sql_query(query, fetch=False)
        st.success("Table changes have been saved.")
    else:
        st.warning("To persist changes, specify the table name.")

with tab_c:
    st.write("This recipe needs:")
    st.checkbox("`DATABRICKS_HOST` set in the environment", value=bool(config.host))
    st.checkbox(
        "`DATABRICKS_HTTP_PATH`, i.e., the **[SQL Warehouse endpoint](https://docs.databricks.com/en/compute/sql-warehouse/create.html)**, set in the environment",
        value=bool(http_path),
    )
    st.checkbox(
        "**[Databricks OAuth](https://docs.databricks.com/dev-tools/api/latest/authentication.html#using-oauth)** credentials set in the environment",
        value=bool(config.client_id and config.client_secret),
    )
    st.write(
        "Also, ensure the app has **[permissions](https://docs.databricks.com/en/dev-tools/databricks-apps/app-development.html#app-permissions)** on the target Catalog table."
    )

with tab_a:
    table_name = st.text_input(
        "Specify a Catalog table name:", placeholder="catalog.schema.table"
    )
    data = load_table_data_or_mock(table_name)
    edited_data = st.data_editor(data, num_rows="dynamic", hide_index=True)

    if st.button("Save"):
        save_table_data(table_name, edited_data)

with tab_b:
    st.code(
        """
import os
import pandas as pd
from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal

config = Config(
    host=os.getenv("DATABRICKS_HOST"),
    client_id=os.getenv("DATABRICKS_CLIENT_ID"),
    client_secret=os.getenv("DATABRICKS_CLIENT_SECRET"),
)
http_path = os.getenv("DATABRICKS_HTTP_PATH")

def execute_sql_query(query):
    with sql.connect(
        server_hostname=config.host,
        http_path=http_path,
        credentials_provider=oauth_service_principal(config),
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

query = "SELECT * FROM catalog.schema.table_name"
data = execute_sql_query(query)
print(data)
        """
    )

    st.info(
        """
        While [Streamlit](https://docs.streamlit.io/) is simple and declarative, ideal for building Python data apps, consider the other Databricks Apps-supported frameworks:
        - **[Dash](https://dash.plotly.com/)**: Use for interactive analytical dashboards. Example: Replace `st.data_editor` with Dash's [`DataTable`](https://dash.plotly.com/datatable) and implement callbacks for saving changes.
        - **[Flask](https://flask.palletsprojects.com/)**: Great for backend-heavy apps with custom APIs. Example: Use forms to input data and integrate Databricks SQL via Flask-SQLAlchemy: [Guide](https://docs.databricks.com/en/dev-tools/sqlalchemy.html).
        - **[Shiny](https://shiny.posit.co/)**: Ideal for interactive web apps. Example: Use Shiny's [`tableOutput`](https://shiny.posit.co/r/reference/shiny/latest/tableOutput.html) and reactive expressions for dynamic data paired with Databricks SQL.
        
        Also, check out these guides: 
        - **[Databricks SQL Connector for Python](https://docs.databricks.com/integrations/python/sql.html)**
        - **[A Powerful Spreadsheet in Streamlit](https://blog.streamlit.io/data-analysis-with-mito-a-powerful-spreadsheet-in-streamlit/)**
        """
    )
