# Set default mode for content recording to manual
mode = 1

# Main menu
while True:
    choice = input(
        "\n1: Change recording mode (default: manual)\n2: Record article\n3: Create embeddings\n4: Ask question\ne: Exit\n\nWhat do you want to do (1/2/3/4/e): "
    ).lower()
    while choice not in ["1", "2", "3", "4", "e"]:
        choice = input("What do you want to do (1/2/4/3/e): ").lower()
    if choice == "1":
        print()
        from library import change_recording_mode

        mode = change_recording_mode.change_recording_mode()
    if choice == "2":
        print()
        from library import record_content

        record_content.record_content(mode)
    if choice == "3":
        print()
        from library import embed_md_documents

        embed_md_documents.embed_md_documents()
    if choice == "4":
        print()
        from library import retrieval_qa

        retrieval_qa.retrieval_qa()
    if choice == "e":
        print()
        break
