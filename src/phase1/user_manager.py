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

def add_new_user(user: str) -> str | None:
    try:
        result = subprocess.run(["sudo", "useradd", user], check=True, capture_output=True,)
        if not result.check_returncode():
            return f"User '{user}' created"
    except subprocess.CalledProcessError as ErrorCall:
        if ErrorCall.returncode == 9:
            if ErrorCall.stderr:
                if ErrorCall.stderr.decode('utf-8').strip() == f"useradd: user '{user}' already existsErrorCall.stderr.decode('utf-8')":
                    return f"User {user} already exists"
        else:
            return ErrorCall.stderr

    except Exception as Error:
        return str(Error)  

def add_user_to_group(user: str, group: str) -> str | None:
    try:
        subprocess.run(["sudo", "useradd", "-G", group, user], check=True, capture_output=True,)
    except subprocess.CalledProcessError as ErrorCall:
        # Check if the group exists
        if ErrorCall.returncode == 6:
            if ErrorCall.stderr:
                if ErrorCall.stderr.decode('utf-8').strip() == f"useradd: group '{group}' does not exist\n":
                    return f"Group '{group}' does not exists"
        elif ErrorCall.returncode == 9:
            if ErrorCall.stderr:
                if ErrorCall.stderr.decode('utf-8').strip() == f"useradd: user '{user}' already exists":
                    return f"User {user} already exists"
        else:
            return ErrorCall.stderr
    except Exception as Error:
        return str(Error)

def delete_user(user: str, force: bool = False) -> str | None:
    try:
        if not force:
            result = subprocess.run(["sudo", "userdel", user], check=True, capture_output=True,)
        else:
            result = subprocess.run(["sudo", "-f", "userdel", user], check=True, capture_output=True,)

        if not result.check_returncode():
            return f"User '{user}' deleted"
        
    except subprocess.CalledProcessError as ErrorCall:
        # Check if the user exists
        if ErrorCall.returncode == 6:
            if ErrorCall.stderr:
                if ErrorCall.stderr.decode('utf-8').strip() == f"userdel: user '{user}' does not exist":
                    return f"User '{user}' does not exists"
        else:
            return ErrorCall.stderr

    except Exception as Error:
        return str(Error)  

def add_new_group(group: str) -> str | None:
    try:
        result = subprocess.run(["sudo", "groupadd", group], check=True, capture_output=True,)
        if not result.check_returncode():
            return f"Group '{group}' created"
    except Exception as Error:
        return str(Error)  

def delete_group(group: str, force: bool = False) -> str | None:
    try:
        if not force:
            result = subprocess.run(["sudo", "groupdel", group], check=True, capture_output=True,)
        else:
            result = subprocess.run(["sudo", "-f", "groupdel", group], check=True, capture_output=True,)

        if not result.check_returncode():
            return f"Group '{group}' deleted"
        
    except subprocess.CalledProcessError as ErrorCall:
        # Check if the group exists
        if ErrorCall.returncode == 6:
            if ErrorCall.stderr:
                if ErrorCall.stderr.decode('utf-8').strip() == f"groupdel: group '{group}' does not exist":
                    return f"Group '{group}' does not exists"
        else:
            return ErrorCall.stderr

    except Exception as Error:
        return str(Error)  

if __name__=="__main__":
    print(delete_user('testuser'))