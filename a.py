from django.utils import timezone
from datetime import datetime, timedelta

# Get current date and time
current_time = datetime.now()
print("Current Date and Time:", current_time.strftime("%Y-%m-%d %H:%M:%S"))

# Calculate the date and time 5 minutes later
later_time = current_time + timedelta(minutes=5)
print("Date and Time 5 Minutes Later:", later_time.strftime("%Y-%m-%d %H:%M:%S"))
