# Octopus Energy Technical Challenge

Django application to read the D0010 flow file and import the data in the postgres DB

### Postgres DB Setup

```
sudo apt-get update
sudo apt-get install python3.8-pip python3.8-dev libpq-dev postgresql

# During the Postgres installation, an operating system user named postgres was created to correspond to the postgres PostgreSQL administrative user. We need to change to this user to perform administrative tasks
sudo su - postgres

# You should now be in a shell session for the postgres user. Log into a Postgres session by typing
psql

# Install postgresql on mac
brew install postgresql
brew services start postgresql
psql postgres

# Create database and user
CREATE DATABASE octopus_energy_db;
CREATE USER octopus_energy_user WITH PASSWORD 'octopus_energy_password';

# Setting encodings to UTF-8, timezones and transaction isolations and grant all permissions for the created user

ALTER ROLE octopus_energy_user SET client_encoding TO 'utf8';
ALTER ROLE octopus_energy_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE octopus_energy_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE octopus_energy_db TO octopus_energy_user;

# Exit
\q
exit
```

### Project Setup

```
sudo apt-get update
sudo apt-get install python3.8-dev git
sudo apt-get install build-essential libssl-dev libffi-dev
sudo apt-get install libjpeg-dev libfreetype6-dev zlib1g-dev

sudo apt-get install virtualenv
sudo apt-get install --upgrade pip

cd octopus_energy

virtualenv --python=python3.8 venv
source venv/bin/activate

pip install -r requirements.txt
```

### Django Migrations

```bash
#Generate changed/modified scripts (use only when you change models.py file)
python manage.py makemigrations 

# Apply the changes to the physical database
python manage.py migrate

```

### Create Django Superuser

```bash
python manage.py createsuperuser 
# Create a admin user with 
username: octopus_admin
email: admin@octpusenergy.com
password: admin

```

### Run Scrapper Scripts

```bash
python scripts/import_dtc_data.py <file_name_and_path>
Example: PYTHONPATH=. python scripts/import_dtc_data.py /Users/zignite/Learning/octopus_energy/data/DTC_1.uff
```

### Run Django Project and Access Admin Portal

```bash
python manage.py runserver


Open url - http://127.0.0.1:8000/admin
Login using username: admin@octpusenergy.com and password: admin
Click on DTC data, you will see the data and you can search for the data

```