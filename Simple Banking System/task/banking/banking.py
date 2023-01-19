# new branch
# Write your code here
from random import randint
import sqlite3

sqlcon = sqlite3.connect('card.s3db')
sql_cur = sqlcon.cursor()

class Bank:
    accounts_count = 0
    clientsdb = {}
    iin_const = "400000"

    def __init__(self, bankname):
        self.bankname = bankname


    def createclientcard(self):

        gencardnum = randint(1, 999999999)
        zero_count = 9 - len(str(gencardnum))
        new_clientcard = self.iin_const + ("0" * zero_count) + str(gencardnum)
        newcard_checksum = self.genchecksum(new_clientcard)
        # print(new_clientcard, newcard_checksum)

        if newcard_checksum > - 1:
            new_clientcard += str(newcard_checksum)
        else:
            raise ValueError('The card and checksum dont match', newcard_checksum)

        rnd_pin = randint(1111, 9999)
        new_pin = "0" * (4 - len(str(rnd_pin))) + str(rnd_pin)
        return new_clientcard, new_pin

    def createaccount(self, name="", surname="", city=""):
        # self.clientname = name
        # self.clientsurname = surname
        # self.clientcity = city
        self.clientcardnumber = ""
        self.clientcardpin = ""
        self.clientcardnumber, self.clientcardpin = self.createclientcard()
        self.clientbalance = 0

        self.clientsdb[self.clientcardnumber] = [name, surname, city,
                                                 self.clientcardpin, self.clientbalance]

        sql_cur.execute('INSERT INTO account_list (id, number, pin, balance) VALUES (1, "123456789", "9991", 0)')

        self.accounts_count = len(self.clientsdb)

    def accountdump(self):
        print(f"List of all({len(self.clientsdb)}) accounts for bank: " + self.bankname)
        # print(self.clientsdb)
        for key, item in self.clientsdb.items():
            print(key, item)

    def checkpin(self, cardnum: str, cardpin: str):
        if int(cardnum) >= 4000000000000000 and cardnum in self.clientsdb.keys():
            if self.clientsdb[cardnum][3] == cardpin:
                return True
        return False

    def checkbalance(self, cardnum: str):
        return self.clientsdb[cardnum][4]

    def genchecksum(self, cardnum: str):
        cardsum = 0

        for num, elem in enumerate(cardnum):
            digit = int(elem)
            if (num + 1) % 2:
                digit = digit * 2
                if digit > 9:
                    digit -= 9
            cardsum += digit

        if cardsum % 10 == 0:
            return 0
        else:
            checksum = 10 - (cardsum % 10)
            if 0 <= checksum <= 9:
                return checksum

        return -1


def user_interface():
    user_logged = False
    user_card = ""

    # Main cycle
    while True:

        # Show menu
        if user_logged:
            print("1. Balance")
            print("2. Log out")
        else:
            print("1. Create an account")
            print("2. Log into account")
        print("0. Exit")

        # read user choice
        try:
            user_choice = int(input())
        except ValueError:
            print("Please write correct number")
            user_choice = int(input())

        print()

        # process user choice
        # create user bank account
        if user_choice == 1 and not user_logged:
            Tink.createaccount()
            cardnum = Tink.clientcardnumber
            cardpin = Tink.clientcardpin

            print("Your card has been created")
            print("Your card number:")
            print(cardnum)
            print("Your card PIN:")
            print(cardpin)

        # login in to existing bank account
        elif user_choice == 2 and not user_logged:

            print("Enter your card number:")
            user_inputcard = str(input())
            print("Enter your PIN:")
            user_inputpin = str(input())

            if Tink.checkpin(user_inputcard, user_inputpin):
                user_logged = 1
                user_card = user_inputcard
                print("You have successfully logged in!")
            else:
                print("Wrong card number or PIN!")
                user_logged = 0

        # exit from bank system
        elif user_choice == 0:
            print("Bye!")
            break

        # dump bank BD
        elif user_choice == 9:
            Tink.accountdump()

        # This user choices valid only if user LOG IN
        # logout user from bank system
        elif user_choice == 2 and user_logged:
            user_logged = False

        # print balance to user
        elif user_choice == 1 and user_logged:
            print("Balance:", Tink.checkbalance(user_card))

        print()



Tink = Bank("Tinkow")
user_interface()

# cur.execute("INSERT INTO ")
# sql_cur.execute("CREATE TABLE account_list (id int, number TEXT, pin TEXT, balance TEXT);")
sqlcon.close()