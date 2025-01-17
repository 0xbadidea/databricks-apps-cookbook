import os
import io
import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

st.header(body="Workflows", divider=True)
st.subheader("Retrieve job results")

st.write(
    "This recipe retreives the results of a [Databricks Workflows](https://docs.databricks.com/en/jobs/index.html) job task run."
)

tab1, tab2, tab3 = st.tabs(["**Try it**", "**Code snippet**", "**Requirements**"])

if "workflow_check_success" not in st.session_state:
    st.session_state.workflow_check_success = False

with tab1:
    task_run_id = st.text_input(
        label="Specify a task run ID",
        placeholder="293894477334278",
    )

    if st.button(label="Get task run results"):
        if not task_run_id.strip():
            st.warning("Please specify a valid task run ID.", icon="⚠️")
        else:
            results = w.jobs.get_run_output(task_run_id)

            st.success("Task run results retrieved successfully", icon="✅")

            if results.sql_output:
                st.markdown("**SQL output**")
                st.json(results.sql_output.as_dict())

            if results.dbt_output:
                st.markdown("**dbt output**")
                st.json(results.dbt_output.as_dict())

            if results.run_job_output:
                st.markdown("**Notebook output**")
                st.json(results.run_job_output.as_dict())

            if results.notebook_output:
                st.markdown("**Notebook output**")
                st.json(results.notebook_output.as_dict())

with tab2:
    st.code("""
    import os
    from databricks.sdk import WorkspaceClient

    w = WorkspaceClient()

    workflow_id = "workflow-id"

    run = w.jobs.runs_get(run_id=workflow_id)
    print(f"Workflow status: {run.state.life_cycle_state}")
    print(f"Result: {run.state.result_state}")
    """)

with tab3:
    st.markdown("""
    To retrieve the results of a job run, your app service principal needs at least the `Can View` permission on the job.

    See [Control access to a job](https://docs.databricks.com/en/jobs/privileges.html#control-access-to-a-job) for more information. 
    """)
