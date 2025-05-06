import streamlit as st
import google.generativeai as genai
import os
import requests
from streamlit_lottie import st_lottie

# ---------------------------
# 🌍 Set Gemini API key
# ---------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "AIzaSyDqUAeaFBj2z47sp4oVk_u1OuS3uN-QEA0"
genai.configure(api_key=GOOGLE_API_KEY)

# ---------------------------
# 🎞️ Load Lottie Animation
# ---------------------------
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

trip_lottie = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_jtbfg2nb.json")

# ---------------------------
# 🧾 Page Setup
# ---------------------------
st.set_page_config(page_title="Trip Planner", page_icon="🗺️", layout="wide")

st.markdown("""
    <style>
    .title {
        font-size:40px !important;
        color:#4A6FA5;
        font-weight: bold;
    }
    .subtitle {
        font-size:20px !important;
        color:#7C9EB2;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# 🎯 App Title + Animation
# ---------------------------
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<div class='title'>🧳 AI Trip Planner</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Plan your journey in seconds ✨</div>", unsafe_allow_html=True)
with col2:
    if trip_lottie:
        st_lottie(trip_lottie, height=180, key="trip")

# ---------------------------
# 📝 Sidebar Inputs
# ---------------------------
st.sidebar.header("✍️ Enter Trip Details")
source = st.sidebar.text_input("📍 Source City")
destination = st.sidebar.text_input("🏙️ Destination City")
days = st.sidebar.slider("🗓️ Number of Days", 1, 30, 3)
preferences = st.sidebar.text_area("💡 Preferences (e.g., nature, nightlife, food, history)")

# ---------------------------
# 🚀 Generate Itinerary
# ---------------------------
if st.sidebar.button("🚀 Generate Itinerary"):
    if not all([source, destination, preferences]):
        st.error("⚠️ Please complete all the fields.")
    else:
        with st.spinner("🧠 Thinking... generating your dream trip!"):
            try:
                model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

                prompt = f"""
                You are a world-class travel planner.

                Create a detailed and structured {days}-day travel itinerary from {source} to {destination} based on the following traveler preferences: {preferences}.

                For each day, include:
                - A title for the day (e.g., “Exploring Old Town”)
                - Morning, afternoon, and evening plans with specific attractions or activities
                - Names of local restaurants or cafés for meals
                - Suggested hotels with 1-2 budget options
                - Transportation details (e.g., Uber, walking, train) between major points
                - Local tips (e.g., cultural etiquette, weather, packing suggestions)
                - Estimated cost breakdown for the day in Indian Rupees (₹), not USD
                - Any hidden gems or offbeat suggestions

                Format each day clearly under a heading: “Day X: [Title]”
                Use markdown to structure the response (with bullet points, subheadings).
                Keep the writing friendly, detailed, and practical.
                """

                response = model.generate_content(prompt)
                output = response.text.strip()

                st.success("🎉 Your trip itinerary is ready!")
                st.markdown("## 🗓️ Your Detailed Itinerary")

                # ---------------------------
                # 📅 Display Each Day
                # ---------------------------
                days_data = output.split("Day ")

                for i in range(1, days + 1):
                    day_content = next((d for d in days_data if d.strip().startswith(f"{i}")), None)
                    if day_content:
                        content = day_content.split("\n", 1)[-1].strip()
                        with st.expander(f"📅 Day {i}"):
                            st.markdown(f"**Day {i}**\n\n{content}")
                    else:
                        st.warning(f"⚠️ Day {i} not found in the response.")

            except Exception as e:
                st.error(f"❌ Error: {e}")
