import os
import io
import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

st.header(body="Workflows", divider=True)
st.subheader("Trigger a Pipeline with Inputs")

tab1, tab2 = st.tabs(["Try It", "Code"])

def trigger_dlt_pipeline(pipeline_id: str, parameters: dict = None):
    try:
        if parameters:
            run = w.pipelines.start_by_id(pipeline_id=pipeline_id, full_refresh=False, parameters=parameters)
        else:
            run = w.pipelines.start_by_id(pipeline_id=pipeline_id, full_refresh=False)
        return {
            "run_id": run.run_id,
            "state": "Triggered",
        }
    except Exception as e:
        return {"error": str(e)}

if "dlt_trigger_success" not in st.session_state:
    st.session_state.dlt_trigger_success = False

with tab1:
    st.info(
        body="""
        To trigger a DLT pipeline, provide the pipeline ID and optional input parameters as key-value pairs.
        Ensure the app's service principal has the necessary permissions to trigger pipelines.
        """,
        icon="ℹ️",
    )

    pipeline_id = st.text_input(
        label="Specify the Pipeline ID",
        placeholder="pipeline-id",
    )

    parameters_input = st.text_area(
        label="Specify Input Parameters (JSON format, optional)",
        placeholder="{\"param1\": \"value1\", \"param2\": \"value2\"}",
    )

    if st.button(label="Trigger DLT Pipeline", icon=":material/play-circle:"):
        if not pipeline_id.strip():
            st.warning("Please specify a valid pipeline ID.", icon="⚠️")
        else:
            try:
                parameters = eval(parameters_input.strip()) if parameters_input.strip() else None
                results = trigger_dlt_pipeline(pipeline_id.strip(), parameters)
                if "error" in results:
                    st.error(f"Error triggering pipeline: {results['error']}", icon="🚨")
                else:
                    st.success("Pipeline triggered successfully", icon="✅")
                    st.json(results)
            except Exception as e:
                st.error(f"Error parsing input parameters: {e}", icon="🚨")

with tab2:
    st.code("""
    from databricks.sdk import WorkspaceClient

    w = WorkspaceClient()

    pipeline_id = "pipeline-id"
    parameters = {
        "param1": "value1",
        "param2": "value2"
    }

    w.pipelines.start_by_id(pipeline_id=pipeline_id, full_refresh=False, parameters=parameters)
    """)


