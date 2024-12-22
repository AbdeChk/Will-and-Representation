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
import nltk
nltk.download('punkt_tab')
sns.set_style("whitegrid")  
sns.despine(top=True, right=True)

def create_word_frequency_plot(df, selected_book):
    """word frequency bar plot."""
    will = df[df['book_title'] == selected_book]['text_clean']
    tokens = word_tokenize(will.iloc[0])
    freq = Counter(tokens)
    sorted_freq = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
    
    top_words = list(sorted_freq.keys())[:15]
    top_freq = list(sorted_freq.values())[:15]
    
    fig, ax = plt.subplots(figsize=(15, 15))
    sns.barplot(y=top_words, x=top_freq, ax=ax, palette=["#333333"])
    plt.xlabel('Frequency', fontsize=25)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    
    return fig

def create_wordcloud(df, selected_book):
    """ word cloud visualization."""
    will = df[df['book_title'] == selected_book]['text_clean']
    tokens = word_tokenize(will.iloc[0])
    freq = Counter(tokens)
    
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
    """sentiment analysis pie chart."""
    def analyze_sentiment(word):
        analysis = TextBlob(word)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity < 0:
            return 'Negative'
        return 'Neutral'
    
    will = df[df['book_title'] == selected_book]['text_clean']
    tokens = word_tokenize(will.iloc[0])
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
    """book similarity network."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['text_clean'])
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    G = nx.Graph()
    
    for i, row in df.iterrows():
        G.add_node(row['book_title'])
        if row['book_title'] != selected_book:
            G.add_edge(
                selected_book,
                row['book_title'],
                weight=similarity_matrix[df.index[df['book_title'] == selected_book][0]][i]
            )
    
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='#808080', ax=ax)
    nx.draw_networkx_edges(G, pos, width=2, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif', ax=ax)
    
    ax.set_title(f'Similarity Network for "{selected_book}"')
    ax.axis('off')
    
    return fig