import streamlit as st

st.header(body="Users", divider=True)
st.subheader("Get Current User")

tab1, tab2 = st.tabs(["Implement", "Try"])

with tab1:
    st.markdown(
        "This code snipped gets information about the user currently accessing this Databricks App extracted from their [HTTP headers](https://docs.databricks.com/en/dev-tools/databricks-apps/app-development.html#what-http-headers-are-passed-to-databricks-apps)."
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
                #### User Details

                **E-mail**: {st.context.headers.get("X-Forwarded-Email")}
                
                **Username**: {st.context.headers.get("X-Forwarded-Preferred-Username")}

                **User**: {st.context.headers.get("X-Forwarded-User")}

                **IP Address**: {st.context.headers.get("X-Real-Ip")}
                """)

    st.markdown("#### All Headers")
    st.json(st.context.headers.to_dict())
