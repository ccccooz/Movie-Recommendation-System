import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Streamlit app
st.title("Genre-Specific and Combined Movie Recommendation System")

# Movie genres
genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller", "Adventure", "Animation", "Fantasy"]

# User inputs for two favorite genres and favorite movies
fav_genre_1 = st.selectbox("Select your 1st favorite genre", genres)
fav_genre_2 = st.selectbox("Select your 2nd favorite genre", genres)
fav_movie_1 = st.text_input("Enter your 1st favorite movie")
fav_movie_2 = st.text_input("Enter your 2nd favorite movie")
fav_movie_3 = st.text_input("Enter your 3rd favorite movie")

# Generate button
if st.button("Generate Recommendations"):
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system",
             "content": "You are a helpful movie recommendation assistant. Provide movie recommendations based on the user's two favorite genres and top 3 favorite movies. Respond in separate tables: one for each genre and one for movies that combine both genres. Each table should have columns: Movie Title, Genre, IMDb Rating, Plot Summary, and Comments from viewers. Sort the movies by IMDb rating in descending order."}
        ]

    # Gather user input
    if fav_genre_1 and fav_genre_2 and fav_movie_1 and fav_movie_2 and fav_movie_3:
        user_input = f"Favorite Genres: {fav_genre_1} & {fav_genre_2}\n\nFavorite Movies: 1. {fav_movie_1}, 2. {fav_movie_2}, 3. {fav_movie_3}"

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display user input
        st.write("## Your Input")
        st.write(user_input)

        # Get AI response
        with st.spinner("Generating recommendations..."):
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
            )
            response = completion.choices[0].message.content

        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Parse the response into separate sections
        genre_1_table, genre_2_table, combined_genres_table = response.split("\n\n", 2)

        # Display recommendations
        st.write(f"## Recommendations for {fav_genre_1}")
        st.markdown(genre_1_table)

        st.write(f"## Recommendations for {fav_genre_2}")
        st.markdown(genre_2_table)

        st.write(f"## Recommendations for {fav_genre_1} & {fav_genre_2}")
        st.markdown(combined_genres_table)

        # Write response to file
        with open('response.md', 'w') as f:
            f.write(response)

        # Add a section for displaying the contents of response.md
        st.subheader("Latest Response")
        try:
            with open('response.md', 'r') as f:
                st.markdown(f.read())
        except FileNotFoundError:
            st.write("No response generated yet.")
    else:
        st.write("Please select two genres and enter your favorite movies to get recommendations.")
