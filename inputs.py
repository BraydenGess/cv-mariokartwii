def user_input():
    try:
        player = input()
        print(player)
    except ValueError:
        return None