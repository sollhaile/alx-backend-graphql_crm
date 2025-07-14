import datetime

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_line = f"{timestamp} CRM is alive\n"
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(log_line)
