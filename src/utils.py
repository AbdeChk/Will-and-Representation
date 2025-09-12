import glob

def get_book_image(book_title):
    img_path = "./assets/*.jpg"
    images = glob.glob(img_path)
    for img in images:
        book_name = img.split('\\')[-1].split('.')[0]
        if book_name == book_title:
            return f"assets/{book_name}.jpg"
    return None

def get_book_details(df, book_title):
    row = df.loc[df['book_title'] == book_title].iloc[0]
    return row['publishing_date'], row['overview']
