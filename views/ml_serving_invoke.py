import os
import io
import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
oai = w.serving_endpoints.get_open_ai_client()

st.header(body="Machine Learning", divider=True)
st.subheader("Call a Model")

tab1, tab2 = st.tabs(["Code", "Try It"])

with tab1:
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

def call_llm_endpoint(prompt: str):
    try:
        return oai.complete(prompt=prompt)
    except Exception as e:
        return {"error": str(e)}

with tab2:
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

    if st.button(label="Call LLM Endpoint", icon=":material/robot:"):
        if not prompt_input.strip():
            st.warning("Please enter a valid prompt.", icon="⚠️")
        else:
            result = call_llm_endpoint(prompt_input.strip())
            if "error" in result:
                st.error(f"Error calling LLM endpoint: {result['error']}", icon="🚨")
            else:
                st.success("Response received successfully", icon="✅")
                st.json(result)