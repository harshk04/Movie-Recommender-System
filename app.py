
import streamlit as st
import requests
import pickle
import gzip

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

page_bg_img = '''
<style>
body {
background-image: url("bg.jpeg");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Load movie data and similarity matrix from the compressed pickle files
# with gzip.open('movie_list.pkl.gz', 'rb') as f:
#     movies = pickle.load(f)
movies = pickle.load(open('movie_list.pkl', 'rb'))

with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

# Add a background image to the entire app
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://wallpapers.com/movie.jpg") no-repeat center center fixed;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar navigation...




# Sidebar navigation
selected = st.sidebar.radio("Navigation", ['Home Page', 'Movie Recommender System', 'Contact Me'])
st.sidebar.header("Project Creator")
st.sidebar.info(
    "This web application was created by [Harsh Kumawat](https://www.linkedin.com/in/harsh-kumawat-069bb324b/). "
    "Feel free to reach out for any questions or feedback."
)

# Main content area
if selected == 'Home Page':
    st.header('Welcome to Movie Recommender System')
    st.write("This is a simple web application built using Streamlit, allowing users to discover movie recommendations based on their selected preferences.")

    st.header("Launching the Streamlit Web Application")
    st.write("The Streamlit application has the following main sections:")

    st.write("Home Page")
    st.write("The landing page of the web application displays the title 'Movie Recommender System' It serves as an introduction to the application.")
    st.write("Movie Recommender System")
    st.write(" Users can input a movie title or select one from the dropdown menu. Upon clicking the 'Show Recommendation' button, the system will display a list of recommended movies similar to the selected one.")
    st.write("Contact Me")
    st.write("This section provides contact information for getting in touch with the developer or project owner.")

elif selected == 'Movie Recommender System':
    st.header('Movie Recommender System')
    movie_list = movies['title'].values
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

    if st.button('Show Recommendation', key='show_recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
elif selected == 'Contact Me':
    st.header('Contact Me')
    st.write("Please fill out the form below to get in touch with me.")

    # Input fields for user's name, email, and message
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Message", height=150)

    # Submit button
    if st.button("Submit"):
        if name.strip() == "" or email.strip() == "" or message.strip() == "":
            st.warning("Please fill out all the fields.")
        else:
            send_email_to = 'kumawatharsh2004@email.com'
            st.success("Your message has been sent successfully!")

# Adding the footer
st.markdown(
    '<div style="position: fixed; bottom: 0; width: 100%; text-align: center;">'
    'Made with ❤️ by <a href="https://www.linkedin.com/in/harsh-kumawat-069bb324b/">Harsh</a>'
    '</div>',
    unsafe_allow_html=True
)
