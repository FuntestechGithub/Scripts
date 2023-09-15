from azure.storage.blob import BlobServiceClient
import os

connection_string = ""
service = BlobServiceClient.from_connection_string(conn_str=connection_string)
container_client = service.get_container_client(container="file-transfer-share")

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if name != "upload-files-to-blob.exe":
            currFile = os.path.join(root, name)
            blob_client = container_client.get_blob_client(blob=currFile[2:])
            with open(currFile, mode="rb") as data:
                blob_client.upload_blob(data=data, overwrite=True)
                print("Uploaded " + currFile + " to Azure Blob Storage ctasbxarmstauw2001")

input("Press enter to exit;")