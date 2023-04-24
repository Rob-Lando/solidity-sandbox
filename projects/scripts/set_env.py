from modules.env_helper.env_encryptor import setup_env

def main():
    
    update_env = input("Is .env up to date? [y/n] -> ").strip().lower()
    assert update_env in ['y','n'], "Please type y for 'yes', n for 'no'"

    if update_env == 'n':
        setup_env("../.env")
    else:
        print("Ok...")

if __name__ == "__main__":
    main()
    