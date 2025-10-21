import streamlit as st
from app.core.file_handler import FileHandler, ALLOWED_EXTENSIONS
import os

st.set_page_config(page_title=" Modeling Platform - Upload", layout="centered")


def render_file_upload_ui():
    st.title(" Modeling Platform - File Upload")

    st.write("Upload a data file (`.csv`, `.xlsx`, `.xls`) for processing and analysis.")
    uploaded_file = st.file_uploader("Choose a file to upload", type=ALLOWED_EXTENSIONS)

    if uploaded_file:
        # Validate file type
        if not FileHandler.is_allowed_file(uploaded_file.name):
            st.error(" File type not allowed. Please upload a CSV or Excel file.")
            return

        # Save file to disk
        file_info = FileHandler.save_uploaded_file(uploaded_file)
        st.success(f" File '{file_info['original_filename']}' uploaded successfully!")
        st.info(f"Saved as `{file_info['saved_filename']}`")

        # Display file details
        st.subheader(" File Information")
        st.write({
            "File Path": file_info["filepath"],
            "File Size (KB)": round(file_info["file_size"] / 1024, 2),
            "File Type": file_info["file_type"]
        })

        # Extract metadata
        metadata = FileHandler.get_file_metadata(file_info["filepath"])
        if metadata:
            st.subheader(" File Metadata")
            st.write({
                "Rows": metadata["row_count"],
                "Columns": metadata["column_count"],
                "Column Names": metadata["columns"]
            })
        else:
            st.warning(" Could not extract metadata from file.")

        # Preview file content
        preview_data = FileHandler.preview_file(file_info["filepath"], rows=5)
        if preview_data is not None:
            st.subheader(" Data Preview (first 5 rows)")
            st.dataframe(preview_data)
        else:
            st.warning(" Preview not available for this file type.")

        # Optional: allow user to download the saved file
        with open(file_info["filepath"], "rb") as f:
            st.download_button(
                label=" Download Saved File",
                data=f,
                file_name=file_info["saved_filename"],
                mime="application/octet-stream"
            )


if __name__ == "__main__":
    render_file_upload_ui()
