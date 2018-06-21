## EONET API

The goal of this project is
* Read data from EONET API save it to database.
* Pull data about wildfires, severe storms, and landslides from the past month to a csv file.
* Email the csv file to an email address.

The project contains 3 programs
* database.py: It will setup the database and create tables. Downloads the data from api and saves them
to db. Then extracts the required data and saves it to data.csv file.
* send_email.py: Sends the data.csv file to desired email.
* cleardb.py: Clears the database.

## Usage
run `database.py` first to setup db ,save data and generate `data.csv` file.

```python
python database.py
```

run `send_email.py` to send `data.csv` email to desired address.
```python
python send_email.py
```

## TODO
* Optimize the code and make it clean.
* Make the email content more customizable for example user should be able to pull any events.
* Research on which database is better for this project as the data grows.
* Add tests
