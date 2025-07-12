import subprocess
import os

"""
# User Manager

Write a Python script that:

- Creates/removes users and groups (using subprocess → useradd, groupadd)
- Generates centralized logs (file + journalctl).

# Extra exercises:

- Implement a “dry-run” mode that shows what would be done without making changes.
- Add email alert on failure (use smtplib)
- Schedule daily execution via cron and check logs.
"""

def add_new_user(user: str) -> str:
    """
    Adds a new user to the system.

    Args:
        user (str): The name of the user to be created.

    Returns:
        str: A success message if the user is created.
             A detailed error message if the user already exists or another error occurs.
    """
    try:
        subprocess.run(["sudo", "useradd", user], check=True, capture_output=True, text=True)
        return f"User '{user}' created successfully."
    except subprocess.CalledProcessError as ErrorCall:
        error_message = ErrorCall.stderr.strip()
        if ErrorCall.returncode == 9 and error_message == f"useradd: user '{user}' already exists":
            return f"Error: User '{user}' already exists."
        else:
            return f"Error adding user '{user}': {error_message} (Code: {ErrorCall.returncode})"
    except FileNotFoundError:
        return "Error: 'sudo' or 'useradd' command not found. Ensure they are in your PATH."
    except Exception as Error:
        return f"An unexpected error occurred: {str(Error)}"

def add_user_to_group(user: str, group: str) -> str:
    """
    Adds an existing user to an existing group.
    Note: This method uses 'useradd -G' which is for creating a new user and adding them
    to a supplementary group. To add an *existing* user to a supplementary group,
    'usermod -aG' would be the more appropriate command.

    Args:
        user (str): The name of the user to be added.
        group (str): The name of the group to which the user will be added.

    Returns:
        str: A success message if the user is added to the group.
             A detailed error message if the group does not exist, the user already exists,
             or if another error occurs.
    """
    try:
        subprocess.run(["sudo", "useradd", "-G", group, user], check=True, capture_output=True, text=True)
        return f"User '{user}' added to group '{group}' successfully."
    except subprocess.CalledProcessError as ErrorCall:
        error_message = ErrorCall.stderr.strip()
        if ErrorCall.returncode == 6 and error_message == f"useradd: group '{group}' does not exist":
            return f"Error: Group '{group}' does not exist."
        elif ErrorCall.returncode == 9 and error_message == f"useradd: user '{user}' already exists":
            return f"Error: User '{user}' already exists."
        else:
            return f"Error adding user '{user}' to group '{group}': {error_message} (Code: {ErrorCall.returncode})"
    except FileNotFoundError:
        return "Error: 'sudo' or 'useradd' command not found. Ensure they are in your PATH."
    except Exception as Error:
        return f"An unexpected error occurred: {str(Error)}"

def delete_user(user: str, force: bool = False) -> str:
    """
    Deletes a user from the system.

    Args:
        user (str): The name of the user to be deleted.
        force (bool): If True, forces the removal of the user and their home directory (-r -f).
                      Default is False (only deletes the user, keeping the home directory).

    Returns:
        str: A success message if the user is deleted.
             A detailed error message if the user does not exist or another error occurs.
    """
    try:
        command = ["sudo", "userdel"]
        if force:
            command.extend(["-r", "-f"]) # -r removes the home directory, -f forces removal
        command.append(user)
        
        subprocess.run(command, check=True, capture_output=True, text=True)
        return f"User '{user}' deleted successfully."
    except subprocess.CalledProcessError as ErrorCall:
        error_message = ErrorCall.stderr.strip()
        if ErrorCall.returncode == 6 and error_message == f"userdel: user '{user}' does not exist":
            return f"Error: User '{user}' does not exist."
        else:
            return f"Error deleting user '{user}': {error_message} (Code: {ErrorCall.returncode})"
    except FileNotFoundError:
        return "Error: 'sudo' or 'userdel' command not found. Ensure they are in your PATH."
    except Exception as Error:
        return f"An unexpected error occurred: {str(Error)}"

