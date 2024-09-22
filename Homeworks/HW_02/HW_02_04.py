default_time = 60


def training_session(rounds):
    time_per_round = default_time
    is_default_time = True  # вирішив відтворити приклад використання повністю

    def adjust_time():
        nonlocal time_per_round
        nonlocal is_default_time
        time_per_round = time_per_round - 5
        is_default_time = False
        return time_per_round

    for each_round in range(1, rounds + 1):
        if is_default_time:
            print(f'Раунд {each_round}: {time_per_round} хвилин')
        else:
            print(f'Раунд {each_round}: {time_per_round} хвилин (після коригування часу)')
        adjust_time()


training_session(3)
