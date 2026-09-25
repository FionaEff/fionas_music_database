# Fiona's Music Database

A music database for private networks.

Features:
- Add albums with various infos like release year, label and genres.
- Add tracks to every album with duration.
- Add artists with various infos like year of founding and country.
- Edit every entry individually.
- Use the Discogs API feature to automatically add tracks, information and cover image to albums.

## Discogs API Usage

Go the https://discogs.com website, look for the album you want to add to the database and find the album ID in your browser's address bar.
Add the ID to the Discogs ID field in the Add Album or Edit Album form and let the API do the rest.

## Quickstart / Local Usage

**Download the Repository**

```bash
$ git clone https://github.com/fionaeff/fionas_music_database
```

**Create a Virtual Environment and Install the Dependencies**

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

**Create an .env File in the Base Directory and Add the Required Variables**

```bash
SECRET_KEY=2344jkbb2kj34523563456lb
```

To generate a random SECRET_KEY, use the following command:

```bash
$ python3 -c "import uuid; print(uuid.uuid4().hex)"
$ echo "SECRET_KEY" = "<paste your generated key here>" > .env
```

**Initialise the SQLite Database**

```bash
$ flask db upgrade
```

**Start the Application on a Test Server**
```bash
$ flask run
```
The application runs on 127.0.0.1:5000

## Installation on a Server

**Install Base Dependencies**

```bash
$ sudo apt install -y python3 python3-venv python3-dev
$ sudo apt install -y supervisor nginx git
```

**Download the Repository to your Server**

```bash
$ git clone https://github.com/fionaeff/fionas_music_database
```

**Create a Virtual Environment and Download the Dependencies**

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

**Create an .env File in the Base Directory and Add the Required Variables**

```bash
SECRET_KEY=2344jkbb2kj34523563456lb
DATABASE_URL=mysql+pymysql://fionas_music_database:<db-password>@localhost:3306/fionas_music_database
```

To generate a random SECRET_KEY, use the following command:

```bash
$ python3 -c "import uuid; print(uuid.uuid4().hex)"
$ echo "SECRET_KEY" = "<paste your generated key here>" > .env
```

**Set up a Database**
You can use SQLite, but a production database like MySQL or PostgreSQL is recommended.
If you're using a production database, you'll need to add a DATABASE_URL variable to your .env file.
This variable will hold your database url and password.

After setting up your database, you'll need to create the tables.

```bash
$ flask db upgrade
```

**Install Gunicorn**

```bash
(venv) $ pip install gunicorn
```

Start Gunicorn using the following command:
```bash
gunicorn -b localhost:8000 -w 4 fionas_music_database:app
```

**Setting Up Supervisor**

Open /etc/supervisor/conf.d/fionas_music_database.conf and add the following:
```bash
[program:fionas_music_database]
command=/home/user/fionas_music_database/venv/bin/gunicorn -b localhost:8000 -w 4 fionas_music_database:app
directory=/home/user/fionas_music_database
user=user
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

Restart the service afterwards:
```bash
$ sudo supervisorctl reload
```

Set up Nginx, Certbot for SSL certificates and redirect your domain to the IP address of your server.

**Deploying Application Updates**

```bash
$ git pull
$ sudo supervisorctl stop fionas_music_database
$ flask db upgrade
$ sudo supervisorctl start fionas_music_database
```

# License

[MIT](https://choosealicense.com/licenses/mit/)