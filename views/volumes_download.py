import os
from pathlib import Path
import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

st.header(body="Working with Unity Catalog volumes", divider=True)

st.subheader("Download a file from a volume")

tab1, tab2 = st.tabs(["Code snippet", "Try it"])

with tab1:
    st.code("""
    import streamlit as st
    from databricks.sdk import WorkspaceClient
            
    w = WorkspaceClient()
            
    download_file_path = "/Volumes/catalog/schema/volume_name/file.csv
            
    try:
        resp = w.files.download(download_file_path)
        file_data = resp.contents.read()

        file_name = os.path.basename(download_file_path)

        print("File downloaded successfully.")
            
        st.download_button(label="Download", data=file_data, file_name=file_name)
    except Exception as e:
        st.error(f"Error downloading file: {str(e)}")
            
    
    """)

with tab2:
    st.info(
        body="""
    To download a file from a volume, your app's service principal needs the following permissions:
    * `USE CATALOG` on the volume's catalog
    * `USE SCHEMA` on the volume's schema
    * `READ VOLUME` on the volume

    See [Privileges required for volume operations](https://docs.databricks.com/en/volumes/privileges.html#privileges-required-for-volume-operations) for more information.
    """,
        icon="ℹ️",
    )
    download_file_path = st.text_input(
        label="Specify a path to a file in a Unity Catalog volume",
        placeholder="/Volumes/main/marketing/raw_files/leads.csv",
    )

    if st.button("Get file"):
        if download_file_path:
            try:
                resp = w.files.download(download_file_path)
                file_data = resp.contents.read()

                file_name = os.path.basename(download_file_path)

                st.success(f"File '{file_name}' downloaded successfully.")
                st.download_button(
                    label="Download file",
                    data=file_data,
                    file_name=file_name,
                    mime="application/octet-stream",
                )
            except Exception as e:
                st.error(f"Error downloading file: {str(e)}")
        else:
            st.warning("Please specify a file path.")
