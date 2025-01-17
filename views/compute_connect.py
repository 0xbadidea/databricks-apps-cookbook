import os
import streamlit as st
import pandas as pd
from databricks.connect import DatabricksSession

st.header("Compute", divider=True)
st.subheader("Connect")
st.write(
    """
    This recipe uses [Databricks Connect](https://docs.databricks.com/en/dev-tools/databricks-connect/python/index.html) to execute pre-defined Python or SQL code on a **shared** cluster with UI inputs. 
    """
)
tab_a, tab_b, tab_c = st.tabs(["**Try it**", "**Code snippet**", "**Requirements**"])

server_hostname = os.getenv("DATABRICKS_HOST")


def connect_to_cluster(cluster_id):
    return DatabricksSession.builder.remote(
        host=server_hostname, cluster_id=cluster_id
    ).getOrCreate()


with tab_a:
    cluster_id = st.text_input(
        "Specify cluster ID:",
        placeholder="0709-132523-cnhxf2p6",
        help="Copy a shared Compute [cluster ID](https://docs.databricks.com/en/workspace/workspace-details.html#cluster-url-and-id) to connect to.",
    )

    if cluster_id:
        spark = connect_to_cluster(cluster_id)
        st.success("Connected 🎉!")

    sub_tab_1, sub_tab_2 = st.tabs(["**Python**", "**SQL**"])
    with sub_tab_1:
        input_val = st.number_input(
            "Specify how many data points to generate:",
            min_value=0,
            value=10,
            step=1,
        )
        if cluster_id:
            if st.button("Generate"):
                try:
                    df = spark.range(input_val).toPandas()
                    st.write("Data:")
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"Failed: {e}")

    with sub_tab_2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("### Data A")
            st.dataframe(
                pd.DataFrame({"id": [1, 2, 3], "value": ["A1", "A2", "A3"]}),
                hide_index=True,
            )
        with col_b:
            st.write("### Data B")
            st.dataframe(
                pd.DataFrame({"id": [2, 3, 4], "value": ["B1", "B2", "B3"]}),
                hide_index=True,
            )

        operation = st.selectbox(
            "Choose how to handle these data:",
            ("INNER JOIN", "LEFT JOIN", "FULL OUTER JOIN", "UNION", "EXCEPT"),
        )

        if cluster_id:
            if st.button("Perform"):
                a = "(VALUES (1, 'A1'), (2, 'A2'), (3, 'A3')) AS a(id, value)"
                b = "(VALUES (2, 'B1'), (3, 'B2'), (4, 'B3')) AS b(id, value)"
                if operation in ("INNER JOIN", "LEFT JOIN", "FULL OUTER JOIN"):
                    query = f"SELECT a.id, a.value AS value_a, b.value AS value_b FROM {a} {operation} {b} ON a.id = b.id"
                else:
                    query = f"SELECT * FROM {a} {operation} SELECT * FROM {b}"
                try:
                    result = spark.sql(query)
                    st.write("Output:")
                    st.dataframe(result.toPandas(), hide_index=True)
                except Exception as e:
                    st.error(f"Failed: {e}")

with tab_b:
    st.code(
        """
        import streamlit as st
        from databricks.connect import DatabricksSession

        cluster_id = "0709-132523-cnaxf2p6"
        spark = DatabricksSession.builder.remote(
            host=os.getenv("DATABRICKS_HOST"),
            cluster_id=cluster_id
        ).getOrCreate()

        query = "SELECT 'I\'m a stellar cook!' AS message"
        sql_output = spark.sql(query).toPandas()
        st.dataframe(sql_output)

        result = spark.range(10).toPandas()
        st.dataframe(result)
        """
    )
    st.info(
        """
        #### Extensions
        - [Databricks Connect](https://docs.databricks.com/en/dev-tools/databricks-connect/index.html) also works with Scala, R, and integrates with your local IDE.
        """,
        icon="ℹ️",
    )

with tab_c:
    st.write(
        "- Ensure your [App principal](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html#how-does-databricks-apps-manage-authorization) `Can Attach To` the cluster."
    )
    st.checkbox(
        "[Databricks Connect](https://docs.databricks.com/en/dev-tools/databricks-connect/python/index.html) installed via `requirements.txt`",
        value=True,
    )
    st.checkbox(
        "[Databricks OAuth](https://docs.databricks.com/dev-tools/api/latest/authentication.html#using-oauth) credentials set in the [environment](https://docs.databricks.com/en/dev-tools/databricks-apps/configuration.html#databricks-apps-environment-variables)",
        value=bool(
            os.getenv("DATABRICKS_CLIENT_ID") and os.getenv("DATABRICKS_CLIENT_SECRET")
        ),
    )
