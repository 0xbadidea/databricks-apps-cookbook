import os
from json import loads
import streamlit as st
import pandas as pd
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

st.header(body="Machine Learning", divider=True)
st.subheader("Invoke a Model")
st.write("""
    This recipe demonstrates how to invoke a model **across classical ML and Large Language (LLMs)**
    hosted on Databricks ML Serving with UI inputs.
""")

tab_a, tab_b, tab_c = st.tabs(["**Try**", "**Implement**", "**Setup**"])

w = WorkspaceClient()

with tab_a:
    endpoints = w.serving_endpoints.list()
    endpoint_names = [endpoint.name for endpoint in endpoints]

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_model = st.selectbox("Select a Serving model:", endpoint_names)
    with col2:
        model_type = st.radio("Model type:", ["LLM", "Classical ML"])

    if model_type == "LLM":
        temperature = st.slider(
            "Select temperature:",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Controls the randomness of the LLM output. Only applicable for chat/completions queries."
        )
        prompt = st.text_area("Enter your prompt:", placeholder="Ask something...")
        if st.button("Invoke LLM"):
            response = w.serving_endpoints.query(
                name=selected_model,
                messages=[
                    ChatMessage(
                        role=ChatMessageRole.SYSTEM, 
                        content="You are a helpful assistant.",
                    ),
                    ChatMessage(
                        role=ChatMessageRole.USER, 
                        content=prompt,
                    ),
                ],
                temperature=temperature,
            )
            st.json(response.as_dict())

    elif model_type == "Classical ML":
        st.info("The model has to be [deployed](https://docs.databricks.com/en/machine-learning/model-serving/create-manage-serving-endpoints.html#create-an-endpoint) to Serving. Request pattern corresponds to the model signature [registered in the Catalog](https://docs.databricks.com/en/machine-learning/manage-model-lifecycle/index.html#train-and-register-unity-catalog-compatible-models).")
        input_value = st.text_area("Enter model input", placeholder='{"feature1": [1.5], "feature2": [2.5]}')
        if st.button("Invoke Model"):
            response = w.serving_endpoints.query(
                name=selected_model, 
                dataframe_records=loads(input_value)
            )
            st.write(response.as_dict())

