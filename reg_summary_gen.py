import streamlit as st
import pandas as pd
import openai
import os
from dotenv import load_dotenv

# ===== Load API key from .env file =====
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error(" No OpenAI API key found. Make sure it's set in a `.env` file.")
    st.stop()

client = openai.Client(api_key=api_key)

# ===== UI Layout =====
st.set_page_config(page_title="Regulatory Summary Generator", layout="wide")
st.title("AI-Powered Regulatory Summary Generator")
st.markdown("Upload a trade data CSV to generate a regulatory report summary (e.g., MiFID II).")

uploaded_file = st.file_uploader("Upload Trade Data CSV", type=["csv"])

# ===== Summary Generation =====
def generate_summary(data: pd.DataFrame) -> str:
    # Turn the uploaded trade data into a plain text table
    trade_text = data.to_string(index=False)

    # Build a simple instruction prompt for the AI
    prompt = (
        "You are a regulatory analyst.\n"
        "Given the following trade data, write a short summary in plain English "
        "that might appear in a regulatory report:\n\n"
        f"{trade_text}"
    )

    # Call OpenAI's chat model to generate the summary
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo" if preferred
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3  # lower temperature = more focused output
    )

    # Extract and return the generated message text
    return response.choices[0].message.content.strip()


# ===== Main Logic =====
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader(" Uploaded Trade Data")
        st.dataframe(df)

        if st.button(" Generate Summary"):
            with st.spinner("Generating summary..."):
                summary = generate_summary(df)
                st.success("Summary generated successfully.")
                st.subheader("Regulatory Summary")
                st.text_area("Summary", summary, height=300)
    except Exception as e:
        st.error(f" Error processing file:\n\n{str(e)}")
