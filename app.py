import streamlit as st
from view_groups import groups

st.set_page_config(layout="wide")
st.logo("assets/logo.svg")
st.title("📖 Databricks Apps Cookbook 🍳")

pages = {}
for group in groups:
    group_views = []
    title = group.get("title", "")
    for view in group["views"]:
        group_views.append(
            st.Page(
                view.get("page"),
                title=view.get("label"),
                icon=view.get("icon"),
            )
        )
        pages[title] = group_views


pg = st.navigation(pages)
pg.run()
