import streamlit as st

st.set_page_config(layout="wide")
st.logo("assets/logo.svg")
st.title("📖 Databricks Apps Cookbook 🍳")

pages = {
    "Start here": [
        st.Page(
            "views/start.py",
            title="Get cooking with Databricks Apps",
            icon=":material/skillet_cooktop:",
        )
    ],
    "Work with tables": [
        st.Page(
            "views/tables_read.py",
            title="Read from a table",
            icon=":material/table_view:",
        ),
        st.Page(
            "views/tables_write.py",
            title="Write to a table",
            icon=":material/table_view:",
        ),
    ],
    "Work with volumes": [
        st.Page(
            "views/volumes_upload.py",
            title="Upload a file",
            icon=":material/folder_open:",
        ),
        st.Page(
            "views/volumes_download.py",
            title="Download a file",
            icon=":material/folder_open:",
        ),
    ],
    "Work with model serving": [
        st.Page(
            "views/model_serving_llm.py",
            title="Call a LLM",
            icon=":material/experiment:",
        )
    ],
    # "Work with workflows": [
    #     st.Page(
    #         "views/workflows_trigger.py",
    #         title="Trigger workflow with inputs",
    #         icon=":material/account_tree:",
    #     ),
    #     st.Page(
    #         "views/workflows_get_results.py",
    #         title="Get workflow results",
    #         icon=":material/account_tree:",
    #     ),
    # ],
    "Identity, users, and groups": [
        st.Page(
            "views/identity.py",
            title="Get current user",
            icon=":material/fingerprint:",
        )
    ],
    # "Work with vector search": [
    #     st.Page(
    #         "views/vector_search.py",
    #         title="Working with vector search",
    #         icon=":material/search:",
    #     ),
    # ],
    # "Work with clusters": [
    #     st.Page(
    #         "views/cluster.py",
    #         title="Working with clusters",
    #         icon=":material/host:",
    #     )
    # ],
}

pg = st.navigation(pages)
pg.run()
