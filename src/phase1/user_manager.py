import subprocess
import os

"""
# User Manager

Write a Python script that:

- Creates/removes users and groups (using subprocess → useradd, groupadd),
- Applies password policy (complexity, expiration),
- Generates centralized logs (file + journalctl).

# Extra exercises:

- Implement a “dry-run” mode that shows what would be done without making changes.
- Add email alert on failure (use smtplib)
- Schedule daily execution via cron and check logs.
"""

def adduser(user: str, group: str) -> str | None:
    try:
        subprocess.run(["sudo", "useradd", "-G", group, user], check=True, capture_output=True,)
    except subprocess.CalledProcessError as ErrorCall:
        # Check if the group exists
        if ErrorCall.returncode == 6:
            if ErrorCall.stderr:
                if ErrorCall.stderr.decode('utf-8') == f"useradd: group '{group}' does not exist\n":
                    return f"Group '{group}' does not exists"
        elif ErrorCall.returncode == 9:
            if ErrorCall.stderr:
                if ErrorCall.stderr.decode('utf-8') == f"useradd: user '{user}' already exists":
                    return f"User {user} already exists"
        else:
            return ErrorCall.stderr
    except Exception as Error:
        return str(Error)


def groupadd(group: str) -> str | None:
    try:
        result = subprocess.run(["sudo", "groupadd", group], check=True, capture_output=True,)
        if not result.check_returncode():
            return f"Group '{group}' created"
    except Exception as Error:
        return str(Error)  


if __name__=="__main__":
    print(groupadd('testgroup1'))