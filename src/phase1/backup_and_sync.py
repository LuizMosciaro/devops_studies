import subprocess
import os

"""Backup & Remote Sync

- Create a script that compresses critical directories,

- Send to Google Drive and/or SFTP server;

Validate integrity via checksums (MD5/SHA256).

Extra exercises:

Implement backup rotation (7-day cycle),

Build a small CLI interface with argparse,

Add notification via Slack or Telegram for success/error."""


def compress_critical_directories() -> None:
    """
    Creates a tar archive containing a backup of critical system directories:
    /bin, /tmp, and /etc. The resulting file is saved as 'sys_bkp.tar' in the
    current directory. Requires superuser permissions (sudo).
    """

    subprocess.run(["sudo", "tar", "-cvf", "sys_bkp.tar", "bin/", "tmp/", "etc/"])
    
