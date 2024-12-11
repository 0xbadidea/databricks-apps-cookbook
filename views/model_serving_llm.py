import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
oai = w.serving_endpoints.get_open_ai_client()

st.header(body="Work with model serving", divider=True)

st.subheader("Call an LLM endpoint")

tab1, tab2 = st.tabs(["Code snippet", "Try it"])

with tab1:
    pass

with tab2:
    pass
