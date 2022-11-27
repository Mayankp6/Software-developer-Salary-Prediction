from gettext import npgettext
import streamlit as st
import pickle
import numpy as np

# Loading our model 

def load_model():

    with open('saved_steps.pkl' , 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data['model']
le_edu = data['le_edu']
le_con = data['le_con']

def show_predicted_page():

    st.title("Software Engineer Salary Prediction")
    st.write("""### We need some more information to predict salary """)

    countries = {

    "United States",
    "India",
    "United Kingdom",
    "Germany",
    "Canada",
    "Brazil",
    "France" ,             
    "Spain"   ,              
    "Australia",      
    "Netherlands",    
    "Poland",         
    "Italy",                 
    "Russian Federation", 
    "Sweden"

    }

    education = {
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
        "Less than a Bachelors"
    }

    country = st.selectbox("Country",countries)
    education_level = st.selectbox("Education",education)
    experience = st.slider("Years of Experience",0,50,3)

    ok = st.button("Calculate Salary ")
    if ok:

        X = np.array([[country,education_level,experience]])
        X[:,0] = le_con.transform(X[:,0])
        X[:,1] = le_edu.transform(X[:,1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The Estimated Salary is : ${salary[0]:.2f} ")
