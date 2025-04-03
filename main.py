#import random as r

def main_menu():
    loop = True
    try:
        while(loop):
            print("Make a selection:")
            selection = input("1: Generate Bracket Picks\n0: Exit\n")
            match selection:
                case "1":
                    generatePicks()
                case "0":
                    loop = False
                case _:
                    print("Invalid input, please try again.")
    except(Exception):
        print("Error occured, try again.")

def generatePicks():
    print("picks")

main_menu()