import multiprocessing

# Server Binding
bind = "0.0.0.0:8000"

# Worker Settings
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 0  # Prevent worker timeouts
preload_app = True  # Preload the app for performance

# Logging Configuration
loglevel = "debug"
accesslog = "-"  # Log access logs to stdout
errorlog = "-"  # Log error logs to stderr
capture_output = True  # Capture stdout/stderr

# Enable unbuffered output
import sys
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

