import os
from pydoc import text
from bs4 import BeautifulSoup
import requests
import csv
from faker import Faker

def runscript(categoryName):
    # get the data from coursera
    defaultUrl = "https://www.coursera.org"
    # category= "%20".join(input().split(" "))
    courseraUrl = "https://www.coursera.org/browse/" + categoryName
    mainPage = requests.get(courseraUrl)
    mainSoup = BeautifulSoup(mainPage.text, 'html.parser')

    foundU= mainSoup.find_all("a", {'class': "nostyle collection-product-card"})   # find the link to the course

    fake = Faker()
    fileName = fake.file_name(extension= categoryName)

    with open(f"./static/csv/{fileName}.csv", "w", newline="") as csvfile:
        fieldnames = ["Course Name", "Course Provider", "Course Description", "# of Students enrolled", "# of Ratings"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for courseName in foundU:
            toUrl = courseName.get('href')
            courseUrl = defaultUrl + toUrl
            print(courseUrl)
            coursePage = requests.get(courseUrl)
            courseSoup = BeautifulSoup(coursePage.text, "html.parser")
            courseName = courseSoup.find("h1",{'class':"banner-title banner-title-without--subtitle m-b-0"})
            courseProvider = courseSoup.find("h3",{'class':"headline-4-text bold rc-Partner__title"})
            courseDescription = courseSoup.find("div",{'class':"content-inner"})
            nbrOfStudents = courseSoup.find("div",{'class':"_1fpiay2"})
            nbrOfRatings = courseSoup.find("span",{'data-test':"ratings-count-without-asterisks"})
            if courseName == None:
                courseName = courseSoup.find("h1",{'class':"banner-title m-b-0"})
            # start writing to file
            writer.writerow({"Course Name": courseName.text,"Course Provider": courseProvider.text,"Course Description":courseDescription.text,"# of Students enrolled":nbrOfStudents.text,"# of Ratings":nbrOfRatings.text})

    # upload the csv file and give the link to the file
    rootDir = os.path.abspath(os.path.dirname(__file__))
    filePath = os.path.join(rootDir, f"static/csc/{fileName}.csv")
    return filePath



