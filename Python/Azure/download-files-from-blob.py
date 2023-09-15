from azure.storage.blob import BlobServiceClient
import os

connection_string = ""
service = BlobServiceClient.from_connection_string(conn_str=connection_string)
container_client = service.get_container_client(container="file-transfer-share")
blob_list = container_client.list_blobs()

path = "./downloaded-blobs/"
# create folder if doesn't exit
if not os.path.exists("downloaded-blobs"):
    os.makedirs("downloaded-blobs")


for blob in blob_list:
    blob_client = container_client.get_blob_client(blob=blob.name)
    with open(file=os.path.join(path, blob.name), mode="wb") as my_blob:
        blob_data = blob_client.download_blob()
        my_blob.write(blob_data.readall())
        print("Uploaded " + blob.name + " to local folder downloaded-blobs.")
        blob_client.delete_blob()

input("Press enter to exit;")