from lib import (
    add_record,
    read_credentials,
    authenticate,
    create_database,
    read_members_data,
    insert_members_data,
    display_menu,
    Query_the_records,
    delete_the_records,
    Modify_records1,
    Query_designated_mobile_phone,
)


def main():
    # Read user credentials
    credentials_file = "pass.json"
    credentials = read_credentials(credentials_file)
    if not credentials:
        return

    # Authenticate user
    username = input("請輸入帳號： ")
    password = input("請輸入密碼： ")
    if not authenticate(credentials, username, password):
        print("帳密錯誤，程式結束")
        return


    # Read member data from file
    members_data_file = "members.txt"
    members_data = read_members_data(members_data_file)

    if not members_data:
        return
    # Display menu
    while True:
        display_menu()
        choice = input("請輸入您的選擇 [0-7]: ")

        if choice == "0" or choice == "":
            break
        elif choice == "1":
            create_database()
        elif choice == "2":
            insert_members_data(members_data)
        elif choice == "3":
            Query_the_records()
        elif choice == "4":
            add_record()
        elif choice == "5":
            Modify_records1()
        elif choice == "6":
            Query_designated_mobile_phone()
        elif choice == "7":
            delete_the_records()
        else:
            print({"=>無效的選擇"})


if __name__ == "__main__":
    main()
