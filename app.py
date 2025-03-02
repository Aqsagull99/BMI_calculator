import streamlit as st
import matplotlib.pyplot as plt
import datetime
import json

# App Config
st.set_page_config(page_title="BMI & Health Analyzer", page_icon="⚖️", layout="wide")

# Sidebar
st.sidebar.header("⚙️ Settings")
unit = st.sidebar.radio("Select Unit", ("Metric (kg, cm)", "Imperial (lbs, inches)"))

# Theme Colors
theme = st.sidebar.radio("Select Theme", ("Green & Purple", "Blue & Orange"))
colors = {"Green & Purple": ("#6A0572", "#00B140"), "Blue & Orange": ("#1E3D59", "#FF6B35")}
primary_color, accent_color = colors[theme]

# Input Fields
col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("Enter your weight", min_value=10.0, max_value=600.0, step=0.1)
    if unit == "Imperial (lbs, inches)":
        weight *= 0.453592  # Convert lbs to kg
with col2:
    height = st.number_input("Enter your height", min_value=50.0, max_value=250.0, step=0.1)
    if unit == "Imperial (lbs, inches)":
        height *= 0.0254  # Convert inches to meters
    else:
        height /= 100  # Convert cm to meters

# Calculate BMI
if st.button("Calculate BMI", key="bmi_calc"):
    if height > 0 and weight > 0:
        bmi = round(weight / (height ** 2), 2)
        category = ""
        if bmi < 18.5:
            category = "Underweight 😟"
        elif 18.5 <= bmi < 24.9:
            category = "Normal ✅"
        elif 25 <= bmi < 29.9:
            category = "Overweight ⚠️"
        else:
            category = "Obese 🚨"
        
        # Show Result
        st.markdown(f"""
        <div style='text-align: center; background: {primary_color}; padding: 10px; border-radius: 10px; color: white;'>
            <h2>Your BMI: {bmi}</h2>
            <h3>{category}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Save BMI History
        history = st.session_state.get("bmi_history", [])
        history.append({"date": str(datetime.date.today()), "bmi": bmi})
        st.session_state["bmi_history"] = history

# Show BMI History
if "bmi_history" in st.session_state and len(st.session_state["bmi_history"]) > 1:
    st.subheader("📊 BMI History")
    fig, ax = plt.subplots()
    dates = [entry["date"] for entry in st.session_state["bmi_history"]]
    values = [entry["bmi"] for entry in st.session_state["bmi_history"]]
    ax.plot(dates, values, marker="o", color=primary_color)
    ax.set_xlabel("Date")
    ax.set_ylabel("BMI")
    ax.set_title("BMI Progress Over Time")
    st.pyplot(fig)

# Health Insights
st.sidebar.subheader("💡 Health Insights")
bmr = round(10 * weight + 6.25 * (height * 100) - 5 * 25 + 5, 2)  # Mifflin St Jeor Formula
st.sidebar.write(f"**Estimated BMR:** {bmr} Calories/day")
st.sidebar.write(f"**Ideal Weight Range:** {round(18.5 * height**2, 2)}kg - {round(24.9 * height**2, 2)}kg")
st.sidebar.write("**Body Fat Estimate:** BMI - Age Factor")

# Footer
st.markdown(f"""
<hr>
<center><b>Made with ❤️ by Aqsa</b></center>
""", unsafe_allow_html=True)




