import streamlit as st
import pandas as pd
import numpy as np
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.write("""
# Elon Twitter Buyout Sentiment App

This app displays twitter sentiment towards Elon's Twitter buyout based keywords. 

#### Data source:

Ten thousand tweets from twitter users from 4 different time points:
- 4/5/21 as control
- 4/14/22 when Elon's offer was announced
- 4/25/22 when Elon's offer was accepted
- 5/10/22 when Elon announces he would unban Trump

Code can be found on [my Github repo](https://github.com/JoshJingtianWang/ElonMusk_NLP).

---
""")

streamlit_df = pickle.load(open('streamlit_df.pkl', 'rb'))
global_average_score = 0.107

#st.sidebar.header('User Input Features')

VADER_test = st.sidebar.text_input('First, test the VADER sentiment analyzer with your own sentence:', 'type your sentence here:')
analyzer = SentimentIntensityAnalyzer()
my_score = analyzer.polarity_scores(VADER_test)['compound']
with st.sidebar:
    st.write("#### The sentiment score of your sentence is: %.3f"%my_score)
    st.write('\n')
    st.write("#### Next, input search parameters to get twitter sentiment:")
#st.sidebar.markdown("""
#[Example CSV input file](./example.csv)
#""")

# Collects user input features into dataframe
#uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
uploaded_file = None 

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    def user_input_features():
        
        keyword = st.sidebar.text_input('Keyword (case insensitive):', 'eg: Trump')
        politics = st.sidebar.selectbox('Conservative:',('Any','True', 'False'))
        date = st.sidebar.selectbox('Date:',('Any','2021-04-05','2022-04-14','2022-04-25','2022-05-10'))
        
        pol_answermap={'True':[True],'False':[False],'Any':[True, False]}
        date_answermap={'2021-04-05':['2021-04-05'],
                        '2022-04-14':['2022-04-14'],
                        '2022-04-25':['2022-04-25'],
                        '2022-05-10':['2022-05-10'],
                        'Any':['2021-04-05','2022-04-14','2022-04-25','2022-05-10']}
                        
        pol_answer=pol_answermap[politics]
        date_answer=date_answermap[date]
        
        df_by_conditions = streamlit_df[(streamlit_df['Text_lowercase'].str.contains(keyword.lower())) & 
                                     (streamlit_df['Date'].isin(date_answer)) & 
                                     (streamlit_df['Conservative'].isin(pol_answer))]
        #st.write(df_by_conditions)
        score = df_by_conditions.VADER_Compound.mean()
        
        #with st.sidebar:
            #st.write("This code will be printed to the sidebar.")
        
        data = {'Keyword': keyword,
                'Conservative': politics,
                'Date': date}

        features = pd.DataFrame(data, index=[0])
        return score, features
    query_score, input_df = user_input_features()

# Displays the user input features
st.subheader('Please the left sidebar to input your features:')
st.write(input_df)

st.write('---')

if query_score > 0.05:
    cat = 'positive'
elif query_score < -0.05:
    cat = 'negative'
else:
    cat = 'neutral'
            
st.write('''
#### The average sentiment score of tweets matching your condition is:
#### %.3f, which is considered %s. 
'''%(query_score, cat))

st.write('\n')
st.write('\n')

st.write('See how your scores compare to the global average:')
my_data = {'Global Average':0.107, 'Your Query Score':query_score}

#plotting the result in barplot
fig = plt.figure(figsize=(10, 4))
sns.barplot(x=list(my_data.keys()),y=list(my_data.values()))
st.pyplot(fig)