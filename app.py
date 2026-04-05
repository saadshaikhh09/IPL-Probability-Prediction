import streamlit as st
import pickle
import pandas as pd

teams = ['Chennai Super Kings',
 'Delhi Capitals',
 'Gujarat Titans',
 'Kolkata Knight Riders',
 'Lucknow Super Giants',
 'Mumbai Indians',
 'Punjab Kings',
 'Rajasthan Royals',
 'Royal Challengers Bengaluru',
 'Sunrisers Hyderabad']

cities = ['Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
       'Hyderabad', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban',
       'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Rajkot', 'Kanpur', 'Bengaluru', 'Indore', 'Dubai', 'Sharjah',
       'Navi Mumbai', 'Lucknow', 'Guwahati', 'Mohali']

pipe = pickle.load(open('pipe.pkl','rb'))
st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))

# remove batting team from bowling options
available_bowling_teams = [team for team in teams if team != batting_team]

with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(available_bowling_teams))

selected_city = st.selectbox('Select host city',sorted(cities))

target = st.number_input('Target', step=1, format="%d")

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Score', step=1, format="%d")
with col4:
    overs = st.number_input('Overs completed', step=1, format="%d")
with col5:
    wickets = st.number_input('Wickets out', step=1, format="%d")
if st.button('Predict Probability'):

    if overs == 0:
        st.warning("Overs cannot be zero. Please enter a valid value (1–20).")
        st.stop()
    else :
        runs_left = target - score
        balls_left = 120 - (overs*6)
        wickets = 10 - wickets
        crr = score/overs
        rrr = (runs_left*6)/balls_left

        input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        st.header(batting_team + "- " + str(round(win*100)) + "%")
        st.header(bowling_team + "- " + str(round(loss*100)) + "%")
