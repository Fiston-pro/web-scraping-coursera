from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
folderId = "1xQjBBteb3VxUtSbl3KmGc9l44_DufUxP"
filename = 'church.data-science.csv'

gfile = drive.CreateFile({'parents': [{'id': folderId}],'title': filename })
gfile.SetContentFile(f'./static/csv/{filename}')
gfile.Upload()

file_list = drive.ListFile({'q': 'title = "time.data-science"'}).GetList()
fileId = file_list[0]['id']

print(f'https://drive.google.com/file/d/{fileId}/view')
     

   