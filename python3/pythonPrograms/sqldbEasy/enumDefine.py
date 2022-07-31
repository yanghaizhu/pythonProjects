from enum import Enum

class controlE(Enum):
    pending = 0
    run = 1

class directE(Enum):
    forward = 0
    backward = 1

class targetE(Enum):
    db = 0
    table = 1
    column = 2
    row = 3

class actionE(Enum):
    show = 0
    add = 1
    modify = 2
    delete = 3

class dbStatus(Enum):
    showTables = 0
    selectTable = 1
    addTable = 2
    showColumn = 10
    selectColumn = 11
    addColumn = 12
    modifyColumn = 13
    showRows = 20
    selectRow = 21
    insertRow = 22
    modifyRow = 23
    showDbs = 100
    selectDb = 101
    addDb = 102


