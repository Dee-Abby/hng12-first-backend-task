# Django Number Classification API

This is a simple Django-based API that classifies a given number based on various mathematical properties. The API determines whether the number is prime, perfect, or an Armstrong number. It also provides a fun fact about the number using the Numbers API.

## Features
- Determines if a number is **prime**, **perfect**, or **Armstrong**.
- Identifies if the number is **even** or **odd**.
- Calculates the **digit sum** of the number.
- Fetches a **fun fact** about the number from [Numbers API](http://numbersapi.com/).

---

## API Endpoint

### **GET /api/?number=<integer>**

#### **Request Example:**
```bash
GET http://localhost:8000/api/?number=3
```

#### **Response Example:**
```json
{
  "number": 3,
  "is_prime": true,
  "is_perfect": false,
  "properties": [
    "odd",
    "armstrong"
  ],
  "digit_sum": 3,
  "fun_fact": "3 is the third Heegner number."
}
```

#### **Error Response Example (Invalid Input):**
```json
{
  "number": "abc",
  "error": "Invalid input. Must be an integer."
}
```

#### **Error Response Example (Negative Number):**
```json
{
  "number": -5,
  "error": "Negative numbers are not supported !!!!!"
}
```

---

## Installation & Setup

### **1. Clone the repository**
```bash
git clone https://github.com/yourusername/django-number-api.git
cd django-number-api
```

### **2. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install dependencies**
```bash
pip install -r requirements.txt
```

### **4. Apply database migrations**
```bash
python manage.py migrate
```

### **5. Run the server**
```bash
python manage.py runserver
```

---

## Project Structure
```
fun/
│── views.py          # API logic to classify numbers
│── urls.py           # URL routes
│── __init__.py
│── ...
└── testproject/
    │── settings.py  # Django settings
    │── urls.py      # Main URL configuration
    └── wsgi.py
```

---

## Deployment
To deploy using **Gunicorn**, create a `gunicorn.conf.py` file with the following settings:

```python
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 0
preload_app = True
loglevel = "debug"
accesslog = "-"
errorlog = "-"
capture_output = True

import sys
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)
```

Run Gunicorn:
```bash
gunicorn -c gunicorn.conf.py testproject.wsgi:application
```

If using **systemd**, create `/etc/systemd/system/django-api.service`:
```ini
[Unit]
Description=Django API Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/venv/bin/gunicorn --config /path/to/gunicorn.conf.py testproject.wsgi:application
Restart=always
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Reload and restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart django-api
```

Check logs:
```bash
sudo journalctl -u django-api -f
```

---

## Contributing
If you’d like to contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin new-feature`)
5. Open a Pull Request

---

## License
This project is licensed under the **MIT License**.
