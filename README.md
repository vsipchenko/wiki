Manual for Ubuntu.

# Make sure you have installed Python 3.*:
```bash
/usr/bin/python3 --version
```

# Install pip and "virtualenv":
```bash
sudo apt update
sudo apt install python3-pip
```

# Install and create virtualenv:
```bash
sudo pip3 install virtualenv
virtualenv <env_name>
source <env_name>/bin/activate
```

# Install project dependencies:
```bash
pip install -r requirements.txt
```

# Create PostgreSQL database and user:
```bash
sudo -u postgres psql

CREATE USER <user_name> WITH password <password>;
CREATE DATABASE <db_name>;
GRANT ALL ON DATABASE <db_name> TO <user_name>;
```

# Set up all required env variables:
1. DB_NAME
2. DB_USER
3. DB_PASS
4. DB_SERVICE
5. DB_PORT
6. SECRET_KEY

SECRET_KEY can be taken from repository owner.

# Run migrations and run server:

``` bash
python manage.py migrate
python manage.py runserver
```
