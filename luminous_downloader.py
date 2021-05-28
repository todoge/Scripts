import os
from sys import path
import time
from selenium import webdriver


DRIVERPATH = "chromedriver.exe"
url = "https://luminus.nus.edu.sg/"

# INITIALISE BROWSER
def initialise_driver(headless=True):
    """ Helper function that creates a new Selenium browser """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    prefs = {}
    prefs["profile.default_content_settings.popups"]=0
    options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(options=options, executable_path=DRIVERPATH)
    return browser

driver = initialise_driver()


# Authenticate into luminus
def authenticate():
    try:
        f = open("cookies.txt", "r")
        f.close()
    except FileNotFoundError: 
        prompt_username_and_password()
    
    
    data = get_username_and_password()
    username = data[0]
    password = data[1]
    auth = login(username, password)
 
    while auth is not True:
        print("Authentication Failed. Please try again!\n")
        prompt_username_and_password()
        data = get_username_and_password()
        username = data[0]
        password = data[1]
        print(username + " " + password)
        auth = login(username, password)
        print(str(auth))

def login(username, password):
    try:
        driver.get(url + "/modules")
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

def prompt_username_and_password():
    f = open("cookies.txt", "w")
    username = input("luminus username:")
    f.write(username + "\n")
    password = input("luminus password:")
    f.write(password + "\n")
    f.close()

def get_username_and_password():
    f = open("cookies.txt", "r")
    username = f.readline()
    password = f.readline()
    f.close()
    return username, password;


# Getting the default download location for files
def get_download_path():
    f = open("cookies.txt", "r")
    try:
        download_path = f.readlines()[2]
        f.close()
        return download_path
    except:
        f.close()
        prompt_download_location()
        get_download_path()

def prompt_download_location():
    f = open("cookies.txt", "r")
    path = input("Input dirctory path to store downloads (eg. C:/Users/user-name/Desktop/):")
    data = f.readlines()
    try:
        data[2] = path
        f = open('cookies.txt', 'w')
        f.writelines( data )
    except IndexError:
        f = open('cookies.txt', 'a')
        f.write(path)
    finally:
        f.close()


# Close all Popups in Luminus if any
def close_all_popups():
    time.sleep(1)
    popups = driver.find_elements_by_xpath("//icon[@name='close']")
    for popup in popups:
        try:
            popup.click()
        except:
            continue


def create_module(module_link, download_path):

        driver.get(module_link + "/files")
        time.sleep(1)
        module_name = driver.find_element_by_xpath("//small").text
        
        print(module_name)
        # Create main folder to house the files
        file_dir = download_path + "/" + module_name
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        create_structure(file_dir)
        

def create_structure(download_path, parent_url, item_no):
    # if current page houses folders
    is_folder = 'Folder' in driver.find_element_by_xpath("//div[@class='name disable-select']").text
    # if it is a folder page
    if is_folder:
        #Get all files
        folders = driver.find_elements_by_xpath("//list-view-item")
        # print(len(folders))
        for folder in folders:
            folder_name = folder.find_element_by_class_name("filename").text
            status = folder.find_element_by_tag_name("folder-status").text
            print(folder_name + " : " + status)
            if status == "Open":
                download_path = download_path + "/" + folder_name
                if not os.path.exists(download_path):
                    os.mkdir(download_path)
                folder.click()
                create_structure(download_path, driver.current_url, )
    else:
        options = webdriver.ChromeOptions()
        prefs = {}
        prefs["download.default_directory"]=download_path
        options.add_experimental_option("prefs", prefs)
        files = driver.find_elements_by_xpath("//list-view-item")
        for file in files:
            file.click()




def newChromeBrowser(headless=True, downloadPath=None):
    """ Helper function that creates a new Selenium browser """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    if downloadPath is not None:
        prefs = {}
        os.makedirs(downloadPath)
        prefs["profile.default_content_settings.popups"]=0
        prefs["download.default_directory"]=downloadPath
        options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(options=options, executable_path=CHROMEDRIVER_PATH)
    return browser




def Main():
    authenticate()
    close_all_popups()
    download_path = get_download_path()
    while not os.path.exists(download_path):
        print(download_path + " is not a valid location! Try giving a valid location")
        prompt_download_location()
        download_path = get_download_path()

    module_cards = driver.find_elements_by_class_name("module-card")
    module_urls = []

    for module_card in module_cards:
        module_link = module_card.get_attribute("href")
        module_urls.append(module_link)

    for module_link in module_urls:
        create_module(module_link, download_path)

    input("cancel")


Main()
