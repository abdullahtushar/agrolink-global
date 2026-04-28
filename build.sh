#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Only load seed data if the database is empty (first deploy)
echo "Checking if database needs seeding..."
python -Xutf8 manage.py shell -c "
from accounts.models import User
if not User.objects.exists():
    from django.core.management import call_command
    call_command('loaddata', 'db_backup.json')
    print('SUCCESS: Seed data loaded.')
else:
    print('SKIP: Database already has data.')
"
