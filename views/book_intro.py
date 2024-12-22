import streamlit as st
from view_groups import groups

st.markdown("""Welcome!

Ready to serve some **delightful web apps** to your users? You're in the right place!  
These recipes will help you quickly build flexible and engaging apps directly on Databricks.  

Cooked up a great recipe to share? [Contribute on GitHub!](https://github.com/databricks) 💡
""")

st.header("🔥 Recipes", divider=True)
recipes = []
for group in groups:
    if group.get("title"):
        recipe_group = []
        for view in group["views"]:
            recipe_group.append({"label": view.get("label"), "page": view.get("page")})
        recipes.append(recipe_group)

columns = st.columns(len(recipes))
for col, links in zip(columns, recipes):
    with col:
        with st.container(border=True):
            for link in links:
                st.page_link(page=link["page"], label=link["label"])

st.header("🔗 Useful Links", divider=True)
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("""
    #### Apps Documentation
    [AWS](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html)

    [Azure](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-apps/)

    [Python SDK](https://databricks-sdk-py.readthedocs.io/en/latest/)
    """)

with col_b:
    st.markdown("""
    #### More Examples
    [Databricks App Templates](https://github.com/databricks/app-templates)
    """)
    st.markdown("""
    #### Other Supported Frameworks
    [Dash](https://dash.plotly.com/): Create interactive analytical dashboards.  

    [Flask](https://flask.palletsprojects.com/): Build backend-heavy apps with custom APIs.  

    [Shiny](https://shiny.posit.co/): Develop interactive web applications.  

    [Gradio](https://gradio.app/): Quickly prototype machine learning models with user-friendly web interfaces.
    """
    )

with col_c:
    st.markdown("""
    #### Blogs
    [Building Data Applications](https://www.linkedin.com/pulse/building-data-applications-databricks-apps-ivan-trusov-6pjwf/)
    """)
