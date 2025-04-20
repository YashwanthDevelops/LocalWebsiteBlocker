# Website Blocker

A Python-based tool that helps you stay focused by blocking distracting websites on Windows. This tool modifies the system's hosts file to redirect specified domains to localhost, effectively preventing access to those websites.

## Features

- 🔒 Block multiple websites at once
- 🔓 Unblock previously blocked websites
- 📝 Maintain a list of websites to block in a separate text file
- 🔄 Create automatic backups before making changes
- 👀 View currently blocked websites
- 🛡️ Administrator privilege verification
- 📋 Easy-to-use command-line interface

## Prerequisites

- Windows operating system
- Python 3.x
- Administrator privileges

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/WebsiteBlocker_Win.git
cd WebsiteBlocker_Win
```

2. Make sure you have Python 3.x installed on your system.

## Usage

1. Run the script with administrator privileges:
   - Right-click on `website_blocker.py`
   - Select "Run as administrator"

2. Follow the menu prompts:
   ```
   Website Blocker Menu:
   1. Block websites
   2. Unblock websites
   3. Show blocked websites
   4. Add website to list
   5. Remove website from list
   6. Show websites in list
   7. Block all websites from list
   8. Exit
   ```

3. To manage websites through the text file:
   - Edit `websites_to_block.txt` directly
   - Add one website per line
   - Use option 7 to block all websites from the list

## File Structure

- `website_blocker.py` - Main script
- `websites_to_block.txt` - List of websites to block
- `hosts_backups/` - Directory containing automatic backups of the hosts file

## How It Works

The script works by modifying the Windows hosts file (`C:\Windows\System32\drivers\etc\hosts`) to redirect specified domains to localhost (127.0.0.1). This effectively blocks access to those websites.

Before making any changes, the script:
1. Verifies administrator privileges
2. Creates a backup of the hosts file
3. Makes the requested modifications
4. Provides feedback on the operation

## Safety Features

- Automatic backups before any modification
- Administrator privilege verification
- Duplicate entry prevention
- Error handling and user feedback
- Easy restoration of blocked websites

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool modifies system files. While it includes safety features and creates backups, use it at your own risk. The author is not responsible for any issues that may arise from using this tool. 