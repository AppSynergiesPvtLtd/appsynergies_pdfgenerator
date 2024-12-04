import streamlit as st
from docx import Document
from datetime import datetime
import os
import platform
import subprocess
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
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

                                # Maintain the font style
                                for run in paragraph.runs:
                                    run.font.size = Pt(10)  # Set font size to match other text and make it smaller

        # Adjust signature alignment specifically for NDA India and ROW templates
        for para in doc.paragraphs:
            if "Signature Details:" in para.text:
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for i, run in enumerate(para.runs):
                    if "<<Company Name>>" in run.text:
                        run.text = run.text.replace("<<Company Name>>", placeholders.get("<<Company Name>>", ""))
                    if "<< Date >>" in run.text:
                        run.text = run.text.replace("<< Date >>", placeholders.get("<< Date >>", ""))
                        for r in para.runs:
                            r.font.size = Pt(8)  # Make the date font size consistent

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
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER  # Center the heading
                spoc_table_found = True

        for table_idx, table in enumerate(doc.tables):
            if spoc_table_found and table_idx == 0:  # Assuming SPOC table is the first table after the identifier
                for row in table.rows:
                    if "Project Sponsor/Client’s Detail" in row.cells[0].text:
                        row.cells[1].text = name
                        row.cells[2].text = designation
                        row.cells[3].text = contact
                        row.cells[4].text = email
                    # Set alignment and font style for cells
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            for run in paragraph.runs:
                                run.font.size = Pt(8)  # Set font size smaller
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
            import pythoncom
            pythoncom.CoInitialize()  # Initialize the COM library
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
option = st.selectbox("Select Document Type", ["NDA", "Contract", "Pricing List"], key="doc_type")

# Base directory for templates
base_dir = os.path.abspath(os.path.dirname(__file__))

# Input form fields for NDA and Contract
if option in ["NDA", "Contract"]:
    region = st.selectbox("Region", ["India", "ROW"], key="region")
    template_path = os.path.join(base_dir, f"{option} Template - {'INDIA 3' if region == 'India' else 'ROW 3'}.docx")

    client_name = st.text_input("Enter Client Name:", key="client_name")
    company_name = st.text_input("Enter Company Name:", key="company_name")
    address = st.text_area("Enter Address:", key="address")
    date_field = st.date_input("Enter Date:", datetime.today(), min_value=datetime.today(), max_value=datetime.today(), key="date_field")

    placeholders = {
        "<< Client Name >>": client_name,
        "<<Company Name>>": company_name,
        "<<Address>>": address,
        "<< Date >>": date_field.strftime("%d-%m-%Y"),
    }

# Input form fields for Pricing List
elif option == "Pricing List":
    currency = st.selectbox("Select Currency", ["USD", "Rupees", "Pounds"], key="currency")
    if currency == "USD":
        template_path = os.path.join(base_dir, "DM & Automations Services Pricing - USD.docx")
    elif currency == "Rupees":
        template_path = os.path.join(base_dir, "DM & Automations Services Pricing - Rupees.docx")
    elif currency == "Pounds":
        template_path = os.path.join(base_dir, "DM & Automations Services Pricing - Pounds.docx")

    client_name = st.text_input("Enter Client Name:", key="client_name_pricing")
    designation = st.text_input("Enter Designation:", key="designation")
    contact = st.text_input("Enter Contact Number:", key="contact")
    email = st.text_input("Enter Email ID:", key="email")
    location = st.selectbox("Location", ["India", "ROW"], key="location")
    select_all_services = st.checkbox("Select All Services", key="select_all_services")
    services = [
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
    ]
    if select_all_services:
        selected_services = services
    else:
        selected_services = st.multiselect("Select Services", services, key="selected_services")

if st.button("Generate Document", key="generate_button"):
    if option == "Pricing List" and (not all([client_name, designation, contact, email, location]) or not selected_services):
        st.error("All fields and at least one service must be selected!")
    elif option in ["NDA", "Contract"] and not all(placeholders.values()):
        st.error("Please fill all required fields!")
    else:
        current_date_str = datetime.now().strftime("%d_%b_%Y").lower()
        word_output_path = os.path.join(base_dir, f"{client_name.lower()}_{option.lower().replace(' ', '_')}_{current_date_str}.docx")
        pdf_output_path = os.path.join(base_dir, f"{client_name.lower()}_{option.lower().replace(' ', '_')}_{current_date_str}.pdf")

        try:
            if option == "Pricing List":
                updated_word_path = edit_pricing_template(
                    template_path, word_output_path, client_name, designation, contact, email, location, selected_services
                )
            else:
                updated_word_path = edit_word_template(template_path, word_output_path, placeholders)

            convert_to_pdf(updated_word_path, pdf_output_path)

            st.session_state["document_generated"] = True
            st.session_state["current_options"] = {
                "option": option,
                "region": region if option in ["NDA", "Contract"] else None,
                "currency": currency if option == "Pricing List" else None,
                "client_name": client_name,
                "designation": designation if option == "Pricing List" else None,
                "contact": contact if option == "Pricing List" else None,
                "email": email if option == "Pricing List" else None,
                "location": location if option == "Pricing List" else None,
                "selected_services": selected_services if option == "Pricing List" else None,
                "placeholders": placeholders if option in ["NDA", "Contract"] else None,
                "current_date_str": current_date_str
            }

            st.success(f"{option} Document Generated Successfully!")
            st.session_state["show_download_buttons"] = True
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Logic to hide download buttons if options are changed
def options_changed():
    current_options = st.session_state.get("current_options", {})
    if not current_options:
        return True
    if current_options.get("option") != option:
        return True
    if option in ["NDA", "Contract"]:
        if current_options.get("region") != region or \
           current_options.get("client_name") != client_name or \
           current_options.get("placeholders") != placeholders:
            return True
    if option == "Pricing List":
        if current_options.get("currency") != currency or \
           current_options.get("client_name") != client_name or \
           current_options.get("designation") != designation or \
           current_options.get("contact") != contact or \
           current_options.get("email") != email or \
           current_options.get("location") != location or \
           current_options.get("selected_services") != selected_services:
            return True
    return False

if options_changed():
    st.session_state["document_generated"] = False
    st.session_state["show_download_buttons"] = False

if st.session_state.get("document_generated"):
    current_date_str = st.session_state.get("current_options").get("current_date_str")
    word_output_path = os.path.join(base_dir, f"{client_name.lower()}_{option.lower().replace(' ', '_')}_{current_date_str}.docx")
    pdf_output_path = os.path.join(base_dir, f"{client_name.lower()}_{option.lower().replace(' ', '_')}_{current_date_str}.pdf")
    with open(word_output_path, "rb") as word_file:
        st.download_button(f"Download {option} (Word)", word_file, file_name=f"{client_name.lower()}_{option.lower().replace(' ', '_')}_{current_date_str}.docx", key="download_word")
    with open(pdf_output_path, "rb") as pdf_file:
        st.download_button(f"Download {option} (PDF)", pdf_file, file_name=f"{client_name.lower()}_{option.lower().replace(' ', '_')}_{current_date_str}.pdf", key="download_pdf")
