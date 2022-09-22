'''CRUD
    --SQLite3 with SQLAlchemy and Dataset
    --used by model to interact with data *list of dictionaries 
'''
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.exc import IntegrityError, NoSuchTableError
from game_pkg import exceptions as mvc_exc


import dataset
conn = dataset.connect('sqlite:///:memory:')
DB_name = "sqlite:///:memory:"



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
        conn.get_table(table_name, primary_id='name', primary_type='String')
        print(f"Created table {table_name} on database {DB_name}")

'''
Create
'''



def insert_char(conn, name, ac, damage, hp, to_hit, table_name):
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
                name=x['name'], 
                ac=x['ac'], 
                damage=x['damage'],
                hp=x['hp'],
                to_hit=x['to_hit']
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
    mvc_exc.ItemNotStored: if the record is not stored in the table.
    """
    table = conn.load_table(table_name)
    row = table.find_one(name=name)
    if row is not None:
        item = {'name': name, 'ac': ac, 'damage': damage, 'hp': hp, 'to_hit': to_hit}
        table.update(item, keys=['name'])
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




# '''backend list'''

# # global Martial Arts opponents list, for creating, updating, etc...
# opponent_list = list()




# # create char list


# def create_chars(game_chars):
#     global opponent_list
#     opponent_list = game_chars

# # create individual char


# def create_char(name, ac, damage, hp, to_hit):
#     global opponent_list
#     results = list(filter(lambda x: x["name"] == name, opponent_list))
#     if results:
#         raise mvc_exc.CharAlreadyStored(f"{name} already stored!")
#     else:
#         opponent_list.append({"name": name,
#                                 "ac": ac,
#                                 "damage": damage, 
#                                 "hp": hp, 
#                                 "to_hit": to_hit})

# # retrive and get char


# def read_char(name):
#     global opponent_list
#     opponents = list(filter(lambda x: x['name'] == name, opponent_list))
#     if opponents:
#         return opponents[0]
#     else:
#         raise mvc_exc.CharNotStored(
#             f"Can't read {name} because it's not stored"
#         )

# # read char list


# def read_chars():
#     global opponent_list
#     return [list_item for list_item in opponent_list]

# # update individual char


# def update_char(name, ac, damage, hp, to_hit):
#     global opponent_list
#     # Python 3.x removed tuple parameters unpacking (PEP 3113), so we have to do it manually (index_x is a tuple, index_oppponent is a list of tuples)
#     index_oppponent = list(
#         filter(lambda index_x: index_x[1]["name"]
#                == name, enumerate(opponent_list))
#     )
#     if index_oppponent:
#         i, item_to_update = index_oppponent[0][0], index_oppponent[0][1]
#         opponent_list[i] = {"name": name,
#                             "ac": ac,
#                             "damage": damage, 
#                             "hp": hp, 
#                             "to_hit": to_hit}
#     else:
#         raise mvc_exc.CharNotStored(
#             f"Can't update {name} because it's not stored"
#         )

# # delete char


# def delete_char(name):
#     global opponent_list
#     # From architect: Python 3.x removed tuple parameters unpacking (PEP 3113), so we have to do it manually (i_x is a tuple, idxs_items is a list of tuples)
#     index_oppponent = list(
#         filter(lambda index_x: index_x[1]["name"] == name, enumerate(opponent_list)))
#     if index_oppponent:
#         i, item_to_delete = index_oppponent[0][0], index_oppponent[0][1]
#         del opponent_list[i]
#     else:
#         raise mvc_exc.CharNotStored(
#             f"Can't delete {name} because it's not stored."
#         )


# # opponents: dict = [{"name": "player1", "arena_level": 1, "damage": 7, "hp": 25, "to_hit": 35,
# #                     "strength": 15, "dexterity": 15, "constitution": 15},
# #                    {"name": "master", "arena_level": 4, "damage": 50, "hp": 1000, "to_hit": 75,
# #                     "strength": 15, "dexterity": 15, "constitution": 15},
# #                    {"name": "warrior", "arena_level": 1, "damage": 5, "hp": 15, "to_hit": 25,
# #                     "strength": 15, "dexterity": 15, "constitution": 15},
# #                    {"name": "veteran", "arena_level": 2, "damage": 8,
# #                     "hp": 1000, "to_hit": 30,
# #                     "strength": 15, "dexterity": 15, "constitution": 15},
# #                    {"name": "grandmaster", "arena_level": 5,
# #                     "damage": 60, "arena_level": 1250, "to_hit": 80,
# #                     "strength": 15, "dexterity": 15, "constitution": 15},
# #                    {"name": "elite", "arena_level": 3, "damage": 15, "hp": 100, "to_hit": 35,
# #                     "strength": 15, "dexterity": 15, "constitution": 15}]

# #player_items: dict = [ {"name": "player1", "hd": 1, "damage": 7, "hp": 25, "to_hit": 35}]
