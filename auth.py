from pydrive2.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # mở trình duyệt, bạn đăng nhập Gmail của mình
gauth.SaveCredentialsFile("credentials.json")
print("✅ Đã lưu credentials.json thành công!")
