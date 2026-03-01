from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
import streamlit as st
import ollama


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
            response = ollama.chat(
            model='mistral',
            messages=[
                {
                    "role": "user",
                    "content": f"""
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
{text}
"""
                }
            ]
        )

        result = response['message']['content']
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