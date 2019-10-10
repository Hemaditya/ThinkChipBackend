import session
from widgets import ENG
import sys
user_path = None
widget_path = None

while True:
    print(f" MAIN MENU ")
    print("1. Create User")
    print("2. Login")
    print("3. Delete User")
    print("4. quit")

    inp = int(input("Enter your choice: "))

    if(inp == 1):
        """
            Create a user.
        """
        inp = input("Enter user name: ")
        user_path = session.create_user(inp)

    elif(inp == 2):
        """
            Get the username and login
        """
        user = input('Enter username: ')
        user_path = session.check_user(user)
        if(user_path == 0):
            continue

        while True:
            print("Select Widgets")
            print("1. ENG ")
            print("2. Go back to main menu")
            print("3. Exit")

            inp = int(input("Enter your choice: "))
            
            if(inp == 1):
                """
                    Start the ENG Widget
                """
                widget_path = session.check_widget(user_path,'eng')
                if(widget_path == 0):
                    widget_path = session.add_widget('raghav','eng')

                inp = int(input("Enter number of trails: "))
                if(inp %10 != 0):
                    print("The number of trails should be in the count of 10")
                    continue
                eng = ENG(widget_path,inp)
                eng.run()

            elif(inp == 2):
                break

            elif(inp == 3):
                print("Exiting from the programm")
                sys.exit()

    elif inp == 3:
        inp = input("Enter the name of the user whose data you want to delete: ") 
        session.delete_user(inp)

    elif inp == 4:
        print("Exiting from the programm")
        sys.exit()

