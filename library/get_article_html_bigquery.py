# Record an AMBOSS article in HTML code (Ribosom source code) by automatically pulling content from BigQuery DB
def get_article_html_bigquery():
    from google.cloud import bigquery
    import contextlib

    while True:
        with contextlib.suppress(ValueError):
            article_id = int(input("Type article ID (no. only) and press enter: "))
            break

    query_client = bigquery.Client()
    query = f"""
        SELECT
            article_title,
            section_title,
            raw_content,
            position,
            question_id
        FROM `business-intelligence-194510.shared_views.content_base_data_current`
        WHERE article_id = {article_id}
        QUALIFY RANK() OVER (PARTITION BY section_id ORDER BY question_id DESC) <= 1
        ORDER BY position
    """
    query_results = query_client.query(query).to_dataframe()
    article_title = query_results.loc[0, "article_title"]
    columns_to_delete = [
        "article_title",
        "position",
        "question_id",
    ]
    for column in columns_to_delete:
        del query_results[column]

    html_content = f"<title>{article_title}</title>"
    prohibited_sections = [
        "Meditricks",
        "3D-Anatomie",
        "Wiederholungsfragen",
        "Kodierung",
    ]
    for i in range(len(query_results)):
        if all(
            prohibited_string not in query_results.loc[i, "section_title"]
            for prohibited_string in prohibited_sections
        ):
            html_content += f"\n<h1>{query_results.loc[i, 'section_title'].lstrip('- ')}</h1>\n{query_results.loc[i, 'raw_content']}"

    return html_content
