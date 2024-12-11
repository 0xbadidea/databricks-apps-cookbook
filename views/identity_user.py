import streamlit as st

st.header(body="Identity, users, and groups", divider=True)

st.subheader("Get current user information")

tab1, tab2 = st.tabs(["Code snippet", "Try it"])

with tab1:
    st.markdown(
        "This code snipped gets information about the user currently accessing this Databricks App extracted from the [HTTP headers contained in the request to the app](https://docs.databricks.com/en/dev-tools/databricks-apps/app-development.html#what-http-headers-are-passed-to-databricks-apps)."
    )

    st.code("""
    import streamlit as st
            
    email = st.context.headers.get('X-Forwarded-Email')
    username = st.context.headers.get('X-Forwarded-Preferred-Username')
    user  = st.context.headers.get('X-Forwarded-User')
    ip = st.context.headers.get('X-Real-Ip')
    """)


with tab2:
    st.markdown(f"""
                #### User information

                **Email address**: {st.context.headers.get("X-Forwarded-Email")}

                **Username**: {st.context.headers.get("X-Forwarded-Preferred-Username")}

                **User**: {st.context.headers.get("X-Forwarded-User")}

                **IP address**: {st.context.headers.get("X-Real-Ip")}
                """)

    st.markdown("#### All headers")
    st.json(st.context.headers.to_dict())
