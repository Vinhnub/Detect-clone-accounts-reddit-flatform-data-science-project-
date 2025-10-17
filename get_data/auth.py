from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

gauth = GoogleAuth()

# Chỉ định file credentials JSON
gauth.LoadClientConfigFile("utils/ggdriver_token.json")

# Mở trình duyệt để đăng nhập Google lần đầu
gauth.LocalWebserverAuth()

# Lưu token vào file
gauth.SaveCredentialsFile("credentials.json")

drive = GoogleDrive(gauth)
file = drive.CreateFile({'title': 'test_upload.txt'})
file.Upload()
print("Upload thành công!")
