import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns
import networkx as nx
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
from collections import Counter
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache
import nltk

nltk.download('punkt')

sns.set_style("whitegrid")  
sns.despine(top=True, right=True)

_tfidf_cache = {}

@lru_cache(maxsize=128)
def _tokenize_text(text: str):
    return tuple(word_tokenize(text)) 

def _get_tokens(df, selected_book):
    row = df.loc[df['book_title'] == selected_book, 'text_clean']
    if row.empty:
        return []
    return list(_tokenize_text(row.iloc[0]))

def _get_word_freq(tokens, top_n=None):
    freq = Counter(tokens)
    if top_n:
        return dict(freq.most_common(top_n))
    return dict(freq)

def _get_tfidf(df):
    df_id = id(df) 
    if df_id not in _tfidf_cache:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(df['text_clean'])
        similarity_matrix = cosine_similarity(tfidf_matrix)
        _tfidf_cache[df_id] = (vectorizer, similarity_matrix, df['book_title'].tolist())
    return _tfidf_cache[df_id]

def create_word_frequency_plot(df, selected_book):
    tokens = _get_tokens(df, selected_book)
    if not tokens:
        raise ValueError(f"No text found for book '{selected_book}'")
    
    freq = _get_word_freq(tokens, top_n=15)
    
    fig, ax = plt.subplots(figsize=(15, 15))
    sns.barplot(
        y=list(freq.keys()), 
        x=list(freq.values()), 
        ax=ax, 
        palette=["#333333"]
    )
    plt.xlabel('Frequency', fontsize=25)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    
    return fig

def create_wordcloud(df, selected_book):
    tokens = _get_tokens(df, selected_book)
    if not tokens:
        raise ValueError(f"No text found for book '{selected_book}'")
    
    freq = _get_word_freq(tokens)
    
    wordcloud = WordCloud(
        width=400, height=400,
        random_state=1,
        background_color='white',
        colormap='binary',
        collocations=False,
        stopwords=STOPWORDS
    )
    wordcloud.generate_from_frequencies(freq)
    
    return wordcloud.to_image()

def create_sentiment_plot(df, selected_book):
    tokens = _get_tokens(df, selected_book)
    if not tokens:
        raise ValueError(f"No text found for book '{selected_book}'")

    def analyze_sentiment(word):
        analysis = TextBlob(word)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity < 0:
            return 'Negative'
        return 'Neutral'
    
    sentiments = [analyze_sentiment(word) for word in tokens]
    sentiment_counts = pd.Series(sentiments).value_counts()
    
    fig, ax = plt.subplots(figsize=(6, 6))
    sentiment_counts.plot.pie(
        autopct='%1.1f%%',
        startangle=90,
        colors=['#31333f', '#878080', '#c2b6b6']
    )
    centre_circle = plt.Circle((0, 0), 0.7, color='white', fc='white', linewidth=1.25)
    fig.gca().add_artist(centre_circle)
    
    ax.set_title(f"Sentiment in {selected_book}")
    plt.legend(sentiment_counts.index, loc='best')
    ax.axis('equal')
    
    return fig

def create_similarity_network(df, selected_book):
    if selected_book not in df['book_title'].values:
        raise ValueError(f"Book '{selected_book}' not found in DataFrame")

    vectorizer, similarity_matrix, titles = _get_tfidf(df)
    selected_idx = titles.index(selected_book)

    fig, ax = plt.subplots(figsize=(6, 6))
    G = nx.Graph()
    
    for i, title in enumerate(titles):
        G.add_node(title)
        if title != selected_book:
            G.add_edge(
                selected_book,
                title,
                weight=similarity_matrix[selected_idx, i]
            )
    
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='#808080', ax=ax)
    nx.draw_networkx_edges(G, pos, width=2, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif', ax=ax)
    
    ax.set_title(f'Similarity Network for "{selected_book}"')
    ax.axis('off')
    
    return fig
