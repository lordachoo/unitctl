#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import Dict, Optional, List

class SystemdUnitCreator:
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
            print("4. Exit")
            choice = input("Select option (1-4): ").strip()
            
            if choice == '1':
                self.create_unit()
            elif choice == '2':
                self.edit_unit()
            elif choice == '3':
                self.generate_file()
            elif choice == '4':
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
        # TODO: Implement unit file parsing and editing
        print("Edit functionality not yet implemented.")

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
    creator = SystemdUnitCreator()
    creator.main_menu()
