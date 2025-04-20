#!/usr/bin/env python3
import os
import sys
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

# Windows hosts file path
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
BACKUP_DIR = Path.home() / "hosts_backups"
WEBSITES_FILE = "websites_to_block.txt"

def ensure_admin_privileges():
    """Check if the script is running with administrator privileges."""
    try:
        # Try to create a file in a protected directory
        with open(os.path.join(os.environ['SystemRoot'], 'temp.txt'), 'w') as f:
            f.write('test')
        os.remove(os.path.join(os.environ['SystemRoot'], 'temp.txt'))
    except PermissionError:
        print("This script requires administrator privileges to run.")
        print("Please run the script as administrator.")
        sys.exit(1)

def read_websites_from_file():
    """Read websites from the text file."""
    try:
        if not os.path.exists(WEBSITES_FILE):
            print(f"Warning: {WEBSITES_FILE} not found. Creating an empty file.")
            with open(WEBSITES_FILE, 'w') as f:
                pass
            return []
        
        with open(WEBSITES_FILE, 'r') as f:
            websites = [line.strip() for line in f if line.strip()]
        return websites
    except Exception as e:
        print(f"Error reading websites file: {e}")
        return []

def add_website_to_file(website):
    """Add a website to the text file."""
    try:
        websites = read_websites_from_file()
        if website not in websites:
            with open(WEBSITES_FILE, 'a') as f:
                f.write(f"{website}\n")
            print(f"Added {website} to {WEBSITES_FILE}")
            return True
        else:
            print(f"{website} is already in the list")
            return False
    except Exception as e:
        print(f"Error adding website to file: {e}")
        return False

def remove_website_from_file(website):
    """Remove a website from the text file."""
    try:
        websites = read_websites_from_file()
        if website in websites:
            websites.remove(website)
            with open(WEBSITES_FILE, 'w') as f:
                for site in websites:
                    f.write(f"{site}\n")
            print(f"Removed {website} from {WEBSITES_FILE}")
            return True
        else:
            print(f"{website} not found in the list")
            return False
    except Exception as e:
        print(f"Error removing website from file: {e}")
        return False

def create_backup():
    """Create a backup of the hosts file."""
    if not BACKUP_DIR.exists():
        BACKUP_DIR.mkdir(parents=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"hosts_backup_{timestamp}"
    
    try:
        shutil.copy2(HOSTS_PATH, backup_path)
        print(f"Backup created at: {backup_path}")
        return True
    except Exception as e:
        print(f"Failed to create backup: {e}")
        return False

def block_websites(websites):
    """Block specified websites by adding them to the hosts file."""
    try:
        with open(HOSTS_PATH, 'r') as f:
            content = f.read()
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            # Write existing content
            temp_file.write(content)
            
            # Add new entries
            for website in websites:
                if f"127.0.0.1 {website}" not in content:
                    temp_file.write(f"\n127.0.0.1 {website}")
                    print(f"Blocked: {website}")
                else:
                    print(f"Already blocked: {website}")
        
        # Replace the original file with the temporary file
        shutil.move(temp_file.name, HOSTS_PATH)
        print("Websites blocked successfully!")
        return True
    except Exception as e:
        print(f"Error blocking websites: {e}")
        return False

def unblock_websites(websites):
    """Unblock specified websites by removing them from the hosts file."""
    try:
        with open(HOSTS_PATH, 'r') as f:
            content = f.readlines()
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            for line in content:
                # Skip lines containing the websites to unblock
                if not any(f"127.0.0.1 {website}" in line for website in websites):
                    temp_file.write(line)
                else:
                    print(f"Unblocked: {line.strip().split()[-1]}")
        
        # Replace the original file with the temporary file
        shutil.move(temp_file.name, HOSTS_PATH)
        print("Websites unblocked successfully!")
        return True
    except Exception as e:
        print(f"Error unblocking websites: {e}")
        return False

def show_blocked_websites():
    """Display currently blocked websites."""
    try:
        with open(HOSTS_PATH, 'r') as f:
            content = f.readlines()
        
        blocked = []
        for line in content:
            if line.strip().startswith('127.0.0.1') and not line.strip().startswith('#'):
                blocked.append(line.strip().split()[-1])
        
        if blocked:
            print("\nCurrently blocked websites:")
            for site in blocked:
                print(f"- {site}")
        else:
            print("\nNo websites are currently blocked.")
    except Exception as e:
        print(f"Error reading hosts file: {e}")

def show_websites_in_file():
    """Display websites in the text file."""
    websites = read_websites_from_file()
    if websites:
        print("\nWebsites in the list:")
        for site in websites:
            print(f"- {site}")
    else:
        print("\nNo websites in the list.")

def main():
    ensure_admin_privileges()
    
    while True:
        print("\nWebsite Blocker Menu:")
        print("1. Block websites")
        print("2. Unblock websites")
        print("3. Show blocked websites")
        print("4. Add website to list")
        print("5. Remove website from list")
        print("6. Show websites in list")
        print("7. Block all websites from list")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ")
        
        if choice == "1":
            websites = input("Enter websites to block (comma-separated): ").strip().split(',')
            websites = [site.strip() for site in websites if site.strip()]
            if websites:
                if create_backup():
                    block_websites(websites)
        
        elif choice == "2":
            websites = input("Enter websites to unblock (comma-separated): ").strip().split(',')
            websites = [site.strip() for site in websites if site.strip()]
            if websites:
                if create_backup():
                    unblock_websites(websites)
        
        elif choice == "3":
            show_blocked_websites()
        
        elif choice == "4":
            website = input("Enter website to add to list: ").strip()
            if website:
                add_website_to_file(website)
        
        elif choice == "5":
            website = input("Enter website to remove from list: ").strip()
            if website:
                remove_website_from_file(website)
        
        elif choice == "6":
            show_websites_in_file()
        
        elif choice == "7":
            websites = read_websites_from_file()
            if websites:
                if create_backup():
                    block_websites(websites)
            else:
                print("No websites in the list to block.")
        
        elif choice == "8":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 