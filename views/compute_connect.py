import streamlit as st
from databricks.connect import DatabricksSession
import os

st.title("Connect to Compute")

cluster_id = st.text_input("Cluster ID", help="Provide the Compute cluster ID to connect to.")

if cluster_id:
    try:
        st.subheader("Step 1: Connect to Cluster")
        spark = DatabricksSession.builder.remote(
            host=f"https://{databricks_host}",
            cluster_id=cluster_id
        ).getOrCreate()
        st.success("Cluster connected successfully! 🎉")

        st.subheader("Step 2: Run a SQL Recipe")
        example_query = "SELECT 'I'm a stellar cook!' AS message"
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
