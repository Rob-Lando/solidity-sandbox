from modules.env_encryptor import setup_env

def main():
    
    up_to_date = input("Is .env up to date? [y/n] -> ").strip().lower()
    assert up_to_date in ['y','n'], "Please type y for 'yes', n for 'no'"

    if up_to_date == 'n':
        setup_env("../.env","verify.json")
    else:
        print("Ok...")

if __name__ == "__main__":
    main()
    