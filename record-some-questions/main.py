# Main menu
while True:
    choice = input(
        "\n1: Record question\ne: Exit\n\nWhat do you want to do (1/e): "
    ).lower()
    while choice not in ["1", "e"]:
        choice = input("What do you want to do (1/2/e): ").lower()
    if choice == "1":
        print()
        from library import record_question

        record_question.record_question()
    if choice == "e":
        print()
        break
