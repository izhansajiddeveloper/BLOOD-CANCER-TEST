# Import necessary libraries
import streamlit as st  # Streamlit for the web interface
from fpdf import FPDF  # To generate PDF reports
from io import BytesIO  # To handle in-memory file operations
import matplotlib.pyplot as plt  # For plotting pie charts
from PIL import Image  # For image processing (if needed)
import pandas as pd  # For handling confidence tracker in table format

# Severity Alert logic
def check_severity(confidence):
    if confidence >= 90:
        return "Critical alert: High confidence in detection."
    elif confidence >= 70:
        return "Warning: Moderate confidence."
    else:
        return "Low confidence in detection."

# Function to generate patient-specific insights
def get_patient_insights(disease):
    insights = {
        "Malaria": "Recommendation: Seek immediate treatment with anti-malarial drugs.",
        "Anemia": "Recommendation: Consider iron supplements and a diet rich in iron.",
        "Leukemia": "Recommendation: Immediate consultation with an oncologist for treatment options.",
        "Tuberculosis": "Recommendation: Start treatment as per healthcare provider's guidance.",
        "Sickle Cell Disease": "Recommendation: Stay hydrated, avoid extreme temperatures, and consult a hematologist."
    }
    return insights.get(disease, "Recommendation: Further evaluation required.")

# Function to generate PDF diagnostic report
def generate_pdf(patient_name, age, gender, results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add patient information
    pdf.cell(200, 10, txt=f"Patient Name: {patient_name}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True)

    # Add classification results with severity alert and insights
    pdf.cell(200, 10, txt="Classification Results:", ln=True)
    for res in results:
        severity = check_severity(res['Confidence'])
        insights = get_patient_insights(res['Disease'])
        pdf.cell(200, 10, txt=f" - {res['Disease']}: {res['Confidence']:.2f}% ({severity})", ln=True)
        pdf.cell(200, 10, txt=f"   Insights: {insights}", ln=True)

    # Save PDF to memory
    pdf_output = BytesIO()
    pdf.output(pdf_output, dest='S')  # Save as a string
    return pdf_output.getvalue()  # Return bytes for download

# Function to generate pie chart of disease distribution
def generate_pie_chart(results):
    disease_counts = {}
    for res in results:
        disease = res['Disease']
        disease_counts[disease] = disease_counts.get(disease, 0) + 1

    # Plotting the pie chart
    labels = disease_counts.keys()
    sizes = disease_counts.values()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Disease Distribution in Blood Cells')
    st.pyplot(fig)

# Function to create a confidence tracker
def generate_confidence_tracker(results):
    df = pd.DataFrame(results)
    st.subheader("AI Confidence Tracker")
    st.dataframe(df)

# Simulated disease classification function (replace with actual model)
def classify_disease(image):
    # Replace with real disease detection logic
    return [
        {"Disease": "Malaria", "Confidence": 88.5},
        {"Disease": "Anemia", "Confidence": 76.3}
    ]

# Streamlit app
st.title("Disease Detection from Blood Cells")
st.write("Upload a blood cell image to classify diseases and generate a diagnostic report.")

# Inputs
uploaded_file = st.file_uploader("Upload Microscopic Blood Cell Image", type=["png", "jpg", "jpeg"])
patient_name = st.text_input("Patient Name")
age = st.number_input("Age", min_value=0, max_value=120, step=1)
gender = st.selectbox("Gender", options=["Select Gender", "Male", "Female", "Other"])

if st.button("Analyze"):
    if uploaded_file and patient_name and age and gender != "Select Gender":
        # Open the uploaded image for processing
        image = Image.open(uploaded_file)

        # Perform disease classification
        results = classify_disease(image)

        # Display results
        st.subheader("Classification Results")
        for res in results:
            severity = check_severity(res['Confidence'])
            st.write(f" - {res['Disease']}: {res['Confidence']:.2f}% ({severity})")
            st.write(f"   Insights: {get_patient_insights(res['Disease'])}")

        # Generate PDF report
        pdf_report = generate_pdf(patient_name, age, gender, results)
        st.download_button(
            label="Download Diagnostic Report (PDF)",
            data=pdf_report,
            file_name="diagnostic_report.pdf",
            mime="application/pdf"
        )

        # Generate Pie Chart
        st.subheader("Disease Distribution")
        generate_pie_chart(results)

        # Generate Confidence Tracker
        generate_confidence_tracker(results)
    else:
        st.error("Please fill in all fields and upload an image.")
