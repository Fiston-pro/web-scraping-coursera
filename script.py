
from bs4 import BeautifulSoup
import requests
import csv
from faker import Faker


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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

    with open(f"{fileName}.csv", "w", newline="") as csvfile:
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

            # to make sure every variable contains something or at least none to avoid errors
            if courseName != None:
                courseName = courseName.text
            if courseProvider != None:
                courseProvider = courseProvider.text
            if courseDescription != None:
                courseDescription = courseDescription.text
            if nbrOfStudents != None:
                nbrOfStudents = nbrOfStudents.text
            if nbrOfRatings != None:
                nbrOfRatings = nbrOfRatings.text
            # start writing to file
            writer.writerow({"Course Name": courseName,"Course Provider": courseProvider,"Course Description":courseDescription,"# of Students enrolled":nbrOfStudents,"# of Ratings":nbrOfRatings})

    # upload the csv file to google drive 
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    folderId = "1xQjBBteb3VxUtSbl3KmGc9l44_DufUxP"
    filepath = f'{fileName}.csv'

    gfile = drive.CreateFile({'parents': [{'id': folderId}],'title': fileName})
    gfile.SetContentFile(filepath)
    gfile.Upload()

    # make a link to the file
    file_list = drive.ListFile({'q': f'title = "{fileName}"'}).GetList()
    fileId = file_list[0]['id']

    return f'https://drive.google.com/file/d/{fileId}/view'

