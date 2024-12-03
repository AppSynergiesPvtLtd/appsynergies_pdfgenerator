import streamlit as st
from docx import Document
from datetime import datetime
import os
import platform
import subprocess
import comtypes.client
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.text import WD_BREAK

port = int(os.environ.get("PORT", 8501))
# Function to edit the Word template dynamically
def edit_word_template(template_path, output_path, placeholders):
    try:
        doc = Document(template_path)

        # Replace placeholders in paragraphs and set alignment
        for para in doc.paragraphs:
            for key, value in placeholders.items():
                if key in para.text:
                    para.text = para.text.replace(key, value)
                    # Set alignment to justify
                    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        # Replace placeholders in tables and set alignment
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():  # Check if the cell is not empty
                        for key, value in placeholders.items():
                            if key in cell.text:
                                # Replace placeholder
                                cell.text = cell.text.replace(key, value)

                                # Set paragraph alignment for each paragraph in the cell
                                for paragraph in cell.paragraphs:
                                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

                                # Set vertical alignment of the cell (top, center, bottom)
                                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

        # Save the updated document
        doc.save(output_path)
        return output_path
    except Exception as e:
        raise Exception(f"Error editing Word template: {e}")


# Function to handle pricing document edit
def edit_pricing_template(template_path, output_path, name, designation, contact, email, location, selected_services):
    try:
        doc = Document(template_path)

        # Replace placeholders in the general paragraphs
        for para in doc.paragraphs:
            if "<<Client Name>>" in para.text:
                para.text = para.text.replace("<<Client Name>>", name)
            if "<<Client Designation>>" in para.text:
                para.text = para.text.replace("<<Client Designation>>", designation)
            if "<<Client Contact>>" in para.text:
                para.text = para.text.replace("<<Client Contact>>", contact)
            if "<<Client Email>>" in para.text:
                para.text = para.text.replace("<<Client Email>>", email)
            if "<<Client Location>>" in para.text:
                para.text = para.text.replace("<<Client Location>>", location)



        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if "<<Client Name>>" in cell.text:
                        cell.text = cell.text.replace("<<Client Name>>", name)
                    if "<<Client Designation>>" in cell.text:
                        cell.text = cell.text.replace("<<Client Designation>>", designation)
                    if "<<Client Contact>>" in cell.text:
                        cell.text = cell.text.replace("<<Client Contact>>", contact)
                    if "<<Client Email>>" in cell.text:
                        cell.text = cell.text.replace("<<Client Email>>", email)
                    if "<<Client Location>>" in cell.text:
                        cell.text = cell.text.replace("<<Client Location>>", location)
        # Process tables to find and update the SPOC table and service table separately
        spoc_table_found = False

        for para in doc.paragraphs:
            if "Supporting SPOC Details" in para.text:
                para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER  # Center the heading
                spoc_table_found = True

        for table_idx, table in enumerate(doc.tables):
            if spoc_table_found and table_idx == 0:  # Assuming SPOC table is the first table after the identifier
                for row in table.rows:
                    if "Project Sponsor/Client’s Detail" in row.cells[0].text:
                        row.cells[1].text = name
                        row.cells[2].text = designation
                        row.cells[3].text = contact
                        row.cells[4].text = email
                spoc_table_found = False
            else:
                rows_to_delete = []
                for row_idx, row in enumerate(table.rows[1:], start=1):
                    service_name = row.cells[0].text.strip()
                    if service_name not in selected_services:
                        rows_to_delete.append(row_idx)

                for row_idx in reversed(rows_to_delete):
                    table._element.remove(table.rows[row_idx]._element)

        # Ensure "Next Steps" starts on a new page
        for para in doc.paragraphs:
            if "Next Steps:" in para.text:
                page_break = para.insert_paragraph_before()
                run = page_break.add_run()
                run.add_break(WD_BREAK.PAGE)

        # Save the updated document
        doc.save(output_path)
        return output_path
    except Exception as e:
        raise Exception(f"Error editing Word template: {e}")


