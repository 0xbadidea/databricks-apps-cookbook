import streamlit as st

st.markdown("""
### Welcome to the Databricks Apps Cookbook!
            
These recipes will have you serve some tasty apps to your users in no time. Have a great recipe to share? Please raise a pull request on GitHub!
""")

st.header(body="Recipes", divider=True)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("Tables")
        st.page_link(
            page="views/tables_read.py",
            label="Read from a table",
            icon=":material/table_view:",
        )
        st.page_link(
            page="views/tables_write.py",
            label="Write to a table",
            icon=":material/table_view:",
        )

with col2:
    with st.container(border=True):
        st.markdown("### Volumes")
        st.page_link(
            page="views/volumes_upload.py",
            label="Upload a file",
            icon=":material/folder_open:",
        )
        st.page_link(
            page="views/volumes_download.py",
            label="Download a file",
            icon=":material/folder_open:",
        )

with col3:
    with st.container(border=True):
        st.subheader("Model serving")
        st.page_link(
            page="views/model_serving_llm.py",
            label="Call an LLM enpoint",
            icon=":material/experiment:",
        )

st.header(body="Links", divider=True)

cola, colb, colc = st.columns(3)

with cola:
    st.markdown("""
    #### Documentation
    * [Databricks Apps (AWS)](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html)
    * [Databricks Apps (Azure)](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-apps/)
    * [Databricks SDK for Python](https://databricks-sdk-py.readthedocs.io/en/latest/)
    """)

with colb:
    st.markdown("""
    #### Repositories
    * [databricks / app-templates](https://github.com/databricks/app-templates)
    """)

with colc:
    st.markdown("""
    #### Blogs
    * [Building data applications with Databricks Apps](https://www.linkedin.com/pulse/building-data-applications-databricks-apps-ivan-trusov-6pjwf/)
    """)
