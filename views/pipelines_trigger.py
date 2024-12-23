import os
import time
import streamlit as st
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import pipelines

st.header(body="Workflows", divider=True)
st.subheader("Trigger a Pipeline")
st.write(
    """
    Use this app to create and trigger a Delta Live Tables (DLT) pipeline in Databricks. Customize the pipeline with runtime parameters to process event data.
    """
)

w = WorkspaceClient()

def upload_code_to_notebook(notebook_path, code):
    w.workspace.import_workspace(
        path=notebook_path,
        content=code.encode("utf-8"),
        format="SOURCE",
        language="PYTHON",
        overwrite=True
    )

def create_pipeline(pipeline_name):
    notebook_path = f'/Users/{w.current_user.me().user_name}/sdk-{time.time_ns()}'

    notebook_code = '''
    import dlt
    from pyspark.sql.functions import *

    @dlt.table(comment="Load and filter data")
    def filtered_data():
        source_path = spark.conf.get("source_path", "/databricks-datasets/structured-streaming/events")
        filter = spark.conf.get("filter", "eventType = 'open'")

        return (
            spark.read.format("json").load(source_path)
                .filter(filter)
                .select("*", current_timestamp().alias("processed_time"))
        )

    @dlt.table(comment="Count filtered events")
    def event_counts():
        return (
            dlt.read("filtered_data")
                .groupBy("eventType")
                .count()
                .withColumnRenamed("count", "event_count")
        )
    '''

    upload_code_to_notebook(notebook_path, notebook_code)

    created = w.pipelines.create(
        continuous=False,
        name=pipeline_name,
        libraries=[pipelines.PipelineLibrary(notebook=pipelines.NotebookLibrary(path=notebook_path))],
        clusters=[
            pipelines.PipelineCluster(
                label="default",
                serverless=True,
                num_workers=1,
                custom_tags={
                    "cluster_type": "serverless",
                }
            )
        ]
    )

    return created

def trigger_pipeline_run(pipeline_id, source_path, filter_condition):
    run = w.pipelines.trigger(
        pipeline_id=pipeline_id,
        configuration_overrides={
            "source_path": source_path,
            "filter": filter_condition
        }
    )
    return run

tab_a, tab_b, tab_c = st.tabs(["**Try**", "**Implement**", "**Setup**"])

with tab_a:
    pipeline_name = st.text_input("Pipeline Name", f"sdk-{time.time_ns()}")
    source_path = st.text_input("Source Path", "/databricks-datasets/structured-streaming/events")
    filter_condition = st.text_input("Filter", "open")

    if st.button("Trigger Run"):
        if not pipeline_name.strip() or not source_path.strip() or not filter_condition.strip():
            st.warning("Please fill in all required fields.")
        else:
            created_pipeline = create_pipeline(pipeline_name)
            if created_pipeline:
                st.success("Pipeline created successfully!")
                run = trigger_pipeline_run(created_pipeline.pipeline_id, source_path, filter_condition)
                if run:
                    st.success("Pipeline run triggered successfully!")
                    st.markdown(f"[View Pipeline]({w.config.host}/#job/{created_pipeline.pipeline_id})")
                else:
                    st.error("Failed to trigger pipeline run.")
            else:
                st.error("An error occurred while creating the pipeline.")

with tab_b:
    st.code("""
    import os
    import time
    import streamlit as st
    from databricks.sdk import WorkspaceClient
    from databricks.sdk.service import pipelines

    w = WorkspaceClient()

    def upload_code_to_notebook(notebook_path, code):
        w.workspace.import_workspace(
            path=notebook_path,
            content=code.encode("utf-8"),
            format="SOURCE",
            language="PYTHON",
            overwrite=True
        )

    def create_pipeline(pipeline_name):
        notebook_path = f'/Users/{w.current_user.me().user_name}/sdk-{time.time_ns()}'

        notebook_code = '''
        import dlt
        from pyspark.sql.functions import *

        @dlt.table(comment="Load and filter data")
        def filtered_data():
            source_path = spark.conf.get("source_path", "/databricks-datasets/structured-streaming/events")
            filter_condition = spark.conf.get("filter", "eventType = 'open'")

            return (
                spark.read.format("json").load(source_path)
                    .filter(filter_condition)
                    .select("*", current_timestamp().alias("processed_time"))
            )

        @dlt.table(comment="Count filtered events")
        def event_counts():
            return (
                dlt.read("filtered_data")
                    .groupBy("eventType")
                    .count()
                    .withColumnRenamed("count", "event_count")
            )
        '''

        upload_code_to_notebook(notebook_path, notebook_code)

        return w.pipelines.create(
            continuous=False,
            name=pipeline_name,
            libraries=[pipelines.PipelineLibrary(notebook=pipelines.NotebookLibrary(path=notebook_path))],
            clusters=[
                pipelines.PipelineCluster(
                    label="default",
                    serverless=True,
                    num_workers=1,
                    custom_tags={
                        "cluster_type": "serverless",
                    }
                )
            ]
        )

    def trigger_pipeline_run(pipeline_id, source_path, filter_condition):
        return w.pipelines.trigger(
            pipeline_id=pipeline_id,
            configuration_overrides={
                "source_path": source_path,
                "filter": filter_condition,
            }
        )

    pipeline_name = st.text_input("Pipeline Name", f"sdk-{time.time_ns()}")
    source_path = st.text_input("Source Path", "/databricks-datasets/structured-streaming/events")
    filter_condition = st.text_input("Event Type to Filter", "open")

    if st.button("Trigger Run"):
        created_pipeline = create_pipeline(pipeline_name)
        if created_pipeline:
            trigger_pipeline_run(
                created_pipeline.pipeline_id,
                source_path,
                filter_condition,
            )
    """)

with tab_c:
    st.checkbox(
        "[Databricks SDK](https://docs.databricks.com/en/dev-tools/sdk-python.html) installed via `requirements.txt`",
        value=True,
    )
    st.checkbox(
        "[Databricks OAuth](https://docs.databricks.com/dev-tools/api/latest/authentication.html#using-oauth) credentials set in the [environment](https://docs.databricks.com/en/dev-tools/databricks-apps/configuration.html#databricks-apps-environment-variables)",
        value=bool(os.getenv("DATABRICKS_CLIENT_ID") and os.getenv("DATABRICKS_CLIENT_SECRET")),
    )
    st.write(
        "- Ensure your [App principal](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html#how-does-databricks-apps-manage-authorization) `Can Attach To` the cluster."
    )
