from datetime import datetime, timedelta

def schedule_listings(num_items: int):
    scheduled_times = []
    now = datetime.utcnow().replace(hour=7, minute=0, second=0, microsecond=0)
    full_hours, remainder = divmod(num_items, 10)
    for hour in range(full_hours):
        for i in range(10):
            scheduled_time = now + timedelta(hours=hour) + timedelta(minutes=6 * i)
            if len(scheduled_times) % 10 == 0 and scheduled_time > now + timedelta(days=1):
                now += timedelta(days=1)
            scheduled_times.append(scheduled_time.isoformat())
            print(f"Item {hour * 10 + i + 1} scheduled for {scheduled_time.isoformat()}")
    for i in range(remainder):
        scheduled_time = now + timedelta(hours=full_hours) + timedelta(minutes=60 / remainder * i)
        if len(scheduled_times) % 10 == 0 and scheduled_time > now + timedelta(days=1):
            now += timedelta(days=1)
        scheduled_times.append(scheduled_time.isoformat())
        print(f"Item {full_hours * 10 + i + 1} scheduled for {scheduled_time.isoformat()}")
    print(scheduled_times)
    return scheduled_times