table = [
    {
        "type": "Classical Models (e.g., scikit-learn, XGBoost)",
        "param": "dataframe_split",
        "description": "JSON-serialized DataFrame in split orientation.",
        "code": """
        ```python
        from databricks.sdk import WorkspaceClient
        import streamlit as st

        w = WorkspaceClient()

        response = w.serving_endpoints.query(
            name="custom-regression-model",
            dataframe_split={
                "columns": ["feature1", "feature2"],
                "data": [[1.5, 2.5]]
            }
        )
        st.json(response.as_dict())
        ```
        """
    },
    {
        "type": "Classical Models (e.g., scikit-learn, XGBoost)",
        "param": "dataframe_records",
        "description": "JSON-serialized DataFrame in records orientation.",
        "code": """
        ```python
        from databricks.sdk import WorkspaceClient
        import streamlit as st

        w = WorkspaceClient()

        response = w.serving_endpoints.query(
            name="custom-regression-model",
            dataframe_records={
                "feature1": [1.5],
                "feature2": [2.5]
            }
        )
        st.json(response.as_dict())
        ```
        """
    },
    {
        "type": "TensorFlow and PyTorch Models",
        "param": "instances",
        "description": "Tensor inputs in row format.",
        "code": """
        ```python
        from databricks.sdk import WorkspaceClient
        import streamlit as st

        w = WorkspaceClient()

        tensor_input = [[1.0, 2.0, 3.0]]
        response = w.serving_endpoints.query(
            name="tensor-processing-model",
            instances=tensor_input,
        )
        st.json(response.as_dict())
        ```
        """
    },
    {
        "type": "TensorFlow and PyTorch Models",
        "param": "inputs",
        "description": "Tensor inputs in columnar format.",
        "code": """
        ```python
        from databricks.sdk import WorkspaceClient
        import streamlit as st

        w = WorkspaceClient()

        tensor_input = {
            "input1": [1.0, 2.0, 3.0],
            "input2": [4.0, 5.0, 6.0],
        }
        response = w.serving_endpoints.query(
            name="tensor-processing-model",
            inputs=tensor_input,
        )
        st.json(response.as_dict())
        ```
        """
    },
    {
        "type": "Completions Models",
        "param": "prompt",
        "description": "Input text for completion tasks.",
        "code": """
        ```python
        from databricks.sdk import WorkspaceClient
        import streamlit as st

        w = WorkspaceClient()

        response = w.serving_endpoints.query(
            name="llm-text-completions-model",
            prompt="Generate a recipe for building scalable Databricks Apps",
            temperature=0.5,
        )
        st.json(response.as_dict())
        ```
        """
    },
    {
        "type": "Chat Models",
        "param": "messages",
        "description": "List of chat messages for conversational models.",
        "code": """
        ```python
        from databricks.sdk import WorkspaceClient
        import streamlit as st
        from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

        w = WorkspaceClient()

        response = w.serving_endpoints.query(
            name="chat-assistant-model",
            messages=[
                ChatMessage(
                    role=ChatMessageRole.SYSTEM, 
                    content="You are a helpful assistant.",
                ),
                ChatMessage(
                    role=ChatMessageRole.USER, 
                    content=prompt,
                ),
            ],
        )
        st.json(response.as_dict())
        ```
        """
    },
    {
        "type": "Embeddings Models",
        "param": "input",
        "description": "Input text for embedding tasks.",
        "code": """
        ```python
        from databricks.sdk import WorkspaceClient
        import streamlit as st

        w = WorkspaceClient()

        response = w.serving_endpoints.query(
            name="embedding-model",
            input="Databricks provides a unified analytics platform.",
        )
        st.json(response.as_dict())
        ```
        """
    }
]

def render_row(column, row):
    with column:
        st.markdown(f"**{row['type']}** accept `{row['param']}`: {row['description']}")
        st.markdown(row['code'])
        st.divider()

with tab_b:
    col_1, col_2 = st.columns(2)
    for i, row in enumerate(table):
        target_col = col_1 if i % 2 == 0 else col_2
        render_row(target_col, row)

    st.info("""
        #### Extensions

        [Gradio](https://gradio.app/guides/quickstart): Enable ML prototyping with pre-built interactive components for models involving images, audio, or video.

        [Dash](https://plotly.com/examples/): Build interactive, data-rich visualizations to explore and analyze the behavior of your ML models in depth.

        [LangChain on Databricks](https://docs.databricks.com/en/large-language-models/langchain.html): Excels at chaining LLM calls, integration with external APIs, and managing conversational contexts.

        Also, check out [Databricks Serving Query API](https://docs.databricks.com/api/workspace/servingendpoints/query). It provides the example responses and optional arguments for the above *Implement* cases.
    """)

with tab_c:
    st.write(
        "- Your workspace needs to be in a [Model Serving-supported region](https://docs.databricks.com/en/machine-learning/model-serving/model-serving-limits.html#regions)."
    )
    st.checkbox(
        "[Databricks SDK](https://docs.databricks.com/en/dev-tools/sdk-python.html) installed via `requirements.txt`",
        value=True,
    )
    st.checkbox(
        "[Databricks OAuth](https://docs.databricks.com/dev-tools/api/latest/authentication.html#using-oauth) credentials set in the [environment](https://docs.databricks.com/en/dev-tools/databricks-apps/configuration.html#databricks-apps-environment-variables)",
        value=bool(os.getenv("DATABRICKS_CLIENT_ID") and os.getenv("DATABRICKS_CLIENT_SECRET")),
    )
    st.write(
        "- Ensure the app has [permissions](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html#how-does-databricks-apps-manage-authorization) on any custom serving endpoint required."
    )
