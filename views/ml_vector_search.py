import os
import io
import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
openai_client = w.serving_endpoints.get_open_ai_client()

EMBEDDING_MODEL_ENDPOINT_NAME = "databricks-gte-large-en"

st.header(body="Machine Learning", divider=True)
st.subheader("Run vector search")

tab1, tab2, tab3 = st.tabs(["**Try it**", "**Code snippet**", "**Requirements**"])

# Initialize session state variables
if "vs_endpoint" not in st.session_state:
    st.session_state["vs_endpoint"] = None

if "selected_index_name" not in st.session_state:
    st.session_state["selected_index_name"] = None

# This will store whatever columns the user types in
if "columns_input" not in st.session_state:
    # Default to "url" or an empty string — your choice
    st.session_state["columns_input"] = "url"


def get_embeddings(text):
    try:
        response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL_ENDPOINT_NAME, input=text
        )
        return response.data[0].embedding
    except Exception as e:
        return f"Error generating embeddings: {e}"


def run_vector_search(prompt: str) -> str:
    """Run vector search against the currently selected index."""
    prompt_vector = get_embeddings(prompt)
    if prompt_vector is None or isinstance(prompt_vector, str):
        # If it’s an error string, just return it
        return f"Failed to generate embeddings: {prompt_vector}"

    # Parse the user-defined columns (comma-separated)
    columns_input_str = st.session_state.get("columns_input", "")
    columns_to_fetch = [
        col.strip() for col in columns_input_str.split(",") if col.strip()
    ]

    try:
        query_result = w.vector_search_indexes.query_index(
            index_name=st.session_state.get("selected_index_name"),
            columns=columns_to_fetch,
            query_vector=prompt_vector,
            num_results=3,
        )
        return query_result.result.data_array
    except Exception as e:
        return f"Error during vector search: {e}"


def load_data_into_index(index_name: str, data: list):
    """Optional helper if you want to load data."""
    try:
        w.mosaic.load_data(index=index_name, data=data)
        return {"status": "Data loaded successfully"}
    except Exception as e:
        return {"error": str(e)}


with tab1:
    vs_endpoint_list = w.vector_search_endpoints.list_endpoints()
    endpoint_names = [ep.name for ep in vs_endpoint_list]

    if st.session_state["vs_endpoint"] not in endpoint_names:
        st.session_state["vs_endpoint"] = endpoint_names[0] if endpoint_names else ""

    st.session_state["vs_endpoint"] = st.selectbox(
        label="Vector search endpoints",
        options=endpoint_names,
        index=endpoint_names.index(st.session_state["vs_endpoint"])
        if st.session_state["vs_endpoint"] in endpoint_names
        else 0,
        key="vs_endpoint_key",
    )

    if st.session_state["vs_endpoint"]:
        vs_index_list = w.vector_search_indexes.list_indexes(
            endpoint_name=st.session_state["vs_endpoint"]
        )
        vs_index_names = [idx.name for idx in vs_index_list]

        if st.session_state["selected_index_name"] not in vs_index_names:
            st.session_state["selected_index_name"] = (
                vs_index_names[0] if vs_index_names else ""
            )

        st.session_state["selected_index_name"] = st.selectbox(
            label=f"Vector search indexes for {st.session_state['vs_endpoint']}",
            options=vs_index_names,
            index=vs_index_names.index(st.session_state["selected_index_name"])
            if st.session_state["selected_index_name"] in vs_index_names
            else 0,
            key="selected_index_key",
        )

    st.session_state["columns_input"] = st.text_input(
        label="Columns to retrieve (comma-separated)",
        value=st.session_state["columns_input"],
        key="columns_input_key",
        help="Enter one or more column names present in the vector search index, separated by commas. E.g. id, text, url.",
    )

    text_input = st.text_input(
        label="Enter your search query",
        placeholder="What is Databricks?",
        key="search_query_key",
    )

    if st.button("Run vector search"):
        result = run_vector_search(text_input)
        st.write("Search results:")
        st.write(result)


with tab2:
    st.code("""
    import os
    from databricks.sdk import WorkspaceClient

    w = WorkspaceClient()

    # Get embedding for a text input
    text_input = "Sample text to embed"
    try:
        embedding = w.mosaic.get_embedding(text=text_input)
        print(f"Generated embedding: {embedding}")
    except Exception as e:
        print(f"Error generating embedding: {e}")

    # Load data into direct query index
    data = [{"id": "1", "text": "Sample document", "embedding": [0.1, 0.2, 0.3]}]
    index_name = "example-index"
    try:
        w.mosaic.load_data(index=index_name, data=data)
        print(f"Data loaded into index {index_name}")
    except Exception as e:
        print(f"Error loading data: {e}")
    """)

with tab3:
    st.markdown("""
                To query a vector search index, your app service principal needs the following permissions:
                * `USE CATALOG` on the catalog that contains the vector search index.
                * `USE SCHEMA` on the schema that contains the vector search index.
                * `SELECT` on the vector search index.
                """)
