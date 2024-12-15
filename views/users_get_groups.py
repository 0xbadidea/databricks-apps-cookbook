import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

st.header(body="Users", divider=True)
st.subheader("Get User Groups")

tab1, tab2 = st.tabs(["Code snippet", "Try it"])

with tab1:
    current_user = st.context.headers.get("X-Forwarded-Email")
    st.markdown(f"The current user is **{current_user}**.")
    group_name = st.text_input(
        f"Check if {current_user} belongs to this group:",
        placeholder="my_group_name",
    )
    if st.button("Check membership"):
        try:
            user = w.users.get(id=current_user)
            print(user)
        except Exception as e:
            print(e)

    if st.button(f"Get all groups for {current_user}"):
        st.json("test")
