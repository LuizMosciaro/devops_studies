import subprocess
import os
import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

"""Backup & Remote Sync

- Create a script that compresses critical directories,

- Send to Google (or Azure Storage) Drive and/or SFTP server;

- Validate integrity via checksums (MD5/SHA256).

Extra exercises:

Implement backup rotation (7-day cycle),

Build a small CLI interface with argparse,

Add notification via Slack or Telegram for success/error."""


def compress_critical_directories() -> None:
    """
    Creates a compressed backup of critical directories using tar and gzip,
    then generates a SHA256 checksum file for the resulting archive.
    The backup is saved as 'sysbackup.tar.gz' and the checksum as 'sysbackup.tar.gz.sha256'.
    """
    subprocess.run(
        "sudo tar -czf sysbackup.tar.gz /bin /tmp /etc && sha256sum sysbackup.tar.gz > sysbackup.tar.gz.sha256",
        shell=True,
        check=True
    )


def send_sysbackup_azure() -> None:
    try:
        account_url = "https://devopsstudyphase12025.blob.core.windows.net"
        default_credential = DefaultAzureCredential()

        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient(account_url, credential=default_credential)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_container_client(container='container-teste-blob')

        # Upload the created file
        with open(file='sysbackup.tar.gz', mode="rb") as data:
            blob_client.upload_blob(name='sysbackup.tar.gz',data=data)
        print('File "sysbackup.tar.gz" sent to Azure')

        blob_list = blob_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)

    except Exception as ex:
        print('Exception:')
        print(ex)

if __name__ == "__main__":
    send_sysbackup_azure()