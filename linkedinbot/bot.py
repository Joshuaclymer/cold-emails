from numpy import RAISE, NaN
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas
import numpy as np
import re

inpDF = pandas.read_csv('ugrad_students_copy.csv')
records = inpDF.to_dict("index")
exportFile = "linkedin_info.csv"

def getUrl(firstname, lastname):
    baselink = 'https://www.linkedin.com/search/results/people/?keywords='
    addemdum = '&origin=SWITCH_SEARCH_VERTICAL'
    params = ["Columbia", "University", firstname, lastname]
    keywords = "%20".join(params)
    return baselink + keywords + addemdum

def getYearFromString(year):
    gradYear = int(year.split(" – ")[1])
    return 2025 - gradYear + 1

def makeSafe(func):
    try:
        return func()
    except:
        return np.nan

def test(func):
    try:
        return func()
    except Exception as e:
        return e
#get index
indexFile = open("lastindex.txt", "r")
startIndex = int(indexFile.read())
indexFile.close()

#Login
driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fsearch%2Fresults%2Fpeople%2F%3Fkeywords%3DColumbia%2520University%2520Joshua%2520Clymer%26origin%3DSWITCH_SEARCH_VERTICAL&fromSignIn=true&trk=cold_join_sign_in")
emailInp = driver.find_element_by_id("username")
emailInp.send_keys("joshuamclymer@gmail.com")
passwordInp = driver.find_element_by_id("password")
passwordInp.send_keys("1Wormgear")
passwordInp.send_keys(Keys.RETURN)

def checkPage(person):
    time.sleep(1)
    person.click()
    time.sleep(1)
    reached_page_end = False
    last_height = driver.execute_script("return document.body.scrollHeight")
    while not reached_page_end:
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
        schools = driver.find_elements_by_xpath("//a[contains(@data-control-name, 'background_details_school')]")
        if (len(schools) != 0):
            break
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            time.sleep(0.5)
            reached_page_end = True
        else:
            last_height = new_height
    columbiaFound = False
    for school in schools:
        info = school.find_element_by_class_name("pv-entity__degree-info")
        if info.find_element_by_xpath("./h3").text in ["Columbia University in the City of New York", "Columbia Engineering", "Columbia College, Columbia University", "Barnard College", "Columbia"]:
            columbiaFound = True
            elements = info.find_elements_by_xpath("./p")
            gpaIndex = ""
            gpa = np.nan
            for element in elements:
                if ("GPA" in element.text):
                    gpaIndex = elements.index(element)
            if (gpaIndex != ""):
                gpa = float(re.findall(r'\d+.\d+', info.find_elements_by_xpath("./p")[gpaIndex].text.split("\n")[1])[0])
                major = makeSafe(lambda : info.find_elements_by_xpath("./p")[gpaIndex - 1].text.split("\n")[1])
            else:
                major = makeSafe(lambda : info.find_elements_by_xpath("./p")[1].text.split("\n")[1])
            yearString = makeSafe(lambda : school.find_element_by_xpath(".//p[contains(@class, 'pv-entity__dates t-14 t-black--light t-normal')]").text.split("\n")[1])
            year = makeSafe(lambda : getYearFromString(yearString))
            if (year != np.nan and (year < 1 or year > 4)):
                print("Year not valid")
                raise
            else:
                try:
                    inpDF.at[i, "GPA"] = gpa
                    inpDF.at[i, "Year"] = year
                    inpDF.at[i, "Major"] = major
                    inpDF.to_csv(r"./linkedin_info.csv", encoding='utf-8', index=False)
                    print("Updated the record for {} {}".format(record["First Name"], record["Last Name"]))
                except Exception as e: 
                    print("Error writing to output table:")
                    print(e)
                try:
                    with open("lastindex.txt", "w") as f:
                        f.write(str(i))
                except:
                    print("something went wrong writing to index file")
                break
    if (not columbiaFound):
        print("Columbia not found in schools")
        raise
    else:
        pass
        # if you want to connect with all the other undergrads in the school, lol.
        # try:
        #     driver.find_element_by_xpath('//button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action"]').click()
        #     time.sleep(0.2)
        #     driver.find_element_by_xpath('//button[@aria-label="Send now"]').click()
        # except:
        #     try: 
        #         driver.find_element_by_xpath('//button[@aria-label="More actions"]').click()
        #         time.sleep(0.2)
        #         driver.find_element_by_xpath('//div[@class="pvs-profile-actions__action display-flex align-items-center  artdeco-dropdown__item artdeco-dropdown__item--is-dropdown ember-view"]').click()
        #         time.sleep(0.2)
        #         driver.find_element_by_xpath('//button[@aria-label="Connect"]').click()
        #         time.sleep(0.2)
        #         driver.find_element_by_xpath('//button[@aria-label="Send now"]').click()
        #     except:
        #         pass
#iterate through rows of inpDF
for i in range(startIndex, inpDF.shape[0]):
    record = records[i]
    time.sleep(1)
    driver.get(getUrl(record["First Name"], record["Last Name"]))
    time.sleep(2)
    peopleButtons = driver.find_elements_by_xpath("//button[contains(@aria-label, 'People')]")
    if (len(peopleButtons) == 0):
        raise "Not on Search Page anymore"
    print("{} of {}".format(i, inpDF.shape[0]))
    try:
        people = driver.find_elements_by_class_name("app-aware-link")
        if people[1].find_elements_by_xpath('.//span[contains(@aria-hidden, "true")]')[0].get_attribute("innerText").split(" ")[1] == record["Last Name"]:
            checkPage(people[1])
        else:
            print("Did not appear in search results")
            raise
    except:
        pass
    #time.sleep(1000)