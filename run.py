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









def main():
    """
    Run all program functions
    """

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