# Function to convert Word to PDF
def convert_to_pdf(doc_path, pdf_path):
    if platform.system() == "Windows":
        try:
            import comtypes.client
            word = comtypes.client.CreateObject("Word.Application")
            doc = word.Documents.Open(doc_path)
            doc.SaveAs(pdf_path, FileFormat=17)
            doc.Close()
            word.Quit()
            print("Converted to PDF using COM")
        except Exception as e:
            raise Exception(f"Error using COM on Windows: {e}")
    else:
        try:
            # LibreOffice method for non-Windows
            subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(pdf_path), doc_path])
            print("Converted to PDF using LibreOffice")
        except Exception as e:
            raise Exception(f"Error using LibreOffice: {e}")

# Streamlit App
st.title("Dynamic Document Generator")

# Dropdown for document selection
option = st.selectbox("Select Document Type", ["NDA", "Contract", "Pricing List"])

# Base directory for templates
base_dir = os.path.abspath(os.path.dirname(__file__))

# Input form fields for NDA and Contract
if option in ["NDA", "Contract"]:
    region = st.selectbox("Region", ["India", "ROW"])
    template_path = os.path.join(base_dir, f"{option} Template - {'INDIA 3' if region == 'India' else 'ROW 3'}.docx")

    client_name = st.text_input("Enter Client Name:")
    company_name = st.text_input("Enter Company Name:")
    address = st.text_area("Enter Address:")
    date_field = st.date_input("Enter Date:", datetime.today())

    placeholders = {
        "<< Client Name >>": client_name,
        "<<Company Name>>": company_name,
        "<<Address>>": address,
        "<< Date >>": date_field.strftime("%d-%m-%Y"),
    }

# Input form fields for Pricing List
elif option == "Pricing List":
    client_name = st.text_input("Enter Client Name:")
    designation = st.text_input("Enter Designation:")
    contact = st.text_input("Enter Contact Number:")
    email = st.text_input("Enter Email ID:")
    location = st.selectbox("Location", ["India", "ROW"])
    selected_services = st.multiselect("Select Services", [
        "Landing page website (design + development)",
        "AI Automations (6 Scenarios)",
        "Whatsapp Automation + Whatsapp Cloud Business Account Setup",
        "CRM Setup",
        "Email Marketing Setup",
        "Make/Zapier Automation",
        "Firefly Meeting Automation",
        "Marketing Strategy",
        "Social Media Channels",
        "Creatives (10 Per Month)",
        "Creatives (20 Per Month)",
        "Creatives (30 Per Month)",
        "Reels (10 Reels)",
        "Meta Ad Account Setup & Pages Setup",
        "Paid Ads (Lead Generation)",
        "Monthly Maintenance & Reporting",
        "AI Chatbot",
        "PDF Generation Automations",
        "AI Generated Social Media Content & Calendar",
        "Custom AI Models & Agents"
    ])
    template_path = os.path.join(base_dir, "DM & Automations Services Pricing - Andrew.docx")

if st.button("Generate Document"):
    if option == "Pricing List" and (not all([client_name, designation, contact, email, location]) or not selected_services):
        st.error("All fields and at least one service must be selected!")
    elif option in ["NDA", "Contract"] and not all(placeholders.values()):
        st.error("Please fill all required fields!")
    else:
        word_output_path = os.path.join(base_dir, f"{option}_Document.docx")
        pdf_output_path = os.path.join(base_dir, f"{option}_Document.pdf")

        try:
            if option == "Pricing List":
                updated_word_path = edit_pricing_template(
                    template_path, word_output_path, client_name, designation, contact, email, location, selected_services
                )
            else:
                updated_word_path = edit_word_template(template_path, word_output_path, placeholders)

            convert_to_pdf(updated_word_path, pdf_output_path)

            st.success(f"{option} Document Generated Successfully!")
            with open(word_output_path, "rb") as word_file:
                st.download_button(f"Download {option} (Word)", word_file, file_name=f"{option}_Document.docx")
            with open(pdf_output_path, "rb") as pdf_file:
                st.download_button(f"Download {option} (PDF)", pdf_file, file_name=f"{option}_Document.pdf")
        except Exception as e:
            st.error(f"An error occurred: {e}")
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    st._is_running_with_streamlit = False
    st.run(host="0.0.0.0", port=port)
