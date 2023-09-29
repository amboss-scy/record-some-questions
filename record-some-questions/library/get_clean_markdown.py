# Convert HTML content from function get_article_html to clean markdown code
def get_clean_markdown(content):  # sourcery skip: avoid-builtin-shadow
    from bs4 import BeautifulSoup
    import re
    import markdownify

    soup = BeautifulSoup(content, "html.parser")

    # Remove certain tags
    for img in soup.find_all("img"):
        img.decompose()

    for span in soup.find_all(
        "span", {"class": ["lektorat", "erklaerung", "physician", "postponed"]}
    ):
        span.decompose()

    for span in soup.find_all("span"):
        span.unwrap()

    heading_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
    for heading in soup.find_all(heading_tags):
        heading.string = heading.text.strip()

    for table in soup.find_all("table"):
        for sub_tag in ["ul", "ol", "p", "li"]:
            for tag in table.find_all(sub_tag):
                tag.unwrap()

        for cell in table.find_all(["th", "td"]):
            string = re.sub("(<td.*?>)|(</td>)|(<th.*?>)|(</th>)", "", str(cell))
            string = "".join(
                [s for s in string.strip().splitlines(True) if s.strip("\r\n").strip()]
            )
            string = re.sub("\n", " — ", string)
            string = re.sub("<br/?>", " — ", string)
            cell.string = string

    for tag in soup.find_all():
        if len(tag.get_text(strip=True)) == 0:
            tag.extract()

    # Convert to markdown and make final replacements
    markdown_content = markdownify.markdownify(str(soup), heading_style="ATX")
    markdown_content = markdown_content.replace("\t", "    ")
    markdown_content = "# " + re.sub("\n#", "\n##", markdown_content)
    markdown_content = (
        markdown_content.split("\n", 1)[0]
        + "\n\n"
        + "\n".join(markdown_content.split("\n")[1:])
    )
    markdown_content = re.sub("\n\n\n+", "\n\n", markdown_content).rstrip("\n")

    return markdown_content
