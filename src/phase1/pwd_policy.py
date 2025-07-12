import re
import subprocess
import os

"""
Password Policies:

Write a Python script that:
- Applies password policy (complexity, expiration)

"""

CONFIG_FILE = "/etc/pam.d/common-password"
BACKUP_FILE = "/etc/pam.d/common-password.bak"

def replace_minlen_value(line: str, new_minlen: int) -> str:
    """
    Replaces the 'minlen' value in a configuration string.

    Args:
        line (str): The configuration line containing 'minlen='.
        new_minlen (int): The new integer value for 'minlen'.

    Returns:
        str: The configuration line with the 'minlen' value replaced.
             Returns the original line if 'minlen=' is not found.
    """
    pattern = r"(minlen=)(\d+)"
    replaced_line = re.sub(pattern, r"\g<1>" + str(new_minlen), line)
    
    return replaced_line

def set_password_min_length(length: int, backup: bool = True) -> None:
    
    if backup:
        print(f"Creating a backup file")
        subprocess.run(["sudo", "cp", CONFIG_FILE, BACKUP_FILE])
    
    with open(CONFIG_FILE, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        if "minlen=" in line:
            replace_minlen_value(line, length)
            
if __name__ == "__main__":
    set_password_min_length(8)