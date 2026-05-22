import os
import streamlit as st

import gemini_service

def main():
    st.set_page_config(page_title="Gemini Multi-File Assistant", layout="centered")
    st.title("Gemini Multi-File Analysis System")
    
    uploaded_files = st.file_uploader(
        "Select your context files", 
        type=["pdf", "csv", "xls", "xlsx"], 
        accept_multiple_files=True
    )
    
    query = st.text_area("Enter your prompt:", placeholder="What do you want to know about these files?")
    
    if st.button("Process Request"):
        if not query:
            st.error("Please enter a prompt description.")
            return
            
        with st.spinner("Processing files and communicating with Gemini API..."):
            local_temp_paths = []
            
            # Store Streamlit files in disk temporarily
            for file in uploaded_files:
                temp_dir = "/tmp" if os.path.exists("/tmp") else "."
                temp_path = os.path.join(temp_dir, file.name)
                with open(temp_path, "wb") as f:
                    f.write(file.getbuffer())
                local_temp_paths.append(temp_path)
            
            try:
                # Call service to cloud upload
                api_ready_files = gemini_service.upload_files_to_api(local_temp_paths)
                
                # Set UI channel to Streamlit
                ui_warning_callback = lambda message: st.warning(message)
                
                # Consume model passing warning callback
                answer = gemini_service.generate_response(
                    prompt=query, 
                    attached_files=api_ready_files,
                    warning_callback=ui_warning_callback
                )
                
                st.subheader("Result Analysis:")
                st.write(answer)
                
            finally:
                # Clean local temporary files
                for path in local_temp_paths:
                    if os.path.exists(path):
                        os.remove(path)

if __name__ == "__main__":
    main()