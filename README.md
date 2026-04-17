# Blood Bank Management System (Python + MySQL)

A command-line based Blood Bank Management System built using Python and MySQL. This system allows users to register, login, donate blood, request blood, and manage records with admin access.

---

## Features

- User Registration & Login (CSV + MySQL hybrid)
- Admin Panel:
  - View all records (registration, donors, patients)
  - Delete records
  - Check blood availability
- General User:
  - Donate blood
  - Request blood
  - Update personal details
- Input validation (email, phone number, blood group)
- Appointment scheduling (automatic date assignment)

---

## Tech Stack

- **Python 3**
- **MySQL**
- Libraries used:
  - `mysql-connector-python`
  - `tabulate`
  - `getpass`
  - `csv`
  - `uuid`
  - `datetime`
  - `re`

---

## Project Structure

```
bloodbank/
│
├── main.py               # Main Python source code
├── bloodusers.csv       # Stores login credentials
├── README.md            # Project documentation
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/bloodbank.git
cd bloodbank
```

---

### 2. Install Required Python Packages

```bash
pip install mysql-connector-python tabulate
```

---

### 3. Setup MySQL Database

Login to MySQL:

```bash
mysql -u root -p
```

Create database:

```sql
CREATE DATABASE bloodbank;
USE bloodbank;
```

---

### 4. Create Tables

Run the following SQL commands:

```sql
CREATE TABLE reg(
    username VARCHAR(20) PRIMARY KEY,
    password VARCHAR(20) UNIQUE,
    name VARCHAR(20),
    gender VARCHAR(10),
    DOB DATE,
    blood_grp VARCHAR(10),
    phone_no VARCHAR(50),
    email VARCHAR(50),
    address VARCHAR(30)
);

CREATE TABLE patient(
    username VARCHAR(20),
    patient_ID VARCHAR(20) PRIMARY KEY,
    unit_l DECIMAL(10,2),
    reason VARCHAR(30),
    blood_grp VARCHAR(10),
    appointment_date DATE,
    FOREIGN KEY (username) REFERENCES reg(username)
);

CREATE TABLE donor(
    username VARCHAR(20),
    donor_ID VARCHAR(20) PRIMARY KEY,
    unit_l DECIMAL(10,2),
    disease VARCHAR(30),
    blood_grp VARCHAR(10),
    appointment_date DATE,
    FOREIGN KEY (username) REFERENCES reg(username)
);
```

---

### 5. Configure Database Connection

In `main.py`, update:

```python
con = mys.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="bloodbank"
)
```

---

### 6. Run the Program

```bash
python main.py
```

---

## Default Flow

1. Register a new user
2. Login as:
   - **Admin**
   - **General User**
3. Perform operations based on role

---

## Notes

- `bloodusers.csv` stores login credentials separately from MySQL.
- Ensure MySQL server is running before executing the program.
- Passwords are stored in plain text (not secure — for educational purposes only).
- Some SQL queries use string concatenation → vulnerable to SQL injection (can be improved).

---

## Future Improvements

- Password hashing (bcrypt)
- Full MySQL-based authentication
- GUI (Tkinter / Web app)
- Better error handling
- Role-based authentication system
- SQL injection protection (prepared statements everywhere)

---

## License

This project is for educational purposes.

---
