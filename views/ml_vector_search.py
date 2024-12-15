import os
import io
import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

st.header(body="Machine Learning", divider=True)
st.subheader("Call Vector Search")

tab2, tab1 = st.tabs(["Try It", "Code"])

with tab1:
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

def get_embedding(text: str):
    try:
        return w.mosaic.get_embedding(text=text)
    except Exception as e:
        return {"error": str(e)}

def load_data_into_index(index_name: str, data: list):
    try:
        w.mosaic.load_data(index=index_name, data=data)
        return {"status": "Data loaded successfully"}
    except Exception as e:
        return {"error": str(e)}

with tab2:
    st.info(
        body="""
        Use Mosaic AI capabilities to:
        1. Generate embeddings for textual data.
        2. Load data into a direct query index for vector search.
        """,
        icon="ℹ️",
    )

    text_input = st.text_input(
        label="Enter text to generate embedding",
        placeholder="Sample text to embed",
    )

    if st.button(label="Generate Embedding", icon=":material/memory:"):
        if not text_input.strip():
            st.warning("Please enter valid text.", icon="⚠️")
        else:
            result = get_embedding(text_input.strip())
            if "error" in result:
                st.error(f"Error generating embedding: {result['error']}", icon="🚨")
            else:
                st.success("Embedding generated successfully", icon="✅")
                st.json(result)

    index_name = st.text_input(
        label="Specify the Index Name",
        placeholder="example-index",
    )

    data_input = st.text_area(
        label="Specify Data to Load (JSON format)",
        placeholder="[{\"id\": \"1\", \"text\": \"Sample document\", \"embedding\": [0.1, 0.2, 0.3]}]",
    )

    if st.button(label="Load Data into Index", icon=":material/database:"):
        if not index_name.strip():
            st.warning("Please specify a valid index name.", icon="⚠️")
        elif not data_input.strip():
            st.warning("Please specify data to load.", icon="⚠️")
        else:
            try:
                data = eval(data_input.strip())
                result = load_data_into_index(index_name.strip(), data)
                if "error" in result:
                    st.error(f"Error loading data: {result['error']}", icon="🚨")
                else:
                    st.success("Data loaded into index successfully", icon="✅")
                    st.json(result)
            except Exception as e:
                st.error(f"Error parsing input data: {e}", icon="🚨")
