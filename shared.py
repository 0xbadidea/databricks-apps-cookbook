import os
import streamlit as st
import pandas as pd
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import ExecuteStatementRequestOnWaitTimeout

assert os.getenv(
    "DATABRICKS_WAREHOUSE_ID"
), "DATABRICKS_WAREHOUSE_ID must be set in app.yaml."

ws = WorkspaceClient(host=os.getenv("DATABRICKS_HOST"))


def execute_query(query):
    try:
        response = ws.statement_execution.execute_statement(
            query,
            warehouse_id=os.getenv("DATABRICKS_WAREHOUSE_ID"),
            wait_timeout="30s",
            on_wait_timeout=ExecuteStatementRequestOnWaitTimeout.CANCEL,
        )

        if response.result:
            data_array = response.result.data_array
            column_names = [col.name for col in response.manifest.schema.columns]
            df = pd.DataFrame(data_array, columns=column_names)
            return df
        else:
            st.warning("Query did not return any results.")
            return pd.DataFrame()

    except Exception as e:
        st.error(f"An error occurred while executing the query: {e}")
        return pd.DataFrame()
