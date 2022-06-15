 # Jacob Rogers
# Login database console application
# 6-11-22

from ast import For
from os import system, unsetenv
from random import random
import sqlite3
import sys
from turtle import back
import pandas
import pyperclip
from colorama import init, Fore, Back, Style

conn = sqlite3.connect('logins.db')
cursor = conn.cursor()
init()

conn.execute('''
    CREATE TABLE IF NOT EXISTS logins (
        title VARCHAR(255) NOT NULL,
        email VARCHAR(255),
        userName VARCHAR(255),
        password VARCHAR(255) NOT NULL
    ); 
''')
# Function to list the matching values in the database.
def search(mode, noResults):

    if noResults:
        print(Back.RED,'\nThe previous search returned no results.\n',Back.BLACK,sep='')
    
    if mode != 1:
        print(Fore.YELLOW, 'Searching for the specific login...', Fore.WHITE,sep='') 

    print(Style.DIM,'\n(The search will return all entries that include your search term in its title)', Fore.RED, sep='')

    term = input('\nType in search term: ')
    print(Fore.WHITE,end='')
    if term == 'mm':
        return 'mm'
    if term == 'qu':
        return 'qu'

    # Check for a search that turns up empty.
    cursor.execute("SELECT COUNT(*) FROM logins WHERE title LIKE ?", ('%'+term+'%',))
    numRecords = cursor.fetchone()[0]
    if numRecords == 0:
        return 'no results'

    print(Fore.WHITE,end='')
    # Search for the term in titles from the table.
    query = cursor.execute("SELECT * FROM logins WHERE title LIKE ?", ('%'+term+'%',))

    system('cls')
    if mode == 1:
        print(Fore.LIGHTCYAN_EX, '---------------------------Search the database---------------------------', Fore.WHITE,sep='')
    elif mode == 3:
        print(Fore.LIGHTCYAN_EX, '---------------------------Edit a login in the database---------------------------', Fore.WHITE,sep='')
    elif mode == 4:
        print(Fore.LIGHTCYAN_EX, '---------------------------Remove a login from the database---------------------------', Fore.WHITE,sep='')
    
    print(Style.DIM,'\nThe logins are in the following format:',Style.NORMAL, sep='')
    print(Fore.LIGHTCYAN_EX, 'Id# (Title, Email, UserName, Password)',sep='')
    print(Fore.WHITE, '------------------Results-------------------',sep='')
    
    # Will print all query results with the term in the title.
    i = 0
    for r in query:
        print(i, r)
        i += 1

    # If there is only one search result.
    if i == 1:
        chosenId = 0
    # If there are multiple, let the user decide which one he wants.
    else:
        chosenId = -1
        while (int(chosenId) < 0 or int(chosenId) > numRecords - 1):
            print(Fore.RED,end='')
            chosenId = input('\nEnter the id number (leftmost number) of the term you want: ')
            if chosenId == 'mm' or chosenId == 'qu': break
            if not chosenId.isnumeric(): 
                chosenId = -1

            if (int(chosenId) < 0 or int(chosenId) > numRecords - 1):
                print(Fore.WHITE,Back.RED,'\nThe id number must be in the range of 0 to the number of logins displayed, and must be numeric.',Back.BLACK,sep='')

            print(Fore.WHITE,end='')

    if chosenId == 'mm': return 'mm'
    if chosenId == 'qu': return 'qu'

    # Get the exact record the user wants.
    sameQuery = cursor.execute("SELECT * FROM logins WHERE title LIKE ?", ('%'+term+'%',))

    system('cls')

    i = 0
    for record in sameQuery:
        if i == int(chosenId):
            print('--------------------------------------------------------------------------------')
            print('(',record[0],',',record[1],',',record[2],',',record[3],')')
            print('--------------------------------------------------------------------------------')
            return record
        i += 1

def checkEmpty() -> bool:
    cursor.execute("SELECT COUNT(*) FROM logins")
    numRecords = cursor.fetchone()[0]

    if numRecords == 0:
        return True
    else:
        return False

