import streamlit as st
from view_groups import groups

st.markdown(
    """
    Welcome!

    Ready to serve some **delightful web apps** to your users? You're in the right place!  
    These recipes will help you quickly build flexible and engaging data apps directly on Databricks.  

    Have a great recipe to share? [Contribute on GitHub](https://github.com/pbv0/databricks-apps-cookbook) 💡!
    """
)

st.header("🔥 Recipes", divider=True)
groups = [group for group in groups if group.get("title")]
columns = st.columns(len(groups))
for col, group in zip(columns, groups):
    with col:
        with st.container(border=True):
            for view in group["views"]:
                st.page_link(page=view["page"], label=view["label"], help=view["help"])

st.header("🔗 Useful Links", divider=True)
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(
        """
        #### Documentation
        - [AWS](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html)
        - [Azure](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-apps/)
        - [Python SDK](https://databricks-sdk-py.readthedocs.io/en/latest/)
        """
    )

with col_b:
    st.markdown(
        """
        #### More Examples
        - [Databricks Apps Templates](https://github.com/databricks/app-templates)

        #### Extensions
        These frameworks are supported by Databricks Apps as well:
        - [Dash](https://dash.plotly.com/): Create interactive analytical dashboards.
        - [Flask](https://flask.palletsprojects.com/): Build backend-heavy apps with custom APIs.  
        - [Shiny](https://shiny.posit.co/): Develop interactive web applications.  
        - [Gradio](https://gradio.app/): Quickly prototype ML models with user-friendly UIs.
        """
    )

with col_c:
    st.markdown(
        """
        #### Highlight Blogs
        - [Building Data Applications](https://www.linkedin.com/pulse/building-data-applications-databricks-apps-ivan-trusov-6pjwf/)
        """
    )
