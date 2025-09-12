import streamlit as st
from src.data_loader import load_data
from src.visualizations import create_word_frequency_plot, create_wordcloud, create_sentiment_plot, create_similarity_network
from src.utils import get_book_image, get_book_details

def setup_page_config():
    st.set_page_config(
        page_title='Arthur Schopenhauer',
        page_icon='🦉',
        layout='wide'
    )

def display_sidebar():
    st.sidebar.header("About")
    st.sidebar.markdown(
        "A simple attempt to highlight the work of philosopher [Arthur Schopenhauer](https://en.wikipedia.org/wiki/Arthur_Schopenhauer) through visualizations. Feedback welcome! 😃"
    )
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.sidebar.header("Resources")
    st.sidebar.markdown(
        """
        - [Schopenhauer Work Corpus](https://www.kaggle.com/datasets/akouaorsot/schopenhauer-work-corpus)
        - [Project Gutenberg](https://www.gutenberg.org/)
        """
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        '<h5>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" height="16">&nbsp by <a href="https://www.facebook.com/chabdellwahad/">@ChkAbde</a></h5>',
        unsafe_allow_html=True,
    )

def display_header():
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image('assets/arthur.jpg', width=250)
    
    quote = "The more unintelligent a man is, the less mysterious existence seems to him. - Arthur Schopenhauer"
    st.markdown(f'<blockquote style="font-style: italic; text-align: center; color: black; font-size: 15px;">{quote}</blockquote>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

def display_book_details(df, selected_book):
    left, center = st.columns([1, 2])
    
    with left:
        img = get_book_image(selected_book)
        if img:
            st.image(img, width=250)
    
    with center:
        publishing_date, overview = get_book_details(df, selected_book)
        st.markdown(f"<h1 style='font-size:24px;color:#1E3D59'>{selected_book}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:16px;color:#666666;font-style:italic'>Published: {publishing_date}</p>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:#F7F9FC;padding:15px;border-radius:5px;border-left:5px solid #1E3D59;'><p style='font-size:16px;color:#333'>{overview}</p></div>", unsafe_allow_html=True)

    st.markdown("---")

def display_visualizations(df, selected_book):
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(create_word_frequency_plot(df, selected_book))
    with col2:
        st.image(create_wordcloud(df, selected_book))
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    with col3:
        st.pyplot(create_sentiment_plot(df, selected_book))
    with col4:
        st.pyplot(create_similarity_network(df, selected_book))

def main():
    setup_page_config()
    display_sidebar()
    display_header()
    
    df = load_data("books/books.csv")
    
    selected_book = st.selectbox('Select a book:', df['book_title'])
    
    display_book_details(df, selected_book)
    display_visualizations(df, selected_book)

if __name__ == "__main__":
    main()
