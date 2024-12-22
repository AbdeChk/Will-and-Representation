import pandas as pd

def load_and_clean_data(path):
    """load and clean text data."""
    df = pd.read_csv(path)
    
    # Fix book titles
    title_corrections = {
        8: 'The World As Will And Idea Vol1',
        9: 'The World As Will And Idea Vol2',
        10: 'The World As Will And Idea Vol3',
        12: 'Fourfold Root of the Principle'
    }
    
    for idx, title in title_corrections.items():
        df.loc[idx, 'book_title'] = title
    
    return df

def load_book_overview(path):
    """Load the book overview dataset."""
    return pd.read_csv(path)