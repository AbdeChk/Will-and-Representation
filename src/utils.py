import glob

def get_book_image(book_title):
    img_path = "./img/*.jpg"
    images = glob.glob(img_path)
    for img in images:
        book_name = img.split('\\')[-1].split('.')[0]
        if book_name == book_title:
            return f"img/{book_name}.jpg"
    return None

def get_book_details(df, overview_df, book_title):
    publishing_date = df.loc[df['book_title'] == book_title, 'publishing_date'].values[0]
    overview = overview_df.loc[overview_df['book'] == book_title, 'overview'].values[0]
    return publishing_date, overview