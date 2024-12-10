import streamlit as st

st.header("Identity, users, and groups")

st.markdown("""
* How to get headers
* How to check in which groups user is
* https://databricks-sdk-py.readthedocs.io/en/latest/workspace/iam/groups.html
""")

st.code(st.context.headers.to_dict())

st.code(st.context.headers.get("X-Forwarded-Email"))
st.code(st.context.headers.get("X-Forwarded-Preferred-Username"))
st.code(st.context.headers.get("X-Forwarded-User"))
st.code(st.context.headers.get("X-Real-Ip"))