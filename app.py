import streamlit as st

st.set_page_config(layout="wide")
st.logo("assets/logo.svg")
st.title("📖 Databricks Apps Cookbook 🍳")

pages = {
    "": [
        st.Page(
            "views/book_intro.py",
            title="Book Intro",
            icon=":material/skillet_cooktop:",
        ),
    ],
    "Tables": [
        st.Page(
            "views/tables_read.py",
            title="Read a Table",
            icon=":material/table_view:",
        ),
        st.Page(
            "views/tables_edit.py",
            title="Edit a Table",
            icon=":material/edit_document:",
        ),
    ],
    "Volumes": [
        st.Page(
            "views/volumes_upload.py",
            title="Upload a File",
            icon=":material/publish:",
        ),
        st.Page(
            "views/volumes_download.py",
            title="Download a File",
            icon=":material/download:",
        ),
    ],
    "Machine Learning": [
        st.Page(
            "views/ml_serving_invoke.py",
            title="Invoke a Model",
            icon=":material/experiment:",
        ),
        st.Page(
            "views/ml_vector_search.py",
            title="Call Vector Search",
            icon=":material/search:",
        ),
        st.Page(
            "views/ml_analyze_image.py",
            title="Analyze Image",
            icon=":material/add_photo_alternate:",
        )
    ],
    "Workflows": [
        st.Page(
            "views/workflows_trigger.py",
            title="Trigger a Job with Inputs",
            icon=":material/valve:",
        ),
        st.Page(
            "views/workflows_get_results.py",
            title="Get Job Results",
            icon=":material/account_tree:",
        ),
    ],
    "Users": [
        st.Page(
            "views/users_get_current.py",
            title="Get Current User",
            icon=":material/fingerprint:",
        ),
        st.Page(
            "views/users_get_groups.py",
            title="Get User Groups",
            icon=":material/groups:",
        )
    ],
    "Compute": [
        st.Page(
            "views/compute_connect.py",
            title="Connect to Compute",
            icon=":material/lan:",
        )
    ,
    ]
}

pg = st.navigation(pages)
pg.run()
