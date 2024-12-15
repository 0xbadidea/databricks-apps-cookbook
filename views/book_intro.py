import streamlit as st

st.markdown("""Welcome!

Ready to serve some **delightful apps** to your users? You're in the right place!  
These recipes will help you quickly build flexible and engaging apps directly on Databricks.  

Cooked up a great recipe to share? [Contribute on GitHub!](https://github.com/databricks) 💡
""")

st.header("🔥 Recipes", divider=True)
recipes = [
    [
        {"label": "Read a Table", "page": "views/tables_read.py"},
        {"label": "Edit a Table", "page": "views/tables_edit.py"},
    ],
    [
        {"label": "Upload a File", "page": "views/volumes_upload.py"},
        {"label": "Download a File", "page": "views/volumes_download.py"},
    ],
    [
        {"label": "Invoke a Model", "page": "views/ml_serving_invoke.py"},
        {"label": "Call Vector Search", "page": "views/ml_vector_search.py"},
        {"label": "Analyze Image", "page": "views/ml_analyze_image.py"},
    ],
    [
        {"label": "Trigger a Workflow", "page": "views/workflows_trigger.py"},
        {"label": "Get Job Results", "page": "views/workflows_get_results.py"},
    ],
    [
        {"label": "Get Current User", "page": "views/users_get_current.py"},
        {"label": "Get User Groups", "page": "views/users_get_groups.py"},
    ],
    [
        {"label": "Connect to Compute", "page": "views/compute_connect.py"},
    ],
]

columns = st.columns(len(recipes))
for col, links in zip(columns, recipes):
    with col:
        with st.container(border=True):
            for link in links:
                st.page_link(page=link["page"], label=link["label"])

st.header("🔗 Useful Links", divider=True)
cola, colb, colc = st.columns(3)

with cola:
    st.markdown("""
    #### Apps Documentation
    [AWS](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html)

    [Azure](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-apps/)

    [Python SDK](https://databricks-sdk-py.readthedocs.io/en/latest/)
    """)

with colb:
    st.markdown("""
    #### More Examples
    [Databricks App Templates](https://github.com/databricks/app-templates)
    """)

with colc:
    st.markdown("""
    #### Blogs
    [Building Data Applications](https://www.linkedin.com/pulse/building-data-applications-databricks-apps-ivan-trusov-6pjwf/)
    """)
