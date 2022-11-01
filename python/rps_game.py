import random

def myFunction():
    player_choice = input("Enter a value")
    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)
    print(f"Choices: Player= {player_choice} ; Computer = {computer_choice}")
    if player_choice == computer_choice:
        return "Draw"
    elif player_choice == "rock" and computer_choice == "scissors":
        return "Player Won"
    elif player_choice == "rockpaper" and computer_choice == "rock":
        return "Player Won"
    elif player_choice == "scissors" and computer_choice == "rock":
        return "Player Won"
    else:
        return "Computer Won"

print(myFunction())