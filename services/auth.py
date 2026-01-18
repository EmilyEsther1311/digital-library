from classes.user import LibraryUser

def log_in(users):
    print("\nLog in")
    while True:
        username = input("Enter username: ")
        #Correct username entered at log in
        if username in users:
            return try_password(users, users[username])
        #Incorrect username entered at log in
        else:
            print(f"Incorrect username")
            while True:
                try:
                    choice = int(input("1. Try different username \n2. Create account \nEnter choice: "))
                except ValueError:
                    print("Invalid choice (must be the number 1 or 2)")
                    continue
                #Go back to the beginning of the outer while true loop (re-start log in)
                if choice == 1:
                    break
                #Go to sign up
                elif choice == 2:
                    return sign_up(users)
                else:
                    print("Invalid choice (must be the number 1 or 2)")
                    continue

def try_password(users, user):
    while True:
        password = input("Enter password: ")
        #Correct password entered
        if password == user.password:
            print(f"\nWelcome {user.username}!")
            return user
        #Incorrect password entered
        else:
            print("\nIncorrect password")
            while True:
                try:
                    choice = int(input("1. Try different password \n2. Re-set password \nEnter choice: "))
                except ValueError:
                    print("Invalid choice (must be the number 1 or 2)")
                    continue
                #Re-try entering password
                if choice == 1:
                    break
                #Re-set password
                elif choice == 2:
                    set_password(user)
                    return log_in(users)
                else:
                    print("Invalid choice (must be the number 1 or 2)")
                    continue

def sign_up(users):
    print("\nSign Up")
    new_user_bool = set_username(users)
    if new_user_bool:
        print("\nAccount successfully created")
    return log_in(users)


#The following function returns True if a new user is created and False otherwise
def set_username(users):
    while True:
        new_username = input("Enter username: ")
        if len(new_username) == 0:
            continue
        else:
            repeat = False
            #Check if the entered username is already assigned to an existing user
            for username in users:
                if new_username == username:
                    repeat = True
                    break
            #Case where username is already assigned to an existing user
            if repeat:
                print(f"An account already exists with username {new_username}")
                while True:
                    try:
                        choice = int(input("\n1. Choose a different username \n2. Log in to the account with this username \nEnter choice: "))
                    except ValueError:
                        print("Invalid choice (must be the number 1 or 2)")
                        continue
                    #Re-start set_username(users)
                    if choice == 1:
                        break
                    #Log in instead of sign up
                    elif choice == 2:
                        return False
                    else:
                        print("Invalid choice (must be the number 1 or 2)")
                        continue
            #Case where a new username is entered, and hence, new account needs to be created
            else:
                #Create new user with new username (and no password)
                users[new_username] = LibraryUser(new_username, "")
                print("Valid username")
                #Set password for new user
                set_password(users[new_username])
                return True

def set_password(user):
    while True:
        print("\nPasswords must be at least 8 characters long and contain a capital letter")
        new_password = input("Enter password: ")

        #Password validation check
        if len(new_password) < 8 or new_password.lower() == new_password:
            print("Password does not meet requirements")
            continue

        # Confirm password (3 attempts)
        for i in range(3):
            confirm_password = input("Confirm password: ")
            if confirm_password == new_password:
                user.password = new_password
                print("Password has been set successfully")
                return

        #Failed confirmation
        print("Too many failed confirmation attempts. Please re-enter a new password")