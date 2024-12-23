import os
import time
import streamlit as st
from json import loads
from databricks.sdk import WorkspaceClient

st.header(body="Workflows", divider=True)
st.subheader("Run a Pipeline")
st.write(
    """
    Use this recipe to run a [Delta Live Tables (DLT) pipeline](https://docs.databricks.com/en/delta-live-tables/tutorial-pipelines.html) with UI **input parameters**.
    """
)

w = WorkspaceClient()


def serialize_pipeline_spec(pipeline_spec):
    return {
        key: value
        for key, value in vars(pipeline_spec).items()
        if value is not None and key not in {"id", "as_dict", "from_dict"}
    }


tab_a, tab_b, tab_c = st.tabs(["**Try**", "**Implement**", "**Setup**"])

with tab_a:
    pipeline_id = st.text_input(
        "Pipeline ID", placeholder="4d8b6fbb-9f77-4d29-87ea-5c71a53f27"
    )
    parameters = st.text_area(
        "Pipeline Parameters", 
        placeholder='{"source_path": "/databricks-datasets/iot-stream/", "filter": "eventType = \'open\'"}'
    )

    if st.button("Run"):
        if not pipeline_id.strip() or not parameters.strip():
            st.warning("Fill in all the fields.")
        else:
            spec = w.pipelines.get(pipeline_id).spec
            spec.configuration.update(loads(parameters))

            w.pipelines.update(pipeline_id=pipeline_id, **serialize_pipeline_spec(spec))

            run = w.pipelines.start_update(pipeline_id)
            if run:
                st.link_button("Open Run", f"{w.config.host}/pipelines/{pipeline_id}/updates/{run.update_id}")

with tab_b:
    st.write("#### Parameterize the Pipeline:")
    st.code(
        """
        import dlt
        source_path = spark.conf.get("source_path", "/databricks-datasets/iot-stream/")
        filter_condition = spark.conf.get("filter", "eventType = 'open'")

        @dlt.table(comment="Load and filter data")
        def filtered_data():
            return (
                spark.read.format("json").load(source_path)
                    .filter(filter_condition)
            )
        """
    )

    st.write("#### Update Parameters:")
    st.code(
        """
        from json import loads
        import streamlit as st
        from databricks.sdk import WorkspaceClient


        def serialize_pipeline_spec(pipeline_spec):
            return {
                key: value
                for key, value in vars(pipeline_spec).items()
                if value is not None and key not in {"id", "as_dict", "from_dict"}
            }


        pipeline_id = st.text_input("Pipeline ID")
        parameters = st.text_area("Pipeline Parameters")

        w = WorkspaceClient()
        spec = w.pipelines.get(pipeline_id).spec
        spec.configuration.update(loads(parameters))

        w.pipelines.update(pipeline_id=pipeline_id, **serialize_pipeline_spec(spec))
        """
    )

    st.write("#### Trigger Run:")
    st.code(
        """
        import streamlit as st
        from databricks.sdk import WorkspaceClient

        pipeline_id = st.text_input("Pipeline ID")

        w = WorkspaceClient()

        run = w.pipelines.start_update(pipeline_id)
        if run:
            st.link_button("Open Run", f"{w.config.host}/pipelines/{pipeline_id}/updates/{run.update_id}")
        """
    )

with tab_c:
    st.write(
        "- Ensure your [App principal](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html#how-does-databricks-apps-manage-authorization) `Can Run` the pipeline."
    )
    st.checkbox(
        "[Databricks SDK](https://docs.databricks.com/en/dev-tools/sdk-python.html) installed via `requirements.txt`",
        value=True,
    )
    st.checkbox(
        "[Databricks OAuth](https://docs.databricks.com/dev-tools/api/latest/authentication.html#using-oauth) credentials set in the [environment](https://docs.databricks.com/en/dev-tools/databricks-apps/configuration.html#databricks-apps-environment-variables)",
        value=bool(os.getenv("DATABRICKS_CLIENT_ID") and os.getenv("DATABRICKS_CLIENT_SECRET")),
    )