go = 'go'
first = True

while go != 'qu':

    system('cls')

    if first:
        print('A program to easily store your passwords and logins in a database on your computer \n -Jacob Rogers | 6-15-22')
        first = False

    print(Fore.YELLOW, '\n--------------------Login Logs--------------------\n', Fore.LIGHTCYAN_EX, sep='')
    print(Style.DIM, 'Choose an action, type the corresponding number, and press enter:\n',sep='')
    print(Fore.WHITE, Style.NORMAL, '0 -> View the entire database', sep='')
    print('1 -> Search for a login')
    print('2 -> Add a login to the database')
    print('3 -> Edit a login\'s information')
    print('4 -> Remove a login from the database')
    print('qu ->', Fore.LIGHTCYAN_EX, ' Quit & SAVE', Fore.WHITE, ' the program',sep='')
    print('mm -> Return to here, the main menu')
    print(Fore.RED,end='')
    action = input('Action: ')
    print(Fore.WHITE,end='')

    # View entire database.
    if action == '0':
        system('cls')

        if checkEmpty():
            print('Database is empty')

        else:
            print(Fore.LIGHTCYAN_EX, '---------------------------Login database fully displayed---------------------------',Fore.WHITE,sep='')
            print(Style.BRIGHT)
            print(pandas.read_sql_query('SELECT * FROM logins;', conn))
            print(Style.NORMAL,end='')

    # Search for a specific login in the database.
    elif action == '1':

        system('cls')

        if checkEmpty():
            print('Database is empty')
        
        else:
            # Run the search function.
            record = 'no results'
            noResults = False
            while record == 'no results':
                print(Fore.LIGHTCYAN_EX, '---------------------------Search the database---------------------------', Fore.WHITE,sep='')
                record = search(1, noResults)
                if record == 'mm' or record == 'qu': break
                if record == 'no results': 
                    noResults = True
                    system('cls')
                    
            
            if record == 'mm': continue
            elif record == 'qu': break

            clipboardChoice = ''
            print(' "e" -> Email \n "u" -> Username \n "p" -> Password \n "mm" -> Return to main menu \n')
            while clipboardChoice != 'mm':
                print(Fore.RED,end='')
                clipboardChoice = input('Choose what you want to copy to the clipboard: ')
                print(Fore.WHITE,end='')

                if clipboardChoice == 'e':
                    if not record[1]:
                        print('There was no email provided')
                    else:
                        print(Fore.GREEN, 'The email address, ', record[1], ', has been copied to your clipboard', Fore.WHITE, sep='')
                        pyperclip.copy(record[1])
                elif clipboardChoice == 'u':
                    if not record[2]:
                        print('There was no username provided')
                    else:
                        print(Fore.GREEN,'The username, ', record[2], ', has been copied to your clipboard',Fore.WHITE, sep='')
                        pyperclip.copy(record[2])
                elif clipboardChoice == 'p':
                    print(Fore.GREEN,'The password, ', record[3], ', has been copied to your clipboard',Fore.WHITE, sep='')
                    pyperclip.copy(record[3])
                else:
                    continue

            if clipboardChoice == 'mm': continue


    # Add a new entry to the database.
    elif action == '2':
        title, email, username, password = None, None, None, None
        system('cls')

        print(Fore.LIGHTCYAN_EX, '---------------------------Add a new login to the database---------------------------', Fore.WHITE,sep='')

        print(Style.DIM, '\nEnter the information about your login, then press enter:\n',Fore.RED, sep='')

        while not title: 
            title = input('Title: ')
            
            if not title: print(Fore.WHITE,Back.RED,'Entering a title is required.',Back.BLACK, Fore.RED,sep='')
            
            if title == 'mm' or title == 'qu': break
        
        if title == 'mm': continue
        elif title == 'qu': break
        
        while not email and not username:
            email = input('(Optional) Email: ')
            if email == 'mm' or email == 'qu': break

            username = input('(Optional) Username: ')
            if username == 'mm' or username == 'qu': break
            if not email and not username:
                print(Fore.WHITE, Back.RED, 'At least one of either username or email is required.', Fore.RED, Back.BLACK,sep='')

        if email == 'mm' or username == 'mm': continue
        if email == 'qu' or username == 'qu': break

        while not password:
            password = input('Password: ')
            if password == 'mm' or password == 'qu': break

            if not password:
                print(Fore.WHITE, Back.RED,'Entering a password is required.', Back.BLACK,sep='')

        if password == 'mm': continue
        elif password == 'qu': break

        
        conn.execute('INSERT INTO logins (title, email, username, password) \
        VALUES(?, ?, ?, ?);', (title, email, username, password))
        

        print(Fore.GREEN,'\nLogin inserted entry into the database.',Fore.WHITE,sep='')

    # Edit a login.
    elif action == '3':
        system('cls')

        if checkEmpty():
            print('Database is empty.')
        
        else:            
           # Run the search function.
            record = 'no results'
            noResults = False
            while record == 'no results':
                print(Fore.LIGHTCYAN_EX, '---------------------------Edit a login from the database---------------------------', Fore.WHITE,sep='')
                record = search(3, noResults)
                if record == 'mm' or record == 'qu': break
                if record == 'no results': 
                    noResults = True
                    system('cls')
            
            if record == 'mm': continue
            if record == 'qu': break

            editChoice = ''
            print(Fore.WHITE,'"t" -> Title \n "e" -> Email \n "u" -> Username \n "p" -> Password \n any other key -> Return to main menu \n',sep='')
            
            print(Fore.RED,end='')
            editChoice = input('Choose what you want you want to edit: ')

            if editChoice == 't':
                title = input("Enter new title: ")
                conn.execute("UPDATE logins SET title = ? WHERE title = ? AND email = ? AND userName = ? AND password = ?", 
                (title, record[0], record[1], record[2], record[3]))
                    
            elif editChoice == 'e':
                email = input("Enter new email: ")
                conn.execute("UPDATE logins SET email = ? WHERE title = ? AND email = ? AND userName = ? AND password = ?", 
                (email, record[0], record[1], record[2], record[3]))
                    
            elif editChoice == 'u':
                username = input("Enter new username: ")
                conn.execute("UPDATE logins SET userName = ? WHERE title = ? AND email = ? AND userName = ? AND password = ?", 
                (username, record[0], record[1], record[2], record[3]))
                    
            elif editChoice == 'p':
                password = input("Enter new password: ")
                conn.execute("UPDATE logins SET password = ? WHERE title = ? AND email = ? AND userName = ? AND password = ?", 
                (password, record[0], record[1], record[2], record[3]))
                    
            else:
                continue

            print(Fore.GREEN, 'Login updated with new information.', Fore.WHITE, sep='')

    # Remove a login.
    elif action == '4':
        system('cls')

        if checkEmpty():
            print('Database is empty.')
        
        else:            
            # Run the search function.
            record = 'no results'
            noResults = False
            while record == 'no results':
                print(Fore.LIGHTCYAN_EX, '---------------------------Remove a login from the database---------------------------', Fore.WHITE,sep='')
                record = search(4, noResults)
                if record == 'mm' or record == 'qu': break
                if record == 'no results': 
                    noResults = True
                    system('cls')
            
            if record == 'mm': continue
            if record == 'qu': break

            
            conn.execute('DELETE FROM logins WHERE title = ? AND email = ? AND userName = ? AND password = ?',(record[0],record[1],record[2],record[3]))
            

            print(Fore.GREEN,'Login deleted from the database.',Fore.WHITE, sep='')

    # Quit program.
    elif action == 'qu':
        break

    print(Fore.RED,end='')
    go = input('\nPress any key to continue: ')
    print(Fore.WHITE,end='')
    
system('cls')
conn.commit()
cursor.close()
conn.close()