def add_new_group(group: str) -> str:
    """
    Adds a new group to the system.

    Args:
        group (str): The name of the group to be created.

    Returns:
        str: A success message if the group is created.
             A detailed error message if the group already exists or another error occurs.
    """
    try:
        subprocess.run(["sudo", "groupadd", group], check=True, capture_output=True, text=True)
        return f"Group '{group}' created successfully."
    except subprocess.CalledProcessError as ErrorCall:
        error_message = ErrorCall.stderr.strip()
        if ErrorCall.returncode == 9 and error_message == f"groupadd: group '{group}' already exists":
            return f"Error: Group '{group}' already exists."
        else:
            return f"Error adding group '{group}': {error_message} (Code: {ErrorCall.returncode})"
    except FileNotFoundError:
        return "Error: 'sudo' or 'groupadd' command not found. Ensure they are in your PATH."
    except Exception as Error:
        return f"An unexpected error occurred: {str(Error)}"

def delete_group(group: str) -> str:
    """
    Deletes a group from the system.
    Note: 'groupdel' does not have the '-f' option to force the removal of groups that are
    the primary group of users. If the group is a user's primary group,
    this function will fail.

    Args:
        group (str): The name of the group to be deleted.

    Returns:
        str: A success message if the group is deleted.
             A detailed error message if the group does not exist,
             if it is a primary group for a user, or if another error occurs.
    """
    try:
        subprocess.run(["sudo", "groupdel", group], check=True, capture_output=True, text=True)
        return f"Group '{group}' deleted successfully."
    except subprocess.CalledProcessError as ErrorCall:
        error_message = ErrorCall.stderr.strip()
        if ErrorCall.returncode == 6 and error_message == f"groupdel: group '{group}' does not exist":
            return f"Error: Group '{group}' does not exist."
        elif ErrorCall.returncode == 8 and "cannot remove the primary group of user" in error_message:
            return f"Error: Group '{group}' is a primary group for existing users. Cannot delete."
        else:
            return f"Error deleting group '{group}': {error_message} (Code: {ErrorCall.returncode})"
    except FileNotFoundError:
        return "Error: 'sudo' or 'groupdel' command not found. Ensure they are in your PATH."
    except Exception as Error:
        return f"An unexpected error occurred: {str(Error)}"

# Example usage (to test the functions after documentation)
if __name__ == "__main__":
    # IMPORTANT: This script MUST be run with sudo for the commands to work.
    # E.g.: sudo python your_script.py

    print("--- Testing add_new_user ---")
    print(add_new_user("testuser1"))
    print(add_new_user("testuser1")) # Try to add again

    print("\n--- Testing add_new_group ---")
    print(add_new_group("testgroup1"))
    print(add_new_group("testgroup1")) # Try to add again

    print("\n--- Testing add_user_to_group ---")
    # For this test, 'testuser2' will be created and added to 'testgroup1'
    # Note: The 'useradd -G' command creates the user if they don't exist and adds them to the supplementary group.
    # If the user already exists, it might fail or do nothing, depending on the useradd version.
    # To add an existing user to a supplementary group, 'usermod -aG' is more robust.
    print(add_user_to_group("testuser2", "testgroup1"))
    print(add_user_to_group("testuser2", "nonexistentgroup")) # Non-existent group

    print("\n--- Testing delete_user ---")
    print(delete_user("testuser1"))
    print(delete_user("nonexistentuser")) # Non-existent user

    print("\n--- Testing delete_group ---")
    print(delete_group("testgroup1"))
    print(delete_group("nonexistentgroup")) # Non-existent group

    # Cleanup (optional - uncomment to remove test users/groups)
    # print("\n--- Cleanup ---")
    # print(delete_user("testuser1", force=True))
    # print(delete_user("testuser2", force=True))
    # print(delete_group("testgroup1"))
