'''
General exceptions for character creation
--used in both CRUD and Controller pages
'''

class CharAlreadyStored(Exception):
    pass


class CharNotStored(Exception):
    pass

class UnsupportedDatabaseEngine(Exception):
    pass

class GameSystemExit(SystemExit(BaseException)):
    pass