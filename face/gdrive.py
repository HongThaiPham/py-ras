from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaFileUpload
import os
import cv2
from face_detect import face_detect


CURRDIR = os.path.join(os.getcwd(), "face")
CLIENTID = os.path.join(CURRDIR, "client_id.json")
STOREFILE = os.path.join(CURRDIR, "storage.json")
FILESTORE = os.path.join(CURRDIR, "dataset")
FILE_TEST = os.path.join(FILESTORE, "face_20190824/face.1566623059835.jpg")
PARENT_FOLDER = "1GWpdI-vkIjXmdrCWkmJYH-lrQMQAFEAp"


# def init_drive():
SCOPES = "https://www.googleapis.com/auth/drive"

store = file.Storage(STOREFILE)
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(CLIENTID, SCOPES)
    creds = tools.run_flow(flow, store)

SERVICE = discovery.build("drive", "v3", http=creds.authorize(Http()))


# ---------------------------------------
# GDrive API: Create New Folder
# ---------------------------------------
def createGDriveFolder(foldername, parent=PARENT_FOLDER):
    file_metadata = {
        "name": foldername,
        "parents": [parent],
        "mimeType": "application/vnd.google-apps.folder",
    }

    folder = SERVICE.files().create(body=file_metadata, fields="id").execute()
    print("Folder created!")
    print("FolderID:", folder.get("id"))
    return folder.get("id")


# ------------------------------------
# GDrive API: Check if Filename exists
# ------------------------------------
def fileInGDrive(filename, parent_folder=PARENT_FOLDER):
    results = (
        SERVICE.files()
        .list(
            q="mimeType='image/jpeg' and name='"
            + filename
            + "' and trashed = false and parents in '"
            + parent_folder
            + "'",
            fields="nextPageToken, files(id, name)",
        )
        .execute()
    )
    items = results.get("files", [])
    if items:
        return True
    else:
        return False


# ------------------------------------
# GDrive API: Check if Folder exists
# ------------------------------------
def folderInGDrive(filename):
    results = (
        SERVICE.files()
        .list(
            q="mimeType='application/vnd.google-apps.folder' and name='"
            + filename
            + "' and trashed = false and parents in '"
            + PARENT_FOLDER
            + "'",
            fields="nextPageToken, files(id, name)",
        )
        .execute()
    )
    items = results.get("files", [])
    if items:
        return True
    else:
        return False


# ---------------------------------------
# GDrive API: Upload files to Google Drive
# ---------------------------------------
def writeImageToGDrive(filename, source, folder_id):
    file_metadata = {"name": filename, "parents": [folder_id], "mimeType": "image/jpeg"}
    media = MediaFileUpload(source, mimetype="image/jpeg")

    if fileInGDrive(filename) is False:
        file = (
            SERVICE.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print("Upload Success!")
        print("File ID:", file.get("id"))
        return file.get("id")

    else:
        print("File already exists as", filename)


def getFolderfromGDrive(folder_name):
    # Main Folder

    results = (
        SERVICE.files()
        .list(
            q="mimeType='application/vnd.google-apps.folder' and name='"
            + folder_name
            + "' and trashed = false and parents in '"
            + PARENT_FOLDER
            + "'",
            fields="nextPageToken, files(id, name)",
        )
        .execute()
    )

    items = results.get("files", [])

    # print(items)

    if not items:
        return ""
    else:
        # print(items[-1]["name"])
        return items[-1]["id"]


# getFolderfromGDrive("face_20190824")

# ---------------------------------------
# Upload Files in GDrive
# ---------------------------------------


def uploadFiles(image_dataset):

    for folder in image_dataset:
        print("------")
        upload_folder = folder["name"]
        print("Processing folder: " + upload_folder)

        # Create folder if it doesnt exist yet
        if folderInGDrive(upload_folder) is False:
            createGDriveFolder(upload_folder)
            print("Folder created for: ", upload_folder)

        for image in folder["images"]:
            writeImageToGDrive(
                image["name"], image["path"], getFolderfromGDrive(upload_folder)
            )


def get_dataset(filestore=FILESTORE):
    result = []
    folders = os.listdir(filestore)
    # print(folders)
    for folder in folders:
        image_items = []
        for r, d, f in os.walk(os.path.join(filestore, folder)):
            for file in f:
                if ".jpg" in file:
                    path = os.path.join(r, file)
                    img = cv2.imread(path)
                    faces = face_detect(img)
                    if len(faces)>0:
                        image_items.append(
                            {"name": file, "path": path}
                        )
        result.append({"name": folder, "images": image_items})
    return result


def upload_dataset():
    dataset = get_dataset()
    uploadFiles(dataset)

