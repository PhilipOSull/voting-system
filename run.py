import gspread
from time import sleep
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('voting_system')

def clear():
    """
    This clears the screen/terminal
    """

    print('\033c')

def reset():
    """
    This resets the vote column to 0
    It resets the nominee column to "None"
    """

    wst_data_len = len(SHEET.worksheet("Voters").col_values(1)[1:])
    cell_list = SHEET.worksheet("Voters").range(f"E2:E{wst_data_len+1}")
    cell_values = [0]*wst_data_len

    for i, val in enumerate(cell_values):
        cell_list[i].value = val
    
    SHEET.worksheet("Voters").update_cells(cell_list)

    cell_list = SHEET.worksheet("Voters").range(f"F2:F{wst_data_len+1}")
    cell_values = ["None"]*wst_data_len

    for i, val in enumerate(cell_values):
        cell_list[i].value = val

    SHEET.worksheet("Voters").update_cells(cell_list)

def validate_pps(pps):
    """
    This makes sure the PPS number entered is valid
    If the PPS number is not 8 characters, it will return False
    If the first 7 characters are not numbers, it will return False
    If the last character is not a letter, it will return False
    Otherwise it will return True
    """

    if len(pps) != 8:
        return False
    pps_numbers = pps[:7]
    for item in pps_numbers:
        if not item.isdigit():
            return False
    pps_chars = pps[-1]
    if not pps_chars[0].isalpha():
        return False
    return True

def voting(nominee_1, nominee_2, voter_id):
    """
    Voter enters their PPS number, if the PPS number is on the worksheet
    then they are registered and can vote.
    If the PPS number format is valid but not on the worksheet then they are 
    not registered and cannot vote.
    If the PPS number format is invalid, they will be prompted if they
    would like to try again.
    If the vote is valid, the the spreadsheet will be updated to show they have
    voted and which nominee they have voted for.
    """
   
    nominee_1_votes, nominee_2_votes = 0, 0
    while True:
        if voter_id == []:
            total_votes = nominee_1_votes + nominee_2_votes
            print("Voting is now closed\n")
            if nominee_1_votes >= nominee_2_votes:
                percent = round(
                    (nominee_1_votes / total_votes) * 100,
                    2
                )
                if percent == 50:
                    print("The election was a draw\n")
                else:
                    print(f"{nominee_1} wins, with {percent}% of the votes")
                break
            elif nominee_2_votes > nominee_1_votes:
                percent = round(
                    (nominee_2_votes / total_votes) * 100,
                    2
                )
                print(f"{nominee_2} wins, with {percent}% of the votes")
                break
        else:
            voter = None
            pps = input(
                "Please enter your PPS number to vote:\n").strip().upper()
            pps_correct = validate_pps(pps)
            if pps_correct:
                pps_exists = SHEET.worksheet("Voters").find(pps)
                if pps_exists:
                    voter = pps_exists.row-1
                else:
                    print(f"The PPS you entered is {pps}, sorry that PPS "
                          "is not registered to vote.\n")
                    try_again = input(
                        "Would you like to try again? Y/N\n").lower()
                    while True:
                        if try_again == "y":
                            print("Double check it is entered correctly...\n")
                            break
                        if try_again == "n":
                            print("Goodbye, thanks and make sure to register "
                                  "before the next election.\n")
                            sleep(5)
                            clear()
                            break
                        elif try_again != "y" or "n":
                            print("Sorry that answer is invalid...")
                            print("Goodbye.\n")
                            print("Have a nice day.")
                            sleep(5)
                            clear()
                            break
            else:
                print(f"The PPS you entered is {pps}, "
                      "sorry that format is incorrect.")
                print("Your PPS number should be 7 numbers followed by a "
                      "letter, Example: 1234567T\n")
                try_again = input("Would you like to try again? Y/N\n").lower()
                while True:
                    if try_again == "y":
                        print("Double check the format is correct "
                              "this time...\n")
                        break
                    if try_again == "n":
                        print("Goodbye, please use a valid PPS number "
                              "next time...\n")
                        print("Have a nice day.")
                        sleep(5)
                        clear()
                        break
                    elif try_again != "y" or "n":
                        print("Sorry but that answer is invalid...")
                        print("Goodbye.\n")
                        print("Have a nice day.")
                        sleep(5)
                        clear()
                        break
            if voter in voter_id:
                print(f"Welcome voter ID number: {voter}\n")
                print("You are registered to Vote\n")
                voter_id.remove(voter)
                vote = (input(
                    "Would you like to vote for Teddy(1) or Syd(2):\n"))

                if not vote.isdigit():
                    print("Sorry but your vote is invalid/spoilt...")
                    print("Please make sure to vote correctly "
                          "in the future.\n")
                    sleep(5)
                    clear()
                    continue
                vote = int(vote)
                cell_values = [0, "None"]
                if vote == 1:
                    nominee_1_votes += 1
                    print("Thank you for your vote.\n")
                    print("Have a nice day.")
                    cell_values[0] = 1
                    cell_values[1] = nominee_1
                    sleep(5)
                    clear()
                elif vote == 2:
                    nominee_2_votes += 1
                    print("Thank you for your vote.\n")
                    print("Have a nice day.")
                    cell_values[0] = 1
                    cell_values[1] = nominee_2
                    sleep(5)
                    clear()
                else:
                    print("Sorry but your vote is invalid/spoilt...")
                    print("Please make sure to vote correctly "
                          "in the future.\n")
                    sleep(5)
                    clear()
                    continue
                cell_list = SHEET.worksheet("Voters").range(f"E{voter+1}:F{voter+1}")
                for i, val in enumerate(cell_values):
                    cell_list[i].value = val
                SHEET.worksheet("Voters").update_cells(cell_list)
            else:
                if voter is not None:
                    voter_exists = int(SHEET.worksheet("Voters").cell(voter+1, 5).value)
                    if voter_exists == 1:
                        print("Sorry but you have already voted...\n")
                        print("Thanks and have a nice day.")
                        sleep(5)
                        clear()
                    else:
                        print("Sorry but your vote was counted "
                              "as invalid/spoilt...")
                        print("Please make sure to vote correctly "
                              "in the future.\n")
                        sleep(5)
                        clear()

def main():
    """
    Run all program functions
    """

    reset()
    clear()
    print("-----------------------")
    print("-----------------------\n")
    print("Welcome to the Election\n")
    print("-----------------------")
    print("-----------------------\n")
    nominee_1, nominee_2 = SHEET.worksheet("Nominees").col_values(1)[1:]
    voter_id = SHEET.worksheet("Voters").col_values(1)[1:]
    voter_id = [int(num) for num in voter_id]
    voting(nominee_1, nominee_2, voter_id)


main()