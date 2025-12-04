from openai import OpenAI
import streamlit as st

# ✅ Direct API key (no getenv or .env needed)
OPENROUTER_API_KEY = "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"

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

FREE_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

def call_llm(prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            model=FREE_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error calling LLM: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Advanced Code Scanner", page_icon="🛡️", layout="wide")
st.title("🛡️ Advanced Code Scanner with LLM Insights")
st.write("Upload one or more code files to detect **malicious or phishing patterns** using AI.")

uploaded_files = st.file_uploader(
    "Choose code files",
    type=["php", "js", "py", "java", "cpp", "html", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        code = file.read().decode("utf-8", errors="ignore")
        st.subheader(f"📄 File: {file.name}")
        
        with st.expander("View File Content"):
            st.code(code, language="plaintext")

        st.info("Requesting LLM analysis… please wait.")
        prompt = (
            "Analyze the following code for any malicious or phishing patterns. "
            "Highlight obfuscation, unsafe use of user input, backdoors, "
            "and suspicious logic.\n\n"
            f"{code}"
        )
        analysis = call_llm(prompt)
        st.markdown(f"### 🤖 LLM Analysis:\n{analysis}")
