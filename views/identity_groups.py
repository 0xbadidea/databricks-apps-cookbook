import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

st.header(body="Identity, users, and groups", divider=True)

st.subheader("Check group membership")

tab1, tab2 = st.tabs(["Code snippet", "Try it"])

with tab1:
    # current_user = st.context.headers.get("X-Forwarded-Email")
    current_user = "pascal.vogel@databricks.com"
    st.markdown(f"The current user is **{current_user}**.")
    group_name = st.text_input(
        f"Check if {current_user} is a member of the following group:",
        placeholder="my_group_name",
    )
    if st.button("Check membership"):
        try:
            user = w.users.get(id="pascal.vogel@databricks.com")
            print(user)
        except Exception as e:
            print(e)

    if st.button(f"Get all groups for {current_user}"):
        st.json("test")
