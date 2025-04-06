# unitctl - Systemd Unit File Manager

`unitctl` is a command-line tool for creating, editing, and managing systemd unit files with an interactive menu-driven interface.

## Features

- Create new systemd units (services, timers, sockets)
- Edit existing unit files
- Save units to `/etc/systemd/system/`
- Use predefined templates for common use cases
- Interactive configuration with validation
- View current unit configuration in menu

## Installation

```bash
chmod +x unitctl
sudo cp unitctl /usr/local/bin/
```

## Usage

Run the interactive menu:
```bash
sudo unitctl
```

### Main Menu Options

1. **Create new unit** - Start a new unit from scratch
   - Choose unit type (service, timer, socket)
   - Configure basic parameters
   - Set service-specific options

2. **Edit existing unit** - Load and modify an existing unit file
   - Parses existing unit file
   - Allows modifying any section
   - Preserves all existing settings

3. **Save unit file** - Write configuration to `/etc/systemd/system/`
   - Generates properly formatted unit file
   - Shows post-installation commands

4. **Use template** - Start from a predefined configuration
   - Simple Service (basic background service)
   - One-shot Service (single-run tasks)
   - Web Application (Python web service)
   - OpenVPN Client (secure VPN connection)
   - Periodic Task (timer unit)

5. **Exit** - Quit the program

## Templates

unitctl includes these predefined templates:

1. **Simple Service**
   - Basic background service
   - Restarts on failure
   - Runs as nobody user

2. **One-shot Service**
   - For tasks that run once
   - Remains active after completion
   - Good for initialization scripts

3. **Web Application**
   - Python web service template
   - Always restarts
   - Runs as www-data user

4. **OpenVPN Client**
   - Secure VPN connection
   - Restricted permissions
   - Automatic restart on failure

5. **Periodic Task**
   - Daily timer unit
   - Persistent across reboots
   - Activates a service unit

## Examples

Create a web application service:
```bash
sudo unitctl
# Choose 4 (Use template) → 3 (Web Application)
# Set unit name: mywebapp
# Edit configuration as needed
# Choose 3 (Save unit file)
```

Edit an existing timer:
```bash
sudo unitctl
# Choose 2 (Edit existing unit)
# Enter path: /etc/systemd/system/daily-backup.timer
# Modify settings as needed
# Choose 3 (Save unit file)
```

## Post-Installation

After saving a unit file, run:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now unit-name.type
```

## Requirements

- Python 3.6+
- systemd
- Root privileges (for saving to /etc/systemd/system/)

## License

[MIT License](LICENSE)
