import streamlit as st
import pandas as pd
import pickle

# Load Model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Load Polynomial Features
with open("poly.pkl", "rb") as f:
    polynomial_features = pickle.load(f)

# Page Configuration
st.set_page_config(
    page_title="Insurance Cost Predictor",
    page_icon="💰",
    layout="wide"
)

# Header
st.title("💰 Medical Insurance Cost Predictor")
st.markdown("""
Predict medical insurance charges using Polynomial Regression.
Fill in the details below and click the Predict button.
""")

st.divider()

# Input Section
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 64, 25)
    sex = st.selectbox("Gender", ["Male", "Female"])
    bmi = st.number_input(
        "BMI",
        min_value=15.0,
        max_value=55.0,
        value=25.0,
        step=0.1
    )

with col2:
    children = st.slider("Number of Children", 0, 5, 0)
    smoker = st.selectbox("Smoker", ["No", "Yes"])
    region = st.selectbox(
        "Region",
        ["northeast", "northwest", "southeast", "southwest"]
    )

# Encoding
sex = 1 if sex == "Male" else 0
smoker = 1 if smoker == "Yes" else 0

region_northwest = 0
region_southeast = 0
region_southwest = 0

if region == "northwest":
    region_northwest = 1
elif region == "southeast":
    region_southeast = 1
elif region == "southwest":
    region_southwest = 1

# Predict Button
if st.button("Predict Insurance Cost", use_container_width=True):

    input_data = pd.DataFrame({
        "age": [age],
        "sex": [sex],
        "bmi": [bmi],
        "children": [children],
        "smoker": [smoker],
        "region_northwest": [region_northwest],
        "region_southeast": [region_southeast],
        "region_southwest": [region_southwest]
    })

    # Apply Polynomial Transformation
    input_poly = polynomial_features.transform(input_data)

    # Prediction
    prediction = model.predict(input_poly)[0]

    st.success(
        f"Estimated Insurance Cost: ₹ {prediction:,.2f}"
    )


# Footer
st.divider()
st.markdown("""
### Project Information
- **Project:** Medical Insurance Cost Prediction
- **Algorithm:** Polynomial Regression (Degree 3)
- **Developer:** Tejas Babar
- **Tools Used:** Python, Pandas, Scikit-Learn, Streamlit
""")