from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
import streamlit as st
#import ollama

from groq import Groq

def analyze_with_groq(prompt, text):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt + text
            }
        ],
        temperature=0.3,
    )

    return completion.choices[0].message.content

def generate_pdf(content):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    for line in content.split("\n"):
        elements.append(Paragraph(line, normal_style))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    buffer.seek(0)
    return buffer

st.title("ReqLens – AI Requirement Analyzer")

st.markdown("""
### AI-powered Requirement Risk & Clarity Analyzer

Upload a requirement document or client notes.  
ReqLens analyzes ambiguity, risks, assumptions, and missing information instantly.
""")

uploaded_file = st.file_uploader("Upload a text file")

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")

    if st.button("Analyze"):
        with st.spinner("Analyzing document..."):

            prompt = """
            You are a senior business analyst.

            Analyze the following document and respond strictly in this format:

            Explicit Requirements:
            - bullet points

            Hidden Assumptions:
            - bullet points

            Missing Information:
            - bullet points

            Potential Risks:
            - bullet points

            Clarifying Questions:
            - bullet points

            Overall Risk Level:
            - Low / Medium / High

            Document:
            """

            result = analyze_with_groq(prompt, text)

            # response = ollama.chat(
            # model='mistral',
            # messages=[
            #     {
            #         "role": "user",
            #         "content": f"""
            # You are a senior business analyst.
            #
            # Analyze the following document and respond strictly in this format:
            #
            # Explicit Requirements:
            # - bullet points
            #
            # Hidden Assumptions:
            # - bullet points
            #
            # Missing Information:
            # - bullet points
            #
            # Potential Risks:
            # - bullet points
            #
            # Clarifying Questions:
            # - bullet points
            #
            # Overall Risk Level:
            # - Low / Medium / High
            #
            # Document:
            # {text}
            # """
            #     }
            # ]
            # )
            #
            # result = response['message']['content']
        risk_level = "Unknown"

        if "Low" in result:
            risk_level = "Low"
        elif "Medium" in result:
            risk_level = "Medium"
        elif "High" in result:
            risk_level = "High"

        st.subheader("📊 Project Risk Level")

        if risk_level == "Low":
            st.success("Low Risk")
        elif risk_level == "Medium":
            st.warning("Medium Risk")
        elif risk_level == "High":
            st.error("High Risk")

        st.subheader("📋 Analysis Report")

        with st.expander("View Full Analysis"):
            st.markdown(result)
            pdf_file = generate_pdf(result)

            st.download_button(
                label="📥 Download Analysis Report (PDF)",
                data=pdf_file,
                file_name="ReqLens_Report.pdf",
                mime="application/pdf"
            )