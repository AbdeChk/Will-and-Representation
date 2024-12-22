import streamlit as st
from src.data_loader import load_and_clean_data, load_book_overview
from src.visualizations import (create_word_frequency_plot, create_wordcloud, create_sentiment_plot,
                                create_similarity_network)
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
        "A simple attempt to highlight the work of philosopher [Arthur Schopenhauer](https://en.wikipedia.org/wiki/Arthur_Schopenhauer) through visualizations. The project is still a work in progress, and I'd appreciate your feedback! 😃 Let me know if you're interested in collaborating." )

    st.sidebar.markdown("<br>" * 2, unsafe_allow_html=True)

    st.sidebar.header("Resources") 
    st.sidebar.markdown(
        """
        - [Schopenhauer Work Corpus](https://www.kaggle.com/datasets/akouaorsot/schopenhauer-work-corpus)
        - [Project Gutenberg](https://www.gutenberg.org/)
        """)
    st.sidebar.markdown("---")
    st.sidebar.markdown(
            '<h5>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://www.facebook.com/chabdellwahad/">@ChkAbde</a></h5>',
            unsafe_allow_html=True,
        )
    
def display_header():
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image('img/arthur.jpg')
    
    quote = "The more unintelligent a man is, the less mysterious existence seems to him. - Arthur Schopenhauer-"
    styled_quote = f'<blockquote style="font-style: italic; text-align: center; color: black; font-size: 15px;">{quote}</blockquote>'
    st.markdown(styled_quote, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  

def display_book_details(df, overview_df, selected_book):
    left_side, cent_side = st.columns([1, 2])
    
    with left_side:
        book_image = get_book_image(selected_book)
        if book_image:
            st.image(book_image, width=250)
    
    with cent_side:
        publishing_date, overview = get_book_details(df, overview_df, selected_book)
        
        st.markdown(f"""
            <h1 style='font-size: 24px; 
                       color: #1E3D59; 
                       margin-bottom: 0px;'>
                {selected_book}
            </h1>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <p style='font-size: 16px; 
                      color: #666666; 
                      font-style: italic; 
                      margin-top: 5px;'>
                Published: {publishing_date}
            </p>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='background-color: #F7F9FC;
                        padding: 15px;
                        border-radius: 5px;
                        border-left: 5px solid #1E3D59;'>
                <p style='font-size: 16px; 
                          line-height: 1.6;
                          color: #333333;'>
                    {overview}
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

def display_visualizations(df, selected_book):
    col1, col2 = st.columns(2)
    with col1:
        freq_plot = create_word_frequency_plot(df, selected_book)
        st.pyplot(freq_plot)
    
    with col2:
        wordcloud = create_wordcloud(df, selected_book)
        st.image(wordcloud)
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    with col3:
        sentiment_plot = create_sentiment_plot(df, selected_book)
        st.pyplot(sentiment_plot)
    
    with col4:
        network_plot = create_similarity_network(df, selected_book)
        st.pyplot(network_plot)
        
def main():
    setup_page_config()
    display_sidebar()  
    display_header()
    
    df = load_and_clean_data("data/data.csv")
    overview_df = load_book_overview("data/book_overview.csv")
    
    selected_book = st.selectbox('Select a book:', df['book_title'])
    
    display_book_details(df, overview_df, selected_book)
    display_visualizations(df, selected_book)

if __name__ == "__main__":
    main()
