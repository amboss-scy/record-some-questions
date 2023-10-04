# Record an AMBOSS question in HTML code (Ribosom source code) by automatically pulling content from BigQuery DB
def get_question_from_bigquery():
    from google.cloud import bigquery
    import contextlib

    while True:
        with contextlib.suppress(ValueError):
            question_id = int(
                input("Type or paste question ID here (no. only) and press Enter: ")
            )
            break

    query_client = bigquery.Client()
    query = f"""
        SELECT
            question_title as question,
            answer_id,
            answer,
            is_correct,
            article_id,
            section_id
        FROM `business-intelligence-194510.shared_views.content_base_data_current`
        WHERE question_id = {question_id}
        ORDER BY answer_id
    """
    query_results = query_client.query(query).to_dataframe()

    try:
        question = query_results.loc[0, "question"]
    except KeyError:
        print("Error: No question with this ID in remote database.")
        return

    columns_to_delete = ["question", "answer_id"]
    for column in columns_to_delete:
        del query_results[column]
    answers_df = query_results

    return question_id, question, answers_df
