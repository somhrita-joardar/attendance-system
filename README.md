
# RFID-Based Automated Attendance System

![Python](https://img.shields.io/badge/python-3.8+-blue)
![MySQL](https://img.shields.io/badge/database-MySQL%208.0+-brightgreen)
![RFID](https://img.shields.io/badge/hardware-RFID%20Reader-orange)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Raspberry%20Pi-lightgrey)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight **RFID-based student attendance management system** that automatically marks attendance in a MySQL database when a student taps their RFID card/tag.

The system uses a custom native module (`scanner_module`) to interface with the RFID reader hardware and updates the attendance record in real-time with the current timestamp.

Ideal for classrooms, labs, hostels, or any entry-point attendance tracking.

## Features

- Real-time scanning of RFID tags
- Automatic extraction of student roll number (`rno`)
- Instant update of attendance status to `'yes'`
- Records exact date and time using MySQL `NOW()`
- Simple, minimal dependencies
- Suitable for deployment on low-cost hardware (e.g., Raspberry Pi)


```
## Requirements

### Software
- Python 3.8 or higher
- MySQL Server (local or remote)
- `mysql-connector-python`

Install the required Python package:
```bash
pip install mysql-connector-python
```

### Hardware
- RFID Reader (e.g., MFRC522, USB HID RFID reader, or any supported by your `scanner_module`)
- Connected via USB/Serial to the host machine

### Native Module
- `scanner_module` must be a compiled shared library (.so on Linux, .dll on Windows) that exposes a `main()` function returning a string containing the scanned tag ID followed by a delimiter (e.g., `"A1B2C3D4;"`)

## Database Setup

Connect to MySQL and run:

```sql
CREATE DATABASE h2;

USE h2;

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rno VARCHAR(50) UNIQUE NOT NULL,
    attendance ENUM('yes', 'no') DEFAULT 'no',
    date_time DATETIME NULL
);

-- Insert sample student data (example)
INSERT INTO attendance (rno) VALUES ('2021001'), ('2021002'), ('2021003');
```

> Ensure each student has a unique `rno` matching their RFID tag ID.

## Configuration

Update the database connection details in `attendance_script.py` if needed:

```python
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",          # CHANGE THIS IN PRODUCTION!
    database="h2"
)
```

## Usage

1. Place the compiled `scanner_module.so` (or `.dll`) in the same directory as the script.

2. Run the script:
```bash
python attendance_script.py
```

3. When a registered student taps their RFID card:
   - The roll number is extracted
   - Attendance is marked as `'yes'`
   - Timestamp is automatically recorded

The script will print the raw scanned data for debugging.

## Security Recommendations

**Current version uses f-string SQL (simple but vulnerable if input is untrusted).**

### Improved Version (Prevent SQL Injection):

Replace the execute line with:

```python
sql = """
    UPDATE attendance 
    SET attendance = 'yes', date_time = NOW() 
    WHERE rno = %s
"""
mycursor.execute(sql, (r,))
mydb.commit()
```

Additional improvements:
- Add try-except blocks for error handling
- Prevent duplicate scans within a short time window
- Log attendance events to a file
- Use environment variables for DB credentials

## Customization Ideas

- Add a GUI (Tkinter, PyQt) for visual feedback
- Play a beep/sound on successful scan
- Send notification/email for attendance
- Generate daily attendance reports
- Support multiple entry/exit points

## Disclaimer

This project is intended for **educational and small-scale institutional use**. It is not professional-grade financial or security software. Always comply with local data privacy laws (e.g., GDPR, school policies) when handling student information.
