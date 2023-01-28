import gspread
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
                    # voter = None
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
                              "next time.\n")
                        print("Have a nice day.")
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
                # voter = None
            if voter in voter_id:
                print(f"Welcome voter ID number: {voter}\n")
                print("You are registered to Vote\n")
                voter_id.remove(voter)
                vote = (input(
                    "Would you like to vote for Teddy(1) or Syd(2):\n"))

                if not vote.isdigit():
                    print("Your vote is invalid/spoilt.")
                    print("Please make sure to vote correctly "
                          "in the future.\n")
                    print("Next Voter")
                    continue

                vote = int(vote)
                cell_values = [0, "None"]
                if vote == 1:
                    nominee_1_votes += 1
                    print("Thank you for your vote\n")
                    print("Have a nice day")
                    cell_values[0] = 1
                    cell_values[1] = nominee_1
                    sleep(5)
                    clear()
                    
                    clear()

                elif vote == 2:
                    nominee_2_votes += 1
                    print("Thank you for your vote\n")
                    print("Have a nice day")
                    cell_values[0] = 1
                    cell_values[1] = nominee_2
                    sleep(5)
                    clear()

                else:
                    print("Your vote is invalid/spoilt.")
                    print("Please make sure to vote correctly "
                          "in the future.\n")
                    print("Next Voter")
                    continue

                cell_list = SHEET.worksheet("Voters").range(f"E{voter+1}:F{voter+1}")
                for i, val in enumerate(cell_values):
                    cell_list[i].value = val 

                SHEET.worksheet("Voters").update_cells(cell_list)

            else:
                if voter is not None:
                    voter_exists = int(SHEET.worksheet("Voters").cell(voter+1, 5).value)
                    if voter_exists == 1:
                        print("Sorry you have already voted\n")
                        print("Next Voter")
                    else:
                        print("Sorry but your vote was counted "
                              "as invalid/spoilt.")
                        print("Please make sure to vote correctly "
                              "in the future.\n")
                        print("Next Voter")









def main():
    """
    Run all program functions
    """

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