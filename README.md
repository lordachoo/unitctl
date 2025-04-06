# unitctl - Systemd Unit File Manager

`unitctl` is a command-line tool for creating, editing, and managing systemd unit files with an interactive menu-driven interface.

## Features

- **Create new systemd units** (services, timers, sockets)
- **Edit existing unit files** - Load and modify any systemd unit
- **Edit current unit** - Continue editing the loaded configuration
- **Save units** to `/etc/systemd/system/` with proper formatting
- **Predefined templates** for common use cases:
  - Simple Service (basic background service)
  - One-shot Service (single-run tasks)
  - Web Application (Python web service)
  - OpenVPN Client (secure VPN connection)
  - Periodic Task (timer unit)
- **Interactive validation** that checks:
  - Required fields
  - Path existence
  - User accounts
  - Systemd best practices
- **Dynamic menu** that adapts based on current state
- **Real-time preview** of current unit configuration

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

Show version:
```bash
unitctl -v
# or
unitctl --version
```

Show help:
```bash
unitctl -h
# or
unitctl --help
```

### Main Menu Options

The menu dynamically adjusts based on whether a unit is currently loaded:

**With no unit loaded:**
1. **Create new unit** - Start a new unit from scratch
2. **Edit existing unit** - Load and modify a unit file
3. **Save unit file** - Write current configuration
4. **Use template** - Start from predefined configuration
5. **Validate unit** - Check current configuration
6. **Exit** - Quit the program

**With unit loaded:**
1. **Create new unit** - Start fresh (discards current)
2. **Edit existing unit** - Load different unit file
3. **Edit current unit** - Continue editing loaded unit
4. **Save unit file** - Write current configuration
5. **Use template** - Apply template to current unit
6. **Validate unit** - Check configuration
7. **Exit** - Quit the program

**Editing Features:**
- Section-by-section editing (Unit, Service, Install, Timer)
- Add/modify/remove individual options
- Preserve all existing settings when editing
- Real-time validation feedback

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

**Create a one-shot service from template:**
```bash
sudo unitctl
# Choose 4 (Use template) → 2 (One-shot Service)
# Set unit name: setup-task
# Edit ExecStart: /usr/local/bin/setup.sh
# Choose 3 (Edit current unit) to verify settings
# Choose 6 (Validate unit) to check configuration
# Choose 4 (Save unit file) when ready
```

**Edit an existing service:**
```bash
sudo unitctl
# Choose 2 (Edit existing unit)
# Enter path: /etc/systemd/system/nginx.service
# Choose 3 (Edit current unit)
# Modify Service section as needed
# Validate and save when complete
```

**Full workflow for a timer:**
```bash
sudo unitctl
1. Create new unit → Choose Timer type
2. Set name: daily-maintenance
3. Configure timer settings
4. Validate configuration
5. Save unit file
6. Follow post-install instructions
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
