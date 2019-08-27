from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaFileUpload
import os
from google.oauth2 import service_account

CURRDIR = os.path.join(os.getcwd(), "face")
CLIENTID = os.path.join(CURRDIR, "client_id.json")
STOREFILE = os.path.join(CURRDIR, "storage.json")
FILESTORE = os.path.join(CURRDIR, "dataset")
FILE_TEST = os.path.join(FILESTORE, "face_20190824/face.1566623059835.jpg")
UPLOAD_FOLDERID = "1GWpdI-vkIjXmdrCWkmJYH-lrQMQAFEAp"
SERVICE_ACCOUNT_FILE = os.path.join(CURRDIR, "p1143d5a02b19.json")


# def init_drive():
SCOPES = "https://www.googleapis.com/auth/drive"

store = file.Storage(STOREFILE)
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(CLIENTID, SCOPES)
    creds = tools.run_flow(flow, store)

drive_api = discovery.build("drive", "v3", http=creds.authorize(Http()))

# return drive_api


def get_drive_list():
    # drive_api = init_drive()
    files = drive_api.files().list().execute().get("files", [])
    for f in files:
        print(f["name"], f["mimeType"])


# get_drive_list()


def upload_image(filepath, name, folderid=UPLOAD_FOLDERID):
    # drive_api = init_drive()
    image_metadata = {"name": name, "parents": [folderid]}
    media = MediaFileUpload(filepath, mimetype="image/jpeg")
    file = (
        drive_api.files()
        .create(body=image_metadata, media_body=media, fields="id")
        .execute()
    )
    print("Image file ID: ", file.get("id"))


def upload_image_to_folder_name(filepath, name, foldername):
    up_folder_id = create_foder(name=foldername)
    upload_image(filepath=filepath, name=name, folderid=up_folder_id)


# upload_image(filepath=FILE_TEST, name="photo.jpg", folderid=FOLDERID_TEST)


def create_foder(name, parentID=UPLOAD_FOLDERID):
    # drive_api = init_drive()
    folder_exist = check_folder_exist(name)
    if folder_exist is None:
        folder_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parentID],
        }
        root_folder = drive_api.files().create(body=folder_metadata).execute()
        print("Folder created with id: ", root_folder["id"])
        return root_folder["id"]
    print("Folder existed with id: ", folder_exist["id"])
    return folder_exist["id"]


def check_folder_exist(foldername):
    # drive_api = init_drive()
    folders = (
        drive_api.files()
        .list(
            q="name='"
            + foldername
            + "' and mimeType='application/vnd.google-apps.folder'",
            spaces="drive",
            fields="files(id, name, mimeType, parents, trashed)",
        )
        .execute()
        .get("files", [])
    )

    if len(folders) > 0:
        for fol in folders:
            if not fol["trashed"] and UPLOAD_FOLDERID in fol["parents"]:
                return fol
                break
    return None


print(folderInGDrive("face_20190824"))
# check_folder_exist("yyy")
# print("xxx" in ["xx", "yyy"])
# print(create_foder("face_20190824"))
# upload_image_to_folder_name(
#     filepath=FILE_TEST, name="face.1566623059835.jpg", foldername="face_20190824"
# )


# files = []
# # r=root, d=directories, f = files
# for r, d, f in os.walk(os.path.join(FILESTORE, "face_20190824")):
#     for file in f:
#         if ".jpg" in file:
#             files.append({"name": file, "path": os.path.join(r, file)})

# for f in files:
#     print(f)
#     upload_image_to_folder_name(
#         filepath=f["path"], name=f["name"], foldername="face_20190824"
#     )

