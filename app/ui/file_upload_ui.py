import streamlit as st
from app.core.file_service import FileService
from app.core.file_handler import FileHandler, ALLOWED_EXTENSIONS
from app.db import init_db

st.set_page_config(page_title=" Modeling Platform - Upload", layout="centered")

if 'db_initialized'  not in st.session_state:
    init_db()
    st.session_state.db_initialized = True


def render_file_upload_ui():
    st.title(" Modeling Platform - File Upload")

    st.write("Upload a data file (`.csv`, `.xlsx`, `.xls`) for processing and analysis.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file to upload", type=ALLOWED_EXTENSIONS)

    if uploaded_file:
        # Validate file type
        if not FileHandler.is_allowed_file(uploaded_file.name):
            st.error(" File type not allowed. Please upload a CSV or Excel file.")
            return

        # Use FileService for complete workflow (saves to disk + database)
        with st.spinner("Uploading file..."):
            db_file = FileService.upload_and_save_file(uploaded_file)

        if db_file:
            st.success(f" File '{uploaded_file.name}' uploaded successfully!")
            st.info(f"Saved as `{db_file.filename}` | Database ID: `{db_file.id}`")

            # Display file details from database
            st.subheader("File Information")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**File Path:**", db_file.filePath)
                st.write("**File Type:**", db_file.file_type)
            with col2:
                st.write("**Upload Time:**", db_file.upload_time.strftime("%Y-%m-%d %H:%M:%S"))
                file_size_kb = round(os.path.getsize(db_file.filePath) / 1024, 2)
                st.write("**File Size:**", f"{file_size_kb} KB")

            # Get file data with preview and metadata
            file_data = FileService.get_file_with_preview(db_file.id, rows=5)

            if file_data and file_data['metadata']:
                # Display metadata
                st.subheader("File Metadata")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", file_data['metadata']['row_count'])
                with col2:
                    st.metric("Columns", file_data['metadata']['column_count'])
                with col3:
                    st.metric("File ID", db_file.id[:8] + "...")

                with st.expander(" Column Names"):
                    st.write(file_data['metadata']['columns'])
            else:
                st.warning(" Could not extract metadata from file.")

            # Preview file content
            if file_data and file_data['preview'] is not None:
                st.subheader(" Data Preview (first 5 rows)")
                st.dataframe(file_data['preview'], use_container_width=True)
            else:
                st.warning(" Preview not available for this file type.")

            # Download button
            with open(db_file.filePath, "rb") as f:
                st.download_button(
                    label=" Download Saved File",
                    data=f,
                    file_name=db_file.filename,
                    mime="application/octet-stream"
                )
        else:
            st.error(" Failed to upload file. Please try again.")

    # Display all uploaded files
    st.divider()
    st.subheader(" Previously Uploaded Files")

    files = FileService.get_all_files()

    if files:
        # Search functionality
        search_term = st.text_input(" Search files by name", "")

        if search_term:
            files = FileService.search_files_by_name(search_term)

        # Display files in a nice format
        for file in files:
            with st.expander(f" {file.filename} - {file.upload_time.strftime('%Y-%m-%d %H:%M')}"):
                col1, col2, col3 = st.columns([2, 2, 1])

                with col1:
                    st.write("**Type:**", file.file_type)
                    st.write("**Path:**", file.filePath)

                with col2:
                    st.write("**ID:**", file.id)
                    st.write("**Uploaded:**", file.upload_time.strftime("%Y-%m-%d %H:%M:%S"))

                with col3:
                    # View preview button
                    if st.button(" Preview", key=f"preview_{file.id}"):
                        preview_data = FileHandler.preview_file(file.filePath, rows=5)
                        if preview_data is not None:
                            st.dataframe(preview_data)

                    # Delete button
                    if st.button("🗑️ Delete", key=f"delete_{file.id}"):
                        if FileService.delete_file(file.id):
                            st.success(f" Deleted {file.filename}")
                            st.rerun()
                        else:
                            st.error(" Failed to delete file")
    else:
        st.info("No files uploaded yet. Upload your first file above! 👆")


if __name__ == "__main__":
    render_file_upload_ui()