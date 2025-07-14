#!/bin/bash

# Get current directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Path to manage.py relative to script
PROJECT_ROOT="${SCRIPT_DIR}/../.."

# Run Django shell cleanup command
deleted_count=$(
  python3 "${PROJECT_ROOT}/manage.py" shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(orders__created_at__gte=cutoff).distinct()
count = inactive_customers.count()
inactive_customers.delete()
print(count)
"
)

if [ "$deleted_count" -gt 0 ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Deleted customers: $deleted_count"
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Deleted customers: 0"
fi >> /tmp/customer_cleanup_log.txt
