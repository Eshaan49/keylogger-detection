# Keylogger Detection Tool (Windows)

## Overview
This project is a Windows-based security tool designed to detect and block malicious keyloggers using behavior-based analysis.

Instead of relying on known malware signatures, the tool monitors running processes and identifies suspicious behavior patterns commonly used by keyloggers.

## Features
- Background process monitoring
- Behavior-based threat scoring
- Startup persistence detection
- Network activity correlation
- Automatic blocking of malicious processes
- Event logging for investigation

## Detection Logic
Each running process is evaluated based on the following behaviors:

| Behavior | Score |
|--------|-------|
| Runs from AppData or Temp | +1 |
| Continuous background CPU usage | +1 |
| Network communication | +2 |
| Startup persistence | +2 |

If the total score reaches **4 or higher**, the process is considered malicious and is blocked.

## Technologies Used
- Python
- psutil
- Windows Registry (winreg)

## How It Works
1. The tool runs silently in the background.
2. It continuously scans running processes.
3. Each process is assigned a threat score based on behavior.
4. High-risk processes are automatically terminated.
5. All actions are logged for security analysis.

## Testing
The tool was tested using a controlled dummy script that simulated keylogger-like behavior without capturing keystrokes or using real malware.

## Limitations
- Kernel-level keyloggers are not detected.
- Network detection may vary depending on system environment.
- Requires administrator privileges for best accuracy.

## Future Enhancements
- GUI dashboard
- Windows service integration
- Quarantine system
- Advanced persistence removal

## Disclaimer
This project is intended for educational and defensive security purposes only.
