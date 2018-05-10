# ETH-Based-AirTicket
An Ethereum-based blockchain air ticket demo.

## Usage

### Step 1: Clear the database file and turn on the testrpc.
```shell
cd ./ETH-Based-AirTicket
rm *.db
testrpc
```

### Step 2: Turn on the web server.

```shell
cd ./ETH-Based-AirTicket
FLASK_APP=main.py flask run
```

### Step 3: GUI management system and ticket checker.

```shell
python GUI_Management.py
python ticketCheacker.py
```
