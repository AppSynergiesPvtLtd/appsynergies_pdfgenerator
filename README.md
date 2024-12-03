

# AppSynergies PDF Generator

## Overview

The **AppSynergies PDF Generator** is a user-friendly Streamlit web application designed for dynamic document generation. It enables users to create and customize professional documents such as NDAs, Contracts, and Pricing Lists with ease. This tool allows for the seamless editing of Word templates and provides a one-click option to generate and download both Word and PDF formats.

---

## Key Features

- **Dynamic Document Editing**: Customize predefined Word templates by filling out user-friendly forms in the app.
- **PDF Conversion**: Automatically convert Word documents into PDFs for universal compatibility.
- **Multi-Template Support**: Generate documents like NDAs, Contracts, and Pricing Lists tailored to specific client details.
- **Service Selection**: For Pricing Lists, users can choose from a list of services to include.
- **Streamlit Integration**: Intuitive UI for quick and easy document generation.

---

## Tech Stack

- **Python 3.x**: Core programming language for the application logic.
- **Streamlit**: Framework for building the web application interface.
- **python-docx**: Library for Word document manipulation.
- **LibreOffice/COM Automation**: Used for Word-to-PDF conversion.
- **OS & Subprocess**: For file management and external process execution.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Akshara-Amirtharaj/appsynergies_pdfgenerator.git
cd appsynergies_pdfgenerator
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`.

---

## Usage

1. **Select Document Type**: Choose between "NDA," "Contract," or "Pricing List."
2. **Fill Out the Form**: Enter client details such as name, designation, email, location, and additional information based on the document type.
3. **Generate Document**: Click the "Generate Document" button to create the customized document.
4. **Download Your Files**: Download the generated Word or PDF files directly from the app.

---

## Document Types

### 1. NDA & Contract
- **Region-Specific Templates**: Choose between "India" and "ROW" templates.
- **Customizable Fields**: Client name, company name, address, and date.
- **Aligned and Justified Formatting**: Ensures a professional appearance.

### 2. Pricing List
- **Client Details**: Name, designation, contact number, email, and location.
- **Service Selection**: Select services from a predefined list to customize the pricing document.
- **Dynamic Tables**: Automatically includes or excludes rows based on selected services.

---

## Example Services for Pricing List

- Landing page website (design + development)
- AI Automations (6 Scenarios)
- WhatsApp Automation + Cloud Business Account Setup
- CRM Setup
- Email Marketing Setup
- Make/Zapier Automation
- Firefly Meeting Automation
- Paid Ads (Lead Generation)
- AI Chatbot
- Custom AI Models & Agents

---

## Contributing

Contributions are welcome! To suggest improvements or add features:
1. Fork the repository.
2. Create a feature branch.
3. Commit and push your changes.
4. Open a pull request with a detailed description.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Contact

For questions or collaboration, feel free to reach out:

- **GitHub**: [Akshara-Amirtharaj](https://github.com/Akshara-Amirtharaj)

