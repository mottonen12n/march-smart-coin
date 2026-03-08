import random as r
import draw_bracket_tk as db
import tkinter as tk

def main_menu():
    #try:
        #loop = True
    picks = generatePicks()
    #teams = [f"A {i}" for i in range(1,17)] + [f"B {i}" for i in range(1,17)] + [f"C {i}" for i in range(1,17)] + [f"D {i}" for i in range(1,17)]
    teams = ["East1","East16","East8","East9","East5","East12","East4","East13","East6","East11","East3","East14","East7","East10","East2","East15","Widwest1","Widwest16","Widwest8","Widwest9","Widwest5","Widwest12","Widwest4","Widwest13","Widwest6","Widwest11","Widwest3","Widwest14","Widwest7","Widwest10","Widwest2","Widwest15","South1","South16","South8","South9","South5","South12","South4","South13","South6","South11","South3","South14","South7","South10","South2","South15","West1","West16","West8","West9","West5","West12","West4","West13","West6","West11","West3","West14","West7","West10","West2","West15"]
    winners = generateWinners(teams, picks)
    def showPicks():
        canvas.delete("all")
        canvas.create_text(10, 10, text="Here are the picks for this current session:\nEast Bracket Picks to Final Four: " + picks[0] +"\nMidwest Bracket Picks to Final Four: " + picks[1] + "\nSouth Bracket Picks to Final Four: " + picks[2] + "\nWest Bracket Picks to Final Four: " + picks[3] + "\nFinal Four Picks: " + picks[4], anchor="nw")
        return

    def showBracket():
        canvas.delete("all")
        canvas.create_text(10, 10, text="Bracket will open in new window.", anchor="nw")
        db.main(teams,winners)
        return

    root = tk.Tk()
    root.title("Smart Coin Bracket Menu")

    picksButton = tk.Button(root, text = "Show Picks", width = 30, command = showPicks, anchor="w")
    picksButton.pack()
    bracketButton = tk.Button(root, text = "Show Bracket", width = 30, command = showBracket, anchor="w")
    bracketButton.pack()
    exitButton = tk.Button(root, text="Exit", width=30, command=root.destroy, anchor="w")
    exitButton.pack()
    canvas = tk.Canvas(root, width=300, height=100)
    canvas.pack()


    root.mainloop()
"""while(loop):
            print("Make a selection:")
            selection = input("1: Show Bracket Picks\n2: Show Winners List\n3: Draw Bracket\n0: Exit\n")
            match selection:
                case "1":
                    print("Here are the picks for this current session, reload the application to reset picks:")
                    print("South Bracket Picks to Final Four: " + picks[0])
                    print("East Bracket Picks to Final Four: " + picks[1])
                    print("West Bracket Picks to Final Four: " + picks[2])
                    print("Midwest Bracket Picks to Final Four: " + picks[3])
                    print("Final Four Picks: " + picks[4])
                case "2":
                    print("Here is the Winners list based on the current picks:")
                    print(generateWinners(teams, picks))
                case "3": 
                    print("Bracket will open in new window. Close the window to continue here.")
                    db.main(teams, winners)
                case "0":
                    loop = False
                case _:
                    print("Invalid input, please try again.")"""
"""    except(Exception):
        #traceback.print_exc(file=sys.stdout)
        print("Error occured, try again.")"""

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

def generateWinners(teams, picks):
    winners = []
    for b in range(4):
        for i in range(8):
            match picks[b][i]:
                case "0": winners.append(teams[b*16+i*2])
                case "1": winners.append(teams[b*16+i*2+1])
    
    for b in range(4):
        for i in range(4):
            match picks[b][i + 8]:
                case "0": winners.append(winners[b*8+i*2])
                case "1": winners.append(winners[b*8+i*2+1])

    for b in range(4):
        for i in range(2):
            match picks[b][i + 12]:
                case "0": winners.append(winners[b*4+i*2+32])
                case "1": winners.append(winners[b*4+i*2+33])

    for b in range(4):
        match picks[b][14]:
            case "0": winners.append(winners[b*2+48])
            case "1": winners.append(winners[b*2+49])
    
    for i in range(2):
        match picks[4][i]:
            case "0": winners.append(winners[i*2+56])
            case "1": winners.append(winners[i*2+57])

    match picks[4][2]:
        case "0": winners.append(winners[60])
        case "1": winners.append(winners[61])

    return winners

main_menu()
#print(generateWinners([f"A {i}" for i in range(16)] + [f"B {i}" for i in range(16)] + [f"C {i}" for i in range(16)] + [f"D {i}" for i in range(16)],generatePicks()))