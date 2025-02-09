import streamlit as st
from fpdf import FPDF
import tempfile

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Generated PDF Report', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(5)

    def chapter_content(self, content):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, content)
        self.ln(5)

# Streamlit App UI
st.title("PDF Generator from User Input")

# Collect multiple inputs from the user
name = st.text_input("Enter your name:")
date_of_birth = st.date_input("Enter Your Birth Date : ")
age = st.number_input("Enter your age:", min_value=1, max_value=120, step=1)
gender = st.selectbox("Select Your Gender : ", ("Male", "Female", "Trans"))
number = st.number_input("Enter your Mobile Number : ")
alt_number = st.number_input("Enter Alternative Number : ")
email = st.text_input("Enter your email:")
address = st.text_input("Enter Your Address : ")
description = st.text_area("Provide a brief description about yourself:")

if st.button("Generate PDF"):
    if name and email and description:
        # Create a PDF instance
        pdf = PDF()
        pdf.add_page()

        # Add user input to the PDF
        pdf.chapter_title("User Information")
        pdf.chapter_content(f"Name: {name}")
        pdf.chapter_content(f"Date of Birth : {date_of_birth}")
        pdf.chapter_content(f"Age : {age}")
        pdf.chapter_content(f"Gender : {gender}")
        pdf.chapter_content(f"Mobile Number : {number}")
        pdf.chapter_content(f"Alternative Number : {alt_number}")
        pdf.chapter_content(f"Email: {email}")
        pdf.chapter_content(f"Address : {address}")
        pdf.chapter_title("Description")
        pdf.chapter_content(description)

        # Save PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_output_path = tmp_file.name
            pdf.output(pdf_output_path)

        # Provide download button for the generated PDF
        with open(pdf_output_path, "rb") as file:
            st.download_button(
                label="Download PDF",
                data=file,
                file_name="User_Details.pdf",
                mime="application/pdf"
            )
    else:
        st.error("Please fill in all the fields to generate the PDF.")
