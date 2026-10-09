# Parking Management System

A parking management backend built with Python, Flask and MySQL. It allocates slots to vehicles, records entry and exit, calculates the parking fee and keeps a payment history. A browser frontend (in `frontend/`) can use the API because CORS is enabled.

## Features

- **Slot allocation:** assigns the first available slot that matches the vehicle type.
- **Duplicate-entry check:** rejects a vehicle that is already parked.
- **Automatic billing:** the fee is calculated on exit from the parking duration and the vehicle category.
- **Payment records:** every exit creates a payment entry with the chosen payment method.
- **History:** full parking records and payment history are available through the API.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask, Flask-CORS |
| Database | MySQL (`mysql-connector-python`) |
| Frontend | Web interface in `frontend/` |

## Project Structure

```
parking-system/
├── app.py          # Flask application and API routes
├── database.py     # MySQL connection and default slot setup
├── schema.sql      # MySQL table definitions
├── requirements.txt
└── frontend/       # Browser interface
```

## Slots and Rates

On the first run, 22 slots are created automatically.

| Vehicle type | Slots | Slot numbers | Rate per hour |
|--------------|-------|--------------|---------------|
| 2-Wheeler | 10 | W01 to W10 | 20 |
| 4-Wheeler | 8 | F01 to F08 | 50 |
| Heavy Vehicle | 4 | H01 to H04 | 100 |

**Billing rule:** the parking time is rounded up to the next full hour, with a minimum of 1 hour.
`amount = hours x rate for the vehicle type`

## Getting Started

### Prerequisites

- Python 3.9 or later
- MySQL Server running locally

### 1. Clone the repository

```bash
git clone https://github.com/Rehan0426/parking-system.git
cd parking-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create the database and tables

```bash
sudo mysql < schema.sql
```

This creates the `parking_system` database and the `slots`, `records` and `payments` tables.

Then create a MySQL user for the app. Replace the user name and password with your own:

````bash
sudo mysql -e "CREATE USER 'your_mysql_user'@'localhost' IDENTIFIED BY 'your_mysql_password'; GRANT ALL PRIVILEGES ON parking_system.* TO 'your_mysql_user'@'localhost';"
```

Then create a MySQL user for the app. Replace the user name and password with your own:

````bash
sudo mysql -e "CREATE USER 'your_mysql_user'@'localhost' IDENTIFIED BY 'your_mysql_password'; GRANT ALL PRIVILEGES ON parking_system.* TO 'your_mysql_user'@'localhost';"
```

### 4. Configure the database connection

The app reads its MySQL settings from environment variables, so no password is stored in the code.

```bash
export DB_USER='your_mysql_user'
export DB_USER='your_mysql_user'
export DB_PASSWORD='your_mysql_password'
# Optional, these are the defaults:
# export DB_HOST=localhost
# export DB_NAME=parking_system
```

### 5. Run the server

```bash
python app.py
```

The first run inserts the default slots. The API is then available at `http://127.0.0.1:5000`.

### 6. Open the frontend

With the server running, open `frontend/index.html` in your browser.

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/slots` | List all slots with their status |
| POST | `/entry` | Register a vehicle entry |
| POST | `/exit/<record_id>` | Register a vehicle exit and calculate the fee |
| GET | `/records` | List all parking records, newest first |
| GET | `/payments` | List all payments, newest first |

### Vehicle entry

`POST /entry`

```json
{
  "plate": "MH12AB1234",
  "type": "4-Wheeler",
  "owner": "Rahul Patil",
  "phone": "9876543210"
}
```

`plate` and `type` are required. `owner` defaults to `"Walk-in"` and `phone` is optional. The plate is stored in uppercase.

Success response:

```json
{ "message": "MH12AB1234 parked at Slot F01" }
```

Error responses (HTTP 400):

```json
{ "error": "Vehicle already parked" }
{ "error": "No 4-Wheeler slots available" }
```

### Vehicle exit

`POST /exit/<record_id>`

```json
{ "method": "Cash" }
```

`method` defaults to `"Cash"`.

Success response:

```json
{ "amount": 100, "hours": 2 }
```

If the record does not exist, the API returns HTTP 404 with `{ "error": "Record not found" }`.

## Database Design

| Table | Purpose | Key columns |
|-------|---------|-------------|
| `slots` | Parking slots and their current status | `number`, `type`, `status` |
| `records` | One row per parking session | `plate`, `slot_id`, `entry_time`, `exit_time`, `hours`, `amount` |
| `payments` | One row per completed payment | `record_id`, `amount`, `method`, `time` |

`records.slot_id` references `slots.id`, and `payments.record_id` references `records.id`.

## Known Limitations and Future Work

- Add authentication for the API.
- Prevent a parking record from being closed twice.
- Validate that the vehicle type and payment method are from a fixed list.
- Add automated tests for the entry, exit and billing logic.
- Turn off Flask debug mode for production use.

## Author

**Rehan Tamboli**
[GitHub](https://github.com/Rehan0426/) | [LinkedIn](https://www.linkedin.com/in/rehan-tamboli-812b1a32b)
