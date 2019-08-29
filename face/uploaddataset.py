from gdrive import upload_dataset
from datetime import datetime
import os

myFile = open(os.path.join(os.getcwd(), "face", "log_upload.txt"), "a")

myFile.write("\nUploaded on " + str(datetime.now()))
# upload_dataset()
