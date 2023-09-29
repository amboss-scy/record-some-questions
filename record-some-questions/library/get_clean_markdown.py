# Convert HTML content from function get_article_html to clean markdown code
def get_clean_markdown(input):
    from bs4 import BeautifulSoup
    import markdownify

    soup = BeautifulSoup(input, "html.parser")

    # Remove certain tags
    for span in soup.find_all("span", {"class": ["lektorat"]}):
        span.decompose()

    for span in soup.find_all("span"):
        span.unwrap()

    for tag in soup.find_all():
        if len(tag.get_text(strip=True)) == 0:
            tag.extract()

    return (
        markdownify.markdownify(str(soup), heading_style="ATX")
        .strip()
        .replace("\n\n\n", "\n\n")
    )
