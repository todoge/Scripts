from selenium import webdriver
PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)

def authenticate():
    try:
        f = open("cookies.txt", "r")
        f.close()
    except FileNotFoundError: 
        prompt()
    
    
    data = get_username_and_password()
    username = data[0]
    password = data[1]
    auth = login(username, password)
 
    while auth is not True:
        print("Authentication Failed. Please try again!\n")
        prompt()
        data = get_username_and_password()
        username = data[0]
        password = data[1]
        print(username + " " + password)
        auth = login(username, password)
        print(str(auth))

def prompt():
    f = open("cookies.txt", "w")
    username = input("luminus username: ")
    f.write(username + "\n")
    password = input("luminus password: ")
    f.write(password + "\n")
    f.close()

def get_username_and_password():
    f = open("cookies.txt", "r")
    username = f.readline()
    password = f.readline()
    f.close()
    return username, password;


def login(username, password):
    url = "https://luminus.nus.edu.sg"
    try:
        driver.get(url)
        driver.find_element_by_xpath('//a[text()="NUS User Login"]').click()
        driver.find_element_by_id("userNameInput").send_keys(username)
        driver.find_element_by_id("passwordInput").send_keys(password)
        try:
            driver.find_element_by_id("submitButton").click()
            error = driver.find_element_by_id("errorText")
            return False
        except:
            return True
        
    except Exception as e:
        print(e)
        return False
        
authenticate()