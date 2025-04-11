import streamlit as st
from fpdf import FPDF
import datetime
import os

# Custom PDF class
class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, 'BMI & Calorie Report', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

# PDF generation function
def generate_pdf(age, gender, weight, height, bmi, category, bmr, calories, activity_level):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Helvetica', '', 12)

    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, f"Age: {age} years", ln=True)
    pdf.cell(0, 10, f"Gender: {gender}", ln=True)
    pdf.cell(0, 10, f"Weight: {weight} kg", ln=True)
    pdf.cell(0, 10, f"Height: {height} cm", ln=True)
    pdf.cell(0, 10, f"BMI: {bmi:.2f} ({category})", ln=True)
    pdf.cell(0, 10, f"BMR: {bmr:.2f} calories/day", ln=True)
    pdf.cell(0, 10, f"Activity Level: {activity_level}", ln=True)
    pdf.cell(0, 10, f"Recommended Daily Calories: {calories:.2f} cal/day", ln=True)

    filename = f"bmi_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# BMI and BMR calculations
def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m ** 2)

def calculate_bmr(weight, height, age, gender):
    if gender.lower() == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_calories(bmr, activity_level):
    levels = {
        "Sedentary": 1.2,
        "Lightly active": 1.375,
        "Moderately active": 1.55,
        "Very active": 1.725,
        "Super active": 1.9
    }
    return bmr * levels.get(activity_level, 1.2)

# Streamlit UI
st.title("BMI and Calorie Calculator")

age = st.number_input("Enter your age:", min_value=1, max_value=120)
gender = st.radio("Select Gender:", ["Male", "Female"])
weight = st.number_input("Enter your weight (kg):", min_value=1.0)
height = st.number_input("Enter your height (cm):", min_value=1.0)
activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly active", "Moderately active", "Very active", "Super active"])

if st.button("Calculate"):
    bmi = calculate_bmi(weight, height)
    category = get_bmi_category(bmi)
    bmr = calculate_bmr(weight, height, age, gender)
    calories = calculate_calories(bmr, activity_level)

    st.subheader("Results")
    st.write(f"**BMI:** {bmi:.2f} ({category})")
    st.write(f"**BMR:** {bmr:.2f} calories/day")
    st.write(f"**Daily Calorie Needs:** {calories:.2f} calories/day")

    pdf_file = generate_pdf(age, gender, weight, height, bmi, category, bmr, calories, activity_level)
    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF Report", f, file_name=pdf_file, mime="application/pdf")
