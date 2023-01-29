import sqlite3
from random import randint


class Bank:
    accounts_count = 0
    # clientsdb = {}
    sqlcon = 0
    sqlcur = 0
    iin_const = '400000'

    def __init__(self, bankname):
        self.bankname = bankname
        self.sqlcon = sqlite3.connect('card.s3db')
        self.sqlcur = self.sqlcon.cursor()
        self.sqlcur.execute('CREATE TABLE IF NOT EXISTS card ('
                            'id integer PRIMARY KEY,'
                            ' number TEXT, '
                            'pin TEXT, '
                            'balance integer DEFAULT 0);'
                            '')
        self.sqlcon.commit()

    def createclientcard(self):

        gencardnum = randint(1, 999999999)
        zero_count = 9 - len(str(gencardnum))
        new_clientcard = self.iin_const + ('0' * zero_count) + str(gencardnum)
        newcard_checksum = self.genchecksum(new_clientcard)

        if newcard_checksum > - 1:
            new_clientcard += str(newcard_checksum)
        else:
            raise ValueError('The card and checksum dont match',
                             newcard_checksum)

        rnd_pin = randint(1111, 9999)
        new_pin = '0' * (4 - len(str(rnd_pin))) + str(rnd_pin)
        return new_clientcard, new_pin

    def createaccount(self, name='', surname='', city=''):
        self.clientcardnumber = ''
        self.clientcardpin = ''
        self.clientcardnumber, self.clientcardpin = self.createclientcard()
        self.clientbalance = 0

        sql_query = f"INSERT INTO card (number, pin, balance) VALUES ('{self.clientcardnumber}', '{self.clientcardpin}', 0)"
        self.sqlcur.execute(sql_query)
        self.sqlcon.commit()

        sql_query = "SELECT COUNT(id) FROM card;"
        self.sqlcur.execute(sql_query)
        self.accounts_count = self.sqlcur.fetchone()[0]
        # logme(fp, ("Account count is:"+str(self.accounts_count)))
    def accountdump(self):
        print(f'List of all({self.accounts_count}) accounts for bank: ' + self.bankname)
        sql_query = "SELECT * FROM card"
        self.sqlcur.execute(sql_query)
        for row in self.sqlcur.fetchall():
            print(row)

    def bankclear(self):
        sql_query = "DELETE FROM card"
        self.sqlcur.execute(sql_query)
        print("All cards deleted")


    def checkpin(self, cardnum: str, cardpin: str):
        sql_query = f"SELECT * FROM card WHERE number={cardnum} and pin={cardpin};"
        self.sqlcur.execute(sql_query)
        result = self.sqlcur.fetchone()
        # print(result, "CHECK PIN")
        if result != None:
            return True
        return False

    def checkbalance(self, cardnum: str):
        sql_query = f"SELECT * FROM card WHERE number={cardnum};"
        self.sqlcur.execute(sql_query)
        return self.sqlcur.fetchone()[3]


    def addbalance(self, cardnum: str, moneysum: int):
        sql_query = f"SELECT * FROM card WHERE number={cardnum};"
        self.sqlcur.execute(sql_query)
        money_count = int(self.sqlcur.fetchone()[3] + moneysum)
        # print(money_count, moneysum)
        sql_query = f"UPDATE card SET balance = {money_count} WHERE number = '{cardnum}';"
        # print(sql_query)
        self.sqlcur.execute(sql_query)
        self.sqlcon.commit()



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


def logme(fp, log_data):
    fp.write(log_data+"\n")

def user_interface():
    user_logged = False
    user_card = ''

    # Main cycle
    while True:

        # Show menu
        if user_logged:
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
        else:
            print('1. Create an account')
            print('2. Log into account')
        print('0. Exit')

        # read user choice
        try:
            user_choice = int(input())
        except ValueError:
            print('Please write correct number')
            user_choice = int(input())

        print()

        # process user choice
        # create user bank account
        if user_choice == 1 and not user_logged:
            Tink.createaccount()
            cardnum = Tink.clientcardnumber
            cardpin = Tink.clientcardpin

            print('Your card has been created')
            print('Your card number:')
            print(cardnum)
            print('Your card PIN:')
            print(cardpin)

        # login in to existing bank account
        elif user_choice == 2 and not user_logged:

            print('Enter your card number:')
            user_inputcard = str(input())
            print('Enter your PIN:')
            user_inputpin = str(input())

            if Tink.checkpin(user_inputcard, user_inputpin):
                user_logged = 1
                user_card = user_inputcard
                print('You have successfully logged in!')
            else:
                print('Wrong card number or PIN!')
                user_logged = 0

        # exit from bank system
        elif user_choice == 0:
            print('Bye!')
            Tink.sqlcon.close()

            break

        # dump bank BD
        elif user_choice == 9:
            Tink.accountdump()

        # clear bank BD
        elif user_choice == 8:
            Tink.bankclear()
            Tink.accountdump()

        # This user choices valid only if user LOG IN
        # logout user from bank system
        elif user_choice == 5 and user_logged:
            user_logged = False

        # print balance to user
        elif user_choice == 1 and user_logged:
            print('Balance:', Tink.checkbalance(user_card))

        # add money to balance
        elif user_choice == 2 and user_logged:
            print('Enter income:')
            try:
                money_count = int(input())
                Tink.addbalance(user_card, money_count)
                print("Income was added!")
            except:
                print("Error wrong money value")

        # print balance to user
        elif user_choice == 3 and user_logged:
            print('Transfer:')
            print('Enter card number:')
            # try:
            card_num = input()
            # logme(fp, (card_num, card_num[-1:]))

            sql_query = f"SELECT count(id) FROM card WHERE number={card_num};"
            Tink.sqlcur.execute(sql_query)
            card_count = Tink.sqlcur.fetchone()[0]
            if card_count == 1 and card_num != user_card:
                print("Enter how much money you want to transfer:")
                money_count = int(input())
                if money_count <= Tink.checkbalance(user_card):
                    # print(money_count)
                    Tink.addbalance(card_num, money_count)
                    Tink.addbalance(user_card, money_count * -1)
                    print("Success!")
                else:
                    print("Not enough money!")
            elif str(Tink.genchecksum(card_num[:-1])) != card_num[-1:]:
                print("Probably you made a mistake in the card number. Please try again!")
            elif card_num == user_card:
                print("You can't transfer money to the same account!")
            else:
                print("Such a card does not exist.")

        elif user_choice == 4 and user_logged:
            sql_query = f"DELETE FROM card WHERE number = '{user_card}';"
            Tink.sqlcur.execute(sql_query)
            Tink.sqlcon.commit()
            print("The account has been closed!")
        print()



Tink = Bank('Tinkow')
with open("log.txt", "a") as fp:
    user_interface()

# cur.execute('INSERT INTO ')
# sqlcon.close()
