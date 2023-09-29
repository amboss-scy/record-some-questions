def change_recording_mode():
    while True:
        mode = input(
            "1: Manual mode\n2: BigQuery mode\n\nWhich mode do you choose (1/2): "
        ).lower()
        while mode not in ["1", "2"]:
            mode = input("Which mode do you choose (1/2): ").lower()
        return mode
