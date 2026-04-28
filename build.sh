#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Only load seed data if the database is empty (first deploy)
python manage.py shell -c "
from accounts.models import User
if not User.objects.exists():
    import subprocess
    subprocess.run(['python', 'manage.py', 'loaddata', 'db_backup.json'], check=True)
    print('Seed data loaded successfully.')
else:
    print('Database already has data, skipping loaddata.')
"
