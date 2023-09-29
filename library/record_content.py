# Record AMBOSS content in Ribsom HTML code
def record_content(mode=int):
    from .get_article_html_bigquery import get_article_html_bigquery
    from .get_article_html_manual import get_article_html_manual
    from .get_clean_markdown import get_clean_markdown

    import os

    # Get current working directory and articles folder path
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    articles_path = os.path.join(absolute_path, "../articles")

    # Create articles folder if it does not exist
    if not os.path.exists(articles_path):
        os.makedirs(articles_path)

    # Get content and title for file
    if mode == 1:
        content = get_article_html_manual()
    else:
        content = get_article_html_bigquery()
    cleaned_content = get_clean_markdown(content)
    title = cleaned_content.split("\n", 1)[0].replace("# ", "").strip()

    # Write content to file articles/{title}.txt
    filename = f"{articles_path}/{title}.md"
    with open(filename, "w") as myfile:
        myfile.write(cleaned_content)
