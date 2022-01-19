from re import T
import streamlit as st

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import requests

from app import rec_collaborative_filtering_by_user

# user-to-user collaborative filtering
with open('user_user_sim_matrix.pkl', 'rb') as f:
    user_user_sim_matrix = pickle.load(f)

with open('customer_item_matrix.pkl', 'rb') as f:
    customer_item_matrix = pickle.load(f)

def rec_collaborative_filtering_by_user(user1):

    user2 = user_user_sim_matrix.loc[user1].sort_values(ascending=False).index[1]
    print('most similar user from user {} is user {}\n'.format(user1, user2))

    user_A = customer_item_matrix.loc[user1]
    games_played_by_A = set()

    for i in range(len(user_A)):
        if user_A[i] == 1:
            games_played_by_A.add(list(user_A.index)[i])

    print('games played by user {} are:'.format(user1))
    print(games_played_by_A,'\n')

    user_B = customer_item_matrix.loc[user2]
    games_played_by_B = set()

    for i in range(len(user_B)):
        if user_B[i] == 1:
            games_played_by_B.add(list(user_B.index)[i])

    print('games played by user {} are:'.format(user2))
    print(games_played_by_B,'\n')

    items_to_recommend_B = games_played_by_A - games_played_by_B
    print('recommendation games to user {} are:\n{}'.format(user2, items_to_recommend_B))

    return games_played_by_A, user2, games_played_by_B, items_to_recommend_B

with open('game_df.pkl', 'rb') as f:
    game_df = pickle.load(f)

game_fr = game_df['Title'].values

st.image('https://tedis.telkom.design/assets/download_logo/logo-gameqoo.png', width=150)
st.title('Recommendation System')

user_A = st.text_input('Input user ID')

if st.button('Find similar user'):
    games_played_by_A, user_B, games_played_by_B, items_to_recommend_B = rec_collaborative_filtering_by_user(user_A)

    text1 = 'Most similar user from user ' + user_A + ' (User_A) is user ' + user_B + ' (User_B'
    st.text(text1)

    text2 = 'Games played by User_A are: '
    st.text(text2)

    for count, game in enumerate(games_played_by_A):
        try:
            st.subheader(game)
            st.image(game_df.loc[game_df['Title'] == game].CoverWebUrl.values[0])
        except:
            st.caption('Image is Unavailable :(')

    text3 = 'Games played by User_B are: '
    st.text(text3)

    for count, game in enumerate(games_played_by_B):
        try:
            st.subheader(game)
            st.image(game_df.loc[game_df['Title'] == game].CoverWebUrl.values[0])
        except:
            st.caption('Image is Unavailable :(')

    text4 = 'Games to recommend User_B are:'
    st.text(text4)

    for count, game in enumerate(items_to_recommend_B):
        try:
            st.subheader(game)
            st.image(game_df.loc[game_df['Title'] == game].CoverWebUrl.values[0])
        except:
            st.caption('Image is Unavailable :(')