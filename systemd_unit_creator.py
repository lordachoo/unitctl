#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import Dict, Optional, List

class UnitCtl:
    def __init__(self):
        self.unit_name: str = ""
        self.unit_type: str = "service"
        self.unit_data: Dict[str, Dict[str, str]] = {
            'Unit': {},
            'Service': {},
            'Install': {},
            'Timer': {}
        }
        self.common_options = {
            'Unit': ['Description', 'After', 'Requires'],
            'Service': ['Type', 'ExecStart', 'Restart', 'User', 'WorkingDirectory'],
            'Install': ['WantedBy'],
            'Timer': ['OnCalendar', 'Persistent', 'Unit']
        }

    def main_menu(self) -> None:
        """Display main menu and handle user choices."""
        while True:
            print("\nSYSTEMD UNIT CREATOR")
            print("1. Create new unit")
            print("2. Edit existing unit")
            print("3. Generate unit file")
            print("4. Use template")
            print("5. Exit")
            choice = input("Select option (1-5): ").strip()
            
            if choice == '1':
                self.create_unit()
            elif choice == '2':
                self.edit_unit()
            elif choice == '3':
                self.generate_file()
            elif choice == '4':
                self._use_template()
            elif choice == '5':
                sys.exit(0)
            else:
                print("Invalid choice, please try again.")

    def create_unit(self) -> None:
        """Create a new systemd unit from scratch."""
        print("\nUNIT TYPE:")
        print("1. Service")
        print("2. Timer")
        print("3. Socket")
        unit_type = input("Select type (1-3): ").strip()
        
        self.unit_name = input("Unit name (without extension): ").strip()
        self.unit_data['Unit']['Description'] = input("Description: ").strip()
        
        if unit_type == '1':
            self.unit_type = 'service'
            self._configure_service()
        elif unit_type == '2':
            self.unit_type = 'timer'
            self._configure_timer()
        elif unit_type == '3':
            self.unit_type = 'socket'
            self._configure_socket()
        else:
            print("Invalid unit type selected.")
            return

    def _configure_service(self) -> None:
        """Configure service-specific options."""
        print("\nSERVICE CONFIGURATION")
        self.unit_data['Service']['Type'] = self._select_from_options(
            "Service type", ['simple', 'forking', 'oneshot', 'notify', 'dbus'])
        self.unit_data['Service']['ExecStart'] = input("ExecStart command: ").strip()
        self.unit_data['Service']['Restart'] = self._select_from_options(
            "Restart policy", ['no', 'always', 'on-success', 'on-failure', 'on-abnormal', 'on-abort', 'on-watchdog'])
        self.unit_data['Service']['User'] = input("Run as user [optional, leave blank for root]: ").strip() or "root"
        self.unit_data['Service']['WorkingDirectory'] = input("Working directory [optional]: ").strip()

    def _configure_timer(self) -> None:
        """Configure timer-specific options."""
        print("\nTIMER CONFIGURATION")
        self.unit_data['Timer']['OnCalendar'] = input("Schedule (e.g. 'daily', 'hourly', or calendar spec): ").strip()
        self.unit_data['Timer']['Persistent'] = self._select_from_options(
            "Persistent timer", ['true', 'false'])
        self.unit_data['Timer']['Unit'] = input("Service to activate (e.g. example.service): ").strip()

    def _configure_socket(self) -> None:
        """Configure socket-specific options."""
        print("\nSOCKET CONFIGURATION")
        self.unit_data['Socket']['ListenStream'] = input("Listen address (e.g. 127.0.0.1:8080): ").strip()

    def _select_from_options(self, prompt: str, options: List[str]) -> str:
        """Helper to select from predefined options."""
        print(f"\n{prompt}:")
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        while True:
            try:
                choice = int(input(f"Select {prompt} (1-{len(options)}): ").strip())
                if 1 <= choice <= len(options):
                    return options[choice-1]
                print("Invalid selection, try again.")
            except ValueError:
                print("Please enter a number.")

    def edit_unit(self) -> None:
        """Edit an existing unit file."""
        unit_path = input("Enter full path to unit file: ").strip()
        try:
            with open(unit_path, 'r') as f:
                content = f.read()
            
            # Parse the unit file
            self.unit_data = {'Unit': {}, 'Service': {}, 'Install': {}, 'Timer': {}}
            current_section = None
            
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                elif '=' in line and current_section:
                    key, value = line.split('=', 1)
                    self.unit_data[current_section][key.strip()] = value.strip()
            
            # Extract unit name and type from path
            self.unit_name = os.path.splitext(os.path.basename(unit_path))[0]
            self.unit_type = os.path.splitext(unit_path)[1][1:]
            
            print(f"\nLoaded {self.unit_name}.{self.unit_type} for editing")
            self._edit_loaded_unit()
            
        except FileNotFoundError:
            print(f"Error: File {unit_path} not found")
        except Exception as e:
            print(f"Error loading unit file: {e}")

    def _edit_loaded_unit(self) -> None:
        """Edit the currently loaded unit."""
        while True:
            print("\nEDIT UNIT")
            print("1. Edit Unit section")
            print("2. Edit Service section")
            print("3. Edit Install section")
            print("4. Edit Timer section")
            print("5. Back to main menu")
            
            choice = input("Select section to edit (1-5): ").strip()
            
            if choice == '1':
                self._edit_section('Unit')
            elif choice == '2':
                self._edit_section('Service')
            elif choice == '3':
                self._edit_section('Install')
            elif choice == '4':
                self._edit_section('Timer')
            elif choice == '5':
                break
            else:
                print("Invalid choice")

    def _edit_section(self, section: str) -> None:
        """Edit a specific section of the unit."""
        print(f"\nEDITING {section} SECTION")
        
        # Initialize section if it doesn't exist
        if section not in self.unit_data:
            self.unit_data[section] = {}
            
        print("Current values:")
        for key, value in self.unit_data[section].items():
            print(f"{key}={value}")
        
        print("\n1. Add/Modify option")
        print("2. Remove option")
        print("3. Back")
        
        choice = input("Select action (1-3): ").strip()
        
        if choice == '1':
            key = input("Option name: ").strip()
            value = input(f"Value for {key}: ").strip()
            self.unit_data[section][key] = value
        elif choice == '2':
            key = input("Option to remove: ").strip()
            if key in self.unit_data[section]:
                del self.unit_data[section][key]
            else:
                print(f"{key} not found in section")
        elif choice != '3':
            print("Invalid choice")

    def _use_template(self) -> None:
        """Use a predefined template."""
        templates = {
            '1': {
                'name': 'Simple Service',
                'type': 'service',
                'data': {
                    'Unit': {
                        'Description': 'Simple Background Service',
                        'After': 'network.target'
                    },
                    'Service': {
                        'Type': 'simple',
                        'ExecStart': '/path/to/your/command',
                        'Restart': 'on-failure',
                        'User': 'nobody',
                        'WorkingDirectory': '/tmp'
                    },
                    'Install': {
                        'WantedBy': 'multi-user.target'
                    }
                }
            },
            '2': {
                'name': 'One-shot Service',
                'type': 'service',
                'data': {
                    'Unit': {
                        'Description': 'One-time Execution Service',
                        'After': 'network.target'
                    },
                    'Service': {
                        'Type': 'oneshot',
                        'ExecStart': '/path/to/your/command',
                        'RemainAfterExit': 'yes'
                    },
                    'Install': {
                        'WantedBy': 'multi-user.target'
                    }
                }
            },
            '3': {
                'name': 'Web Application',
                'type': 'service',
                'data': {
                    'Unit': {
                        'Description': 'Web Application Service',
                        'After': 'network.target'
                    },
                    'Service': {
                        'Type': 'simple',
                        'ExecStart': '/usr/bin/python3 /path/to/app.py',
                        'Restart': 'always',
                        'User': 'www-data',
                        'WorkingDirectory': '/path/to/app'
                    },
                    'Install': {
                        'WantedBy': 'multi-user.target'
                    }
                }
            },
            '4': {
                'name': 'OpenVPN Client',
                'type': 'service',
                'data': {
                    'Unit': {
                        'Description': 'OpenVPN Client Connection',
                        'After': 'network.target'
                    },
                    'Service': {
                        'Type': 'simple',
                        'ExecStart': '/usr/sbin/openvpn --config /etc/openvpn/client.conf',
                        'Restart': 'on-failure',
                        'User': 'root',
                        'Group': 'nogroup',
                        'PrivateTmp': 'true',
                        'ProtectSystem': 'full'
                    },
                    'Install': {
                        'WantedBy': 'multi-user.target'
                    }
                }
            },
            '5': {
                'name': 'Periodic Task',
                'type': 'timer',
                'data': {
                    'Unit': {
                        'Description': 'Periodic Task Timer'
                    },
                    'Timer': {
                        'OnCalendar': 'daily',
                        'Persistent': 'true',
                        'Unit': 'example.service'
                    },
                    'Install': {
                        'WantedBy': 'timers.target'
                    }
                }
            }
        }
        
        print("\nAVAILABLE TEMPLATES:")
        for key, template in templates.items():
            print(f"{key}. {template['name']} ({template['type']})")
        
        print("\nSelect template:")
        print("1. Simple Service")
        print("2. One-shot Service") 
        print("3. Web Application")
        print("4. OpenVPN Client")
        print("5. Periodic Task")
        choice = input("Enter choice (1-5): ").strip()
        if choice in templates:
            template = templates[choice]
            self.unit_name = input(f"Unit name for {template['name']}: ").strip()
            self.unit_type = template['type']
            self.unit_data = template['data']
            print(f"\nLoaded {template['name']} template")
            self._edit_loaded_unit()
        else:
            print("Invalid template choice")

    def generate_file(self) -> None:
        """Generate the systemd unit file."""
        if not self.unit_name:
            print("No unit configured. Please create a unit first.")
            return
            
        content = []
        for section, options in self.unit_data.items():
            if options:
                content.append(f"[{section}]")
                for key, value in options.items():
                    if value:  # Only include non-empty values
                        content.append(f"{key}={value}")
                content.append("")
        
        try:
            path = Path(f"/etc/systemd/system/{self.unit_name}.{self.unit_type}")
            path.write_text("\n".join(content).strip())
            print(f"\nSuccess! Unit file created at {path}")
            print("\nRemember to run:")
            print(f"  sudo systemctl daemon-reload")
            print(f"  sudo systemctl enable {self.unit_name}.{self.unit_type}")
            print(f"  sudo systemctl start {self.unit_name}.{self.unit_type}")
        except PermissionError:
            print("\nError: Permission denied. Try running with sudo.")
        except Exception as e:
            print(f"\nError creating file: {e}")

if __name__ == "__main__":
    creator = UnitCtl()
    creator.main_menu()
