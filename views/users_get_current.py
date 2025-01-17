import streamlit as st

st.header(body="Users", divider=True)
st.subheader("Get current user")
st.write(
    "This recipe gets information about the user accessing this Databricks App from their [HTTP headers](https://docs.databricks.com/en/dev-tools/databricks-apps/app-development.html#what-http-headers-are-passed-to-databricks-apps)."
)

tab_a, tab_b, tab_c = st.tabs(["**Try it**", "**Code snippet**", "**Requirements**"])

with tab_a:
    headers = st.context.headers
    st.markdown(
        f"""
        #### User Details

        E-mail: {headers.get("X-Forwarded-Email")}
        
        Username: {headers.get("X-Forwarded-Preferred-Username")}

        IP Address: {headers.get("X-Real-Ip")}
        """
    )
    st.markdown("#### All Headers")
    st.json(headers.to_dict(), expanded=False)

with tab_b:
    st.code(
        """
        import streamlit as st

        headers = st.context.headers
        email = headers.get("X-Forwarded-Email")
        username = headers.get("X-Forwarded-Preferred-Username")
        user  = headers.get("X-Forwarded-User")
        ip = headers.get("X-Real-Ip")

        st.write(f"E-mail: {email}, username: {username}, user: {user}, ip: {ip}")
        """
    )
    st.info(
        """
        #### Extensions
        - Dash, Flask: Use [`request.headers`](https://flask.palletsprojects.com/en/stable/api/#flask.Request.headers) from `flask` Python library.
        - Shiny: Use the [`session$request`](https://shiny.rstudio.com/articles/accessing-network-headers.html) object to extract headers in Shiny R.
        """
    )
