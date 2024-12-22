import os
import streamlit as st
from databricks.connect import DatabricksSession

st.header(body="Connect to Compute", divider=True)
st.subheader("Run SQL on a Cluster")
st.write(
    """
    This recipe demonstrates how to connect to a Databricks Compute cluster and run SQL queries interactively. 
    Provide the cluster ID to establish a connection and execute a SQL recipe.
    """
)

tab_a, tab_b, tab_c = st.tabs(["Try", "Implement", "Troubleshoot"])

with tab_a:
    cluster_id = st.text_input("Cluster ID", help="Provide the Compute cluster ID to connect to.")

    if cluster_id:
        try:
            st.subheader("Step 1: Connect to Cluster")
            spark = DatabricksSession.builder.remote(
                host=f"https://{os.getenv('DATABRICKS_HOST')}",
                cluster_id=cluster_id
            ).getOrCreate()
            st.success("Cluster connected successfully! 🎉")

            st.subheader("Step 2: Run a SQL Recipe")
            example_query = "SELECT 'I\'m a stellar cook!' AS message"
            query = st.text_area("Here goes your SQL code:", example_query)

            if st.button("Run Recipe"):
                try:
                    # Execute the SQL query
                    df = spark.sql(query)
                    st.write("Recipe Output:")
                    st.dataframe(df.toPandas())
                except Exception as e:
                    st.error(f"Error in the recipe: {e}")
        except Exception as e:
            st.error(f"Failed to connect: {e}")
    else:
        st.info("Please provide the cluster ID to get started.")

with tab_b:
    st.code("""
    import os
    from databricks.connect import DatabricksSession

    cluster_id = "your-cluster-id"

    spark = DatabricksSession.builder.remote(
        host=f"https://{os.getenv('DATABRICKS_HOST')}",
        cluster_id=cluster_id
    ).getOrCreate()

    query = "SELECT 'I\'m a stellar cook!' AS message"

    try:
        df = spark.sql(query)
        print(df.toPandas())
    except Exception as e:
        print(f"Error in the recipe: {e}")
    """)

with tab_c:
    st.write("This recipe needs:")
    st.checkbox("Databricks Connect installed and configured", value=True)
    st.checkbox(
        "Databricks workspace credentials configured via environment variables or a config file",
        value=bool(os.getenv("DATABRICKS_HOST") and os.getenv("DATABRICKS_TOKEN")),
    )
    st.write(
        "Ensure the service principal or user has sufficient permissions to access the cluster. For more information, refer to the **[Databricks Connect documentation](https://docs.databricks.com/dev-tools/databricks-connect.html)**."
    )
