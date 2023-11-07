import random

def title():
    print("-----Random Number Game -----")

def game():
    print("A dice will roll. You have 3 tries to guess what it will land on.")

    guessesRemaining = 3
    while guessesRemaining > 0:
        guess = input("What is your guess? ")
        roll = random.randint(1, 6)

        if int(guess) == roll:
            print("\t The dice rolled " + str(roll))
            print("\t You guessed " + guess)
            print("\t Congratulations! You Win!")
            break

        elif guess != roll:
            print("\t The dice rolled " + str(roll))
            print("\t Sorry, you guessed " + guess)
            guessesRemaining -= 1

            if guessesRemaining > 1:
                print("\t You have " + str(guessesRemaining) + " guesses left \n")

            if guessesRemaining == 1:
                print("\t You have " + str(guessesRemaining) + " guess left \n")

    if guessesRemaining == 0:
        print("\n Game Over! You Lose")


title()

active1 = True 
while active1 == True:
    game()
    active2 = True
    while active2 == True:
        choice = input("\n Do you want to play again? (yes/no): ")
        if choice == "yes":
            active2 = False
        elif choice == "no":
            print("Goodbye")
            active2 = False
            active1 = False
        else:
            print("That is not a valid input")