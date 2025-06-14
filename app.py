import streamlit as st
import json
import os
from datetime import datetime
from extractor import (
    extract_text_from_pdf,
    extract_emails,
    extract_phone_numbers,
    extract_name,
    extract_skills,
    extract_experience
)

st.title("Resume Skill Extractor")

uploaded_file = st.file_uploader("Upload your PDF resume", type=["pdf"])

if uploaded_file:
    try:
        with st.spinner("Extracting data from your resume..."):
            text = extract_text_from_pdf(uploaded_file)
            
            if not text:
                st.error("Failed to extract text from PDF. Please ensure it's a valid PDF file.")
                st.stop()

            data = {
                "Name": extract_name(text),
                "Emails": extract_emails(text),
                "Phones": extract_phone_numbers(text),
                "Skills": extract_skills(text),
                "Experience": extract_experience(text),
                "Timestamp": datetime.now().isoformat()
            }

        st.success("Extraction complete!")
        st.subheader("Extracted Data")
        
        # Display each section separately for better readability
        st.markdown("### Personal Information")
        st.write(f"**Name:** {data['Name']}")
        st.write(f"**Emails:** {', '.join(data['Emails']) if data['Emails'] else 'Not found'}")
        st.write(f"**Phone Numbers:** {', '.join(data['Phones']) if data['Phones'] else 'Not found'}")
        
        st.markdown("### Skills")
        if data['Skills']:
            st.write("- " + "\n- ".join(data['Skills']))
        else:
            st.write("No skills found")
            
        st.markdown("### Experience")
        if data['Experience']:
            st.write("- " + "\n- ".join(data['Experience']))
        else:
            st.write("No experience found")

        # Store in JSON file with proper formatting
        try:
            with open("data_store.json", "a") as f:
                json.dump(data, f, indent=2)
                f.write("\n")
            st.success("Data has been saved to data_store.json")
        except Exception as e:
            st.error(f"Failed to save data: {str(e)}")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    finally:
        # Clean up uploaded file
        try:
            os.remove(uploaded_file.name)
        except:
            pass
