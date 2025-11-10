from pydrive2.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LoadClientConfigFile("utils/ggdrive_token.json")  # <-- chỉ rõ file
gauth.LocalWebserverAuth()
gauth.SaveCredentialsFile("credentials.json")