# TicTacToe-Game
A TicTacToe Multiplayer Game built with Django,
 Django Channels and WebSocket Web Protocol

# Setup

To setup this project on your local machine:

1. Create a working directory
```console
mkdir TicTacToe
```
2. Create and activate Virtual Environment
```console
python3 -m venv venv
source venv/bin/activate
```

3. Clone the repository
```console
git clone https://github.com/DrAnonymousNet/TicTacToe-Game.git
```

4. Install Requirements
```console
pip install -r requirements.txt
```

5. Setup a Postgres Database from the terminal or PgAdmin

Windows: `psql -U postgres`
Linux: `sudo -u postgres psql`
macOS: `psql -U postgres`

```bash
CREATE DATABASE tictactoe;
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
ALTER USER postgres WITH SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE tictactoe TO postgres;
\q
```


6. Create a `.env` file and add the following environment variables




