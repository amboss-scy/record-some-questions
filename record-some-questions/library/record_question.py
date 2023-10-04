# Record AMBOSS question
def record_question():
    from .get_question_from_bigquery import get_question_from_bigquery
    from .get_clean_markdown import get_clean_markdown
    import os

    # Get current working directory and articles folder path
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    questions_path = os.path.join(absolute_path, "../questions")

    # Create questions folder if it does not exist
    if not os.path.exists(questions_path):
        os.makedirs(questions_path)

    # Get content and title for file
    question_tuple = get_question_from_bigquery()
    try:
        question_id = question_tuple[0]
        question = "### QUESTION\n\n" + get_clean_markdown(question_tuple[1]).strip()
        answers_df = question_tuple[2]
    except TypeError:
        return

    answers = []
    for i in range(len(answers_df)):
        is_correct = answers_df.loc[i, "is_correct"] == 1
        has_article_id = answers_df.notna().loc[i, "article_id"]
        has_section_id = answers_df.notna().loc[i, "section_id"]
        answer = (
            f"### OPTION {i + 1}\n\n"
            + get_clean_markdown(answers_df.loc[i, "answer"]).strip()
            + f"\n\n* CORRECT: {'YES' if is_correct else 'NO'}\n* ARTICLE ID: {answers_df.loc[i, 'article_id'] if has_article_id else 'NONE'}\n* SECTION ID: {answers_df.loc[i, 'section_id']if has_section_id else 'NONE'}"
        )
        answers.append(answer)

    out_str = question
    for answer in answers:
        out_str += "\n\n" + answer

    # Write out_str to file questions/{question_id}.txt
    fname = f"{questions_path}/{question_id}.md"
    with open(fname, "w") as f:
        f.write(out_str)
