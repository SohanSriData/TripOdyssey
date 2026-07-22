import streamlit as st
import requests
import datetime

BASE_URL = "http://localhost:8000"

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Trip Odyssey Travel Planner",
    page_icon=";)",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
<style>

.title-text{
    font-size:48px;
    font-weight:700;
    margin-bottom:8px;
}

.subtitle-text{
    font-size:18px;
    color:#9ca3af;
    margin-bottom:24px;
}

.response-box{
    padding:25px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.1);
}

.footer-note{
    color:#9ca3af;
    font-size:14px;
}

/* Style the form nicely */
div[data-testid="stForm"]{
    padding:25px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.1);
    background-color:rgba(255,255,255,0.02);
}

</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.header("How to use")

    st.write(
        "Provide your destination, trip duration, and preferences. "
        "The agent returns a plan with itinerary, costs, hotels, "
        "food, transport and attractions."
    )

    st.markdown("---")

    st.subheader("Tips")

    st.write("• Ask for a stay duration, such as 5 days.")
    st.write("• Mention preferred cuisine, activities or budget.")
    st.write("• Ask for costs in INR if you want local currency values.")

    st.markdown("---")

    st.write("Built for fast AI-powered travel planning.")

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.markdown(
    "<div class='title-text'>Trip Odyssey Travel Planner</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class='subtitle-text'>
Generate a complete travel itinerary, budget breakdown and
destination guide for any city worldwide.
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# USER INPUT FORM
# ---------------------------------------------------------

with st.form(key="query_form", clear_on_submit=True):

    st.subheader("Start your travel plan")

    user_input = st.text_input(
        "Your travel request",
        placeholder=(
            "e.g. Plan a trip to Goa for 5 days with beaches, "
            "local food and a budget of ₹20,000."
        ),
    )

    submit_button = st.form_submit_button(
        "Generate Plan",
        use_container_width=True,
    )

# ---------------------------------------------------------
# API CALL
# ---------------------------------------------------------

if submit_button:

    if not user_input.strip():
        st.warning("Please enter your travel request.")
    else:
        try:
            with st.spinner("Planning your trip..."):

                payload = {
                    "question": user_input
                }

                response = requests.post(
                    f"{BASE_URL}/query",
                    json=payload,
                    timeout=300,
                )

            if response.status_code == 200:

                answer = response.json().get(
                    "answer",
                    "No answer was returned.",
                )

                generated_time = datetime.datetime.now().strftime(
                    "%Y-%m-%d at %H:%M"
                )

                markdown_content = f"""
# 🌍 AI Travel Plan

**Generated:** {generated_time}

**Created by:** TripOdyssey

---

{answer}

---

> **Disclaimer**
>
> This travel plan was generated using AI. Please verify prices,
> hotel availability, transportation schedules, visa requirements
> and operating hours before making bookings.
"""

                st.success("Your travel plan is ready!")

                with st.expander(
                    "View Generated Travel Plan",
                    expanded=True,
                ):
                    st.markdown(markdown_content)

            else:
                st.error(
                    f"Backend returned an error ({response.status_code})."
                )
                st.code(response.text)

        except requests.exceptions.Timeout:
            st.error(
                "The request timed out. Please try again."
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the backend server. "
                "Make sure it is running on port 8000."
            )

        except Exception as e:
            st.error(
                f"The response failed due to:\n\n{e}"
            )