import json
import sqlite3


def read_credentials(credentials_file: str) -> dict:
    """
    從 JSON 檔案讀取使用者憑證。

     參數：
         file_path (str)：包含憑證的 JSON 檔案的路徑。

     返回：
         dict：使用者憑證作為字典。
    """
    try:
        with open(credentials_file, "r", encoding="UTF-8") as file:
            credentials = json.load(file)
        return credentials
    except FileNotFoundError:
        print(f"Error: File not found - {credentials_file}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file - {credentials_file}")
        return None


def authenticate(
    credentials: dict,
    username: str,
    password: str,
) -> bool:
    """
    驗證用戶憑證。

    參數：
        憑證（dict）：包含使用者名稱和密碼的字典。
        username (str)：使用者輸入的使用者名稱。
        密碼（str）：使用者輸入的密碼。

    返回：
        bool：如果驗證成功，則為 True，否則為 False。
    """
    for credentials_list in credentials:
        if "帳號" in credentials_list and "密碼" in credentials_list:
            if (
                username == credentials_list["帳號"]
                and password == credentials_list["密碼"]
            ):
                return True


def create_database():
    """
    建立 SQLite 資料庫和成員表。 1
    """
    conn = sqlite3.connect("wanghong.db")
    cursor = conn.cursor()

    # Create members table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS members (
            iid INTEGER PRIMARY KEY AUTOINCREMENT,
            mname TEXT NOT NULL,
            msex TEXT NOT NULL,
            mphone TEXT NOT NULL
        )
    """
    )
    print("=>資料庫已建立")

    conn.commit()
    conn.close()


def read_members_data(file_path: str) -> list:
    """
    從文字檔案中讀取成員資料。

         參數：
             file_path (str)：包含成員資料的文字檔案的路徑。

         返回：
             list：作為元組的成員資料列表。
    """
    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            lines = file.readlines()

        # Process lines and create a list of tuples
        member_data = [tuple(line.strip().split(",")) for line in lines]

        return member_data
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None


def insert_members_data(member_data: list):
    """
    將成員資料插入成員表中。 2

     參數：
         member_data（列表）：作為元組的成員資料列表。
    """

    conn = sqlite3.connect("wanghong.db")
    cursor = conn.cursor()

    # Insert data into members table
    cursor.executemany(
        """
        INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)
    """,
        member_data,
    )
    print(f"=>異動 {cursor.rowcount} 筆記錄")

    conn.commit()
    conn.close()


def Query_the_records():
    """
    顯示所有紀錄 3
    """
    conn = sqlite3.connect("wanghong.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    data = cursor.fetchall()
    if len(data) > 0:
        print("姓名\t\t性別\t手機")
        print("-" * 29)
        for record in data:
            print(f"{record[1]}\t\t{record[2]}\t{record[3]}")
    else:
        print("=>查無資料")
    cursor.close()
    conn.close()


def add_record():
    """
    將新記錄加入members表中。 4
    """
    conn = sqlite3.connect("wanghong.db")
    cursor = conn.cursor()

    vid = input("請輸入姓名: ")
    name = input("請輸入性別 : ")
    age = input("請輸入手機: ")
    age = int(age)  # 將輸入的字串進行轉型

    # 安全的佔位符號寫法
    data = (vid, name, age)
    cursor.execute("INSERT INTO members (mname, msex , mphone) VALUES (?, ?, ?)", data)
    print(f"=>異動 {cursor.rowcount} 筆記錄")
    conn.commit()

    cursor.close()
    conn.close()


def Modify_records1():
    """
    修改紀錄 5
    """
    conn = sqlite3.connect("wanghong.db")
    cursor = conn.cursor()

    vid = input("請輸入想修改記錄的姓名:")
    if len(vid) > 0:
        cursor.execute("SELECT * FROM members WHERE mname = ?", (vid,))
        data = cursor.fetchall()
        # ---------------------------------------------------------------------------------------------------------
        name = input("請輸入要改變的性別: ")
        age = input("請輸入要改變的手機:")
        cursor.execute(
            "UPDATE members SET msex=? ,mphone=? WHERE mname=?;", (name, age, vid)
        )
        if len(data) > 0:
            for record in data:
                print("原資料：")
                print(f"姓名：{record[1]}, 性別{record[2]}, 電話：{record[3]}")
                print(f"=>異動 {cursor.rowcount} 筆記錄")
        cursor.execute("SELECT * FROM members WHERE mname = ?", (vid,))
        data = cursor.fetchall()
        for record in data:
            print("修改後資料：")
            print(f"姓名：{record[1]}, 性別{record[2]}, 電話：{record[3]}")
    else:
        print("=>必須指定姓名才可修改記錄")

    conn.commit()
    cursor.close()
    conn.close()


def Query_designated_mobile_phone():
    """
    查詢指定手機 6
    """
    conn = sqlite3.connect("wanghong.db")
    cursor = conn.cursor()

    phone = input("請輸入手機: ")

    try:
        cursor.execute("SELECT * FROM members WHERE mphone = ?", (phone,))
        data = cursor.fetchall()
    except sqlite3.Error as error:
        print(f"執行 SELECT 操作時發生錯誤：{error}")
    if len(data) > 0:
        print("姓名\t\t性別\t手機")
        print("-" * 29)
        for record in data:
            print(f"{record[1]}\t\t,{record[2]}\t,{record[3]}")
    else:
        print("查無資料")
    conn.commit()
    cursor.close()
    conn.close()


def delete_the_records():
    """
    刪除紀錄 7
    """
    conn = sqlite3.connect("wanghong.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM  members")
        print(f"=>異動 {cursor.rowcount} 筆記錄")
        conn.commit()
    except sqlite3.Error as error:
        print(f"執行 DELETE 操作時發生錯誤：{error}")
    cursor.close()
    conn.close()


def display_menu():
    """
    Display a simple menu.
    """
    print("---------- 選單 ----------")
    print("0 / Enter 離開")
    print("1 建立資料庫與資料表")
    print("2 匯入資料")
    print("3 顯示所有紀錄")
    print("4 新增記錄")
    print("5 修改記錄")
    print("6 查詢指定手機")
    print("7 刪除所有記錄")
    print("-" * 30)
    print("")


# You can add more functions for additional menu options
