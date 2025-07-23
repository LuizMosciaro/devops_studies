import subprocess
import os
from time import sleep
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

FILENAME = 'sysbackup.tar.gz'

account_url = "https://devopsstudyphase12025.blob.core.windows.net"
default_credential = DefaultAzureCredential()

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(account_url, credential=default_credential)

# Create a blob client using the local file name as the name for the blob
blob_client = blob_service_client.get_container_client(container='container-teste-blob')


def compress_critical_directories() -> None:
    """
    Creates a compressed backup of critical directories using tar and gzip,
    then generates a SHA256 checksum file for the resulting archive.
    The backup is saved as FILENAME and the checksum as FILENAMEsha256'.
    """
    subprocess.run(
        "sudo tar -czf sysbackup.tar.gz /bin /tmp /etc && sha256sum sysbackup.tar.gz > sysbackup.tar.gz.sha256",
        shell=True,
        check=True
    )


def upload_sysbackup_azure() -> None:
    try:
        # Upload the created file
        with open(file=FILENAME, mode="rb") as data:
            blob_client.upload_blob(name=FILENAME,data=data)
        print(f'File {FILENAME} sent to Azure')
    except Exception as ex:
        print('Exception:')
        print(ex)

def check_file_integrity() -> None:
    print("Checking backup file integrity")
    subprocess.run(
        "sudo sha256sum -c sysbackup.tar.gz.sha256",
        shell=True,
        check=True
    )
    
def download_sysbackup_azure() -> None:
    try:
        # Download the created file
        blob_client.download_blob(FILENAME)
        print(f'File {FILENAME} downloaded from Azure')
        with open(file=FILENAME, mode="wb") as sample_blob:
            download_stream = blob_client.download_blob(FILENAME)
            sample_blob.write(download_stream.readall())
    except Exception as ex:
        print('Exception:')
        print(ex)
    finally:
        check_file_integrity()


if __name__ == "__main__":
    compress_critical_directories()
    upload_sysbackup_azure()
    download_sysbackup_azure()