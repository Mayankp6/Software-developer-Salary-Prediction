import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories,cutoff):
    countries = {}
    for i in range(len(categories)):
        
        if categories.values[i] >= cutoff:
            countries[categories.index[i]] = categories.index[i]
        else:
            countries[categories.index[i]] = 'Other'
            
    return countries
        
def clean_edu(ed):
    
    if 'Bachelor’s degree' in ed:
        return 'Bachelor’s degree'
    elif 'Master’s degree' in ed:
        return 'Master’s degree'
    elif 'Professional degree' in ed or 'Other Doctoral' in ed:
        return 'Post grad'
    else:
        return 'Less than a Bachelors'

def clean_years(cat):
        if cat == 'Less than 1 year':
            return 0.5
        elif cat == 'More than 50 years':
            return 50
        else:
            return float(cat)

@st.cache
def load_data():
    df = pd.read_csv('clean_dataset.csv')
    # df = df[['Country','Employment','ConvertedComp','EdLevel','YearsCodePro']]
    # df = df.dropna()
    df = df.rename({'ConvertedComp':'Salary'} , axis=1)
    df = df[df['Employment'] == 'Employed full-time']

    df = df.drop('Employment',axis=1)

    country_map = shorten_categories(df.Country.value_counts() , 400)

    df['Country'] =  df['Country'].map(country_map)

    df = df[df['Salary'] <= 250000]
    df = df[df['Salary']>=10000]
    df = df[df['Country'] != 'Other']

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_years)
    df['EdLevel'] = df['EdLevel'].apply(clean_edu)

    return df

df = load_data()


def show_explore_page():

    st.title("Exxplore Software Engineer Salaries")
    st.write("""#### Stack Overflow Survey 2020 """)

    data = df['Country'].value_counts()

    fig1,ax1 = plt.subplots()
    ax1.pie(data , labels=data.index , autopct='%1.1f%%' ,shadow=True,startangle=90 )
    ax1.axis('equal')

    st.write('''### Number of Data from different Countries''')
    st.pyplot(fig1)


    st.write('''### Mean Salaries based on Countries''')

    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)


    st.write('''### Mean Salaries based on Experience''')

    data = df.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)
