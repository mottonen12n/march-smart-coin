import random as r
import traceback
import sys

def main_menu():
    loop = True
    try:
        while(loop):
            print("Make a selection:")
            selection = input("1: Generate Bracket Picks\n0: Exit\n")
            match selection:
                case "1":
                    picks = generatePicks()
                    print("South Bracket Picks to Final Four: " + picks[0])
                    print("East Bracket Picks to Final Four: " + picks[1])
                    print("West Bracket Picks to Final Four: " + picks[2])
                    print("Midwest Bracket Picks to Final Four: " + picks[3])
                    print("Final Four Picks: " + picks[4])
                case "0":
                    loop = False
                case _:
                    print("Invalid input, please try again.")
    except(Exception):
        #traceback.print_exc(file=sys.stdout)
        print("Error occured, try again.")

def generatePicks():
    result = []
    
    #Each division bracket up to Final Four
    result.append(generateDivisionToFinalFour())
    result.append(generateDivisionToFinalFour())
    result.append(generateDivisionToFinalFour())
    result.append(generateDivisionToFinalFour())
    #Final Four
    result.append(onein2()+onein2()+onein2())
    return result

def generateDivisionToFinalFour():
    result = ""
    #First Round
    #1-16
    result += onein16()
    #8-9
    result += onein2()
    #5-12
    result += onein2()
    #4-13
    result += onein4()
    #6-11
    result += onein2()
    #3-14
    result += onein4()
    #7-10
    result += onein2()
    #2-15
    result += onein8()

    #Second Round to Elite Eight
    #1/16 vs. 8/9
    if(result[0] == "0"):
        result += onein4()
    else:
        result += onein2()

    #Rest of Round 2
    result += onein2()
    result += onein2()
    result += onein2()
    #Sweet Sixteen
    result += onein2()
    result += onein2()
    #Elite Eight
    result += onein2()

    return result

def onein2():
    return str(r.randint(0,1))

def onein4():
    if(r.randint(1,4) == 1):
        return "1"
    else:
        return "0"
    
def onein8():
    if(r.randint(1,8) == 1):
        return "1"
    else:
        return "0"
    
def onein16():
    if(r.randint(1,16) == 1):
        return "1"
    else:
        return "0"

main_menu()