import os
import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
oai = w.serving_endpoints.get_open_ai_client()

st.header(body="Machine Learning", divider=True)
st.subheader("Call a Model")
st.write(
    """
    This recipe demonstrates how to call a model hosted on a Databricks Serving endpoint.
    You can interact with the endpoint by providing a prompt and retrieving the model's response.
    """
)
tab_a, tab_b, tab_c = st.tabs(["Try", "Implement", "Troubleshoot"])

def call_llm_endpoint(prompt: str):
    try:
        return oai.complete(prompt=prompt)
    except Exception as e:
        return {"error": str(e)}

with tab_a:
    st.info(
        body="""
        Use this tool to interact with an LLM endpoint hosted on Databricks.
        Provide a prompt and get a response from the model.
        """,
        icon="ℹ️",
    )

    prompt_input = st.text_area(
        label="Enter your prompt",
        placeholder="What is the capital of France?",
    )

    if st.button(label="Call LLM Endpoint"):
        if not prompt_input.strip():
            st.warning("Please enter a valid prompt.")
        else:
            result = call_llm_endpoint(prompt_input.strip())
            if "error" in result:
                st.error(f"Error calling LLM endpoint: {result['error']}")
            else:
                st.success("Response received successfully")
                st.json(result)

with tab_b:
    st.code("""
    import os
    from databricks.sdk import WorkspaceClient

    w = WorkspaceClient()
    oai = w.serving_endpoints.get_open_ai_client()

    prompt = "What is the capital of France?"
    try:
        response = oai.complete(prompt=prompt)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error calling LLM endpoint: {e}")
    """)

with tab_c:
    st.write("This recipe needs:")
    st.checkbox("Databricks SDK installed", value=True)
    st.checkbox(
        "Databricks workspace credentials configured via environment variables or a config file",
        value=bool(os.getenv("DATABRICKS_HOST") and os.getenv("DATABRICKS_TOKEN")),
    )
    st.write(
        "Ensure the service principal used has sufficient permissions to access the serving endpoint. For more information, refer to the **[Databricks documentation](https://docs.databricks.com/machine-learning/serving/index.html)**."
    )
