'''CRUD
    --SQLite3 with SQLAlchemy and Dataset
    --used by model to interact with data *list of dictionaries 
'''
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.exc import IntegrityError, NoSuchTableError
from game_pkg import exceptions as mvc_exc
from sqlalchemy import create_engine

import dataset
user = "postgres"
pw = "PGAADMIN"
db_type = "postgresql"
port = "5432"
hostserver = "localhost"
DB_name = "Arena"
conn_str = f"{db_type}://{user}:{pw}@{hostserver}:{port}/{DB_name}"
engine = create_engine(conn_str)






def connect_to_db(db_name=DB_name, db_engine=engine):
    """Connect to a database. Create the database if there isn't one yet.

    The database can be a SQLite DB (either a DB file or an in-memory DB), or a PostgreSQL DB. In order to connect to a PostgreSQL DB you have first to create a database, create a user, and finally grant him all necessary privileges on that database and tables.
    'postgresql://<username>:<password>@localhost:<PostgreSQL port>/<db name>'
    Note: at the moment it looks it's not possible to close a connection manually (e.g. like calling conn.close() in sqlite3).


    Parameters
    ----------
    db_name : str or None
        database name (without file extension .db)
    db_engine : str
        database engine ('sqlite' or 'postgres')

    Returns
    -------
    dataset.persistence.database.Database
        connection to a database
    """
    engines = set("postgres")
    if db_name is None:
        db_string = "sqlite:///:memory:"
        print(f"New connection to in-memory SQLite DB...")
    else:
        if db_engine == "sqlite":
            db_string = f"sqlite:///{DB_name}.db"
            print(f"New connection to SQLite DB...")
        elif db_engine == "postgres":
            db_string = \
                f"{conn_str}"
            print(f"New connection to PostgreSQL DB...")
        else:
            raise mvc_exc.UnsupportedDatabaseEngine(
                f"No database engine with this name." 
                f"Choose one of the following: {engines}")

    return dataset.connect(db_string)


def create_table(conn, table_name):
    """Load a table or create it if it doesn't exist yet.

    The function load_table can only load a table if exist, and raises a NoSuchTableError if the table does not already exist in the database.

    The function get_table either loads a table or creates it if it doesn't exist yet. The new table will automatically have an id column unless specified via optional parameter primary_id, which will be used as the primary key of the table.

    Parameters
    ----------
    table_name : str
    conn : dataset.persistence.database.Database
    """
    try:
        conn.load_table(table_name)
    except NoSuchTableError as e:
        print(f"Table {e} does not exist. It will be created now")
        conn.get_table(table_name, primary_id="name", primary_type="String")
        print(f"Created table {table_name} on database {DB_name}")

'''
Create
'''



def insert_char(conn, name, ac, damage, hp, to_hit,table_name):
    """Insert a single item in a table.

    Parameters
    ----------
    name : str
    price : float
    quantity : int
    table_name : dataset.persistence.table.Table
    conn : dataset.persistence.database.Database

    Raises
    ------
    mvc_exc.ItemAlreadyStored: if the record is already stored in the table.
    """
    table = conn.load_table(table_name)
    try:
        table.insert(dict(name=name, ac=ac, damage=damage, hp=hp, to_hit=to_hit))
    except IntegrityError as e:
        raise mvc_exc.CharAlreadyStored(
            f"{name} already stored in table {table.table.name}.\n Original Exception raised: {e}")


def insert_chars(conn, chars, table_name):
    """Insert all items in a table.

    Parameters
    ----------
    items : list
        list of dictionaries
    table_name : str
    conn : dataset.persistence.database.Database
    """
    # TODO: check what happens if 1+ records can be inserted but 1 fails
    table = conn.load_table(table_name)
    try:
        for x in chars:
            table.insert(dict(
                name=x["name"], 
                ac=x["ac"], 
                damage=x["damage"],
                hp=x["hp"],
                to_hit=x["to_hit"]
                ))
    except IntegrityError as e:
        print(f"At least one in {[x['name'] for x in chars]} was already stored in table {table.table.name}. \nOriginal Exception raised: {e}")

'''
Read chars
'''

def select_char(conn, name, table_name):
    """Select a single item in a table.

    The dataset library returns a result as an OrderedDict.

    Parameters
    ----------
    name : str
        name of the record to look for in the table
    table_name : str
    conn : dataset.persistence.database.Database

    Raises
    ------
    mvc_exc.ItemNotStored: if the record is not stored in the table.
    """
    table = conn.load_table(table_name)
    row = table.find_one(name=name)
    if row is not None:
        return dict(row)
    else:
        raise mvc_exc.CharNotStored(f"Can\'t read {name} because it\'s not stored in table {table.table.name}")


def select_all(conn, table_name):
    """Select all items in a table.

    The dataset library returns results as OrderedDicts.

    Parameters
    ----------
    table_name : str
    conn : dataset.persistence.database.Database

    Returns
    -------
    list
        list of dictionaries. Each dict is a record.
    """
    table = conn.load_table(table_name)
    rows = table.all()
    return list(map(lambda x: dict(x), rows))


'''
Update Character(s)
'''

def update_char(conn, name, ac, damage, hp, to_hit, table_name):
    """Update a single item in the table.

    Note: dataset update method is a bit counterintuitive to use. Read the docs here: https://dataset.readthedocs.io/en/latest/quickstart.html#storing-data
    Dataset has also an upsert functionality: if rows with matching keys exist they will be updated, otherwise a new row is inserted in the table.

    Parameters
    ----------
    name : str
    ac : int
    hp : int
    damage: int
    to_hit: real
    table_name : str
    conn : dataset.persistence.database.Database

    Raises
    ------
    mvc_exc.CharNotStored: if the record is not stored in the table.
    """
    table = conn.load_table(table_name)
    row = table.find_one(name=name)
    if row is not None:
        item = {"name": name, "ac": ac, "damage": damage, "hp": hp, "to_hit": to_hit}
        table.update(item, keys=["name"])
    else:
        raise mvc_exc.CharNotStored(f"Can\'t update {name} because it\'s not stored in table {table.table.name}")


''''
Delete Character
'''

def delete_char(conn, char_name, table_name):
    """Delete a single item in a table.

    Parameters
    ----------
    item_name : str
    table_name : str
    conn : dataset.persistence.database.Database

    Raises
    ------
    mvc_exc.ItemNotStored: if the record is not stored in the table.
    """
    table = conn.load_table(table_name)
    row = table.find_one(name=char_name)
    if row is not None:
        table.delete(name=char_name)
    else:
        raise mvc_exc.CharNotStored(f"Can\'t delete {char_name} because it\'s not stored in table {table.table.name}")





