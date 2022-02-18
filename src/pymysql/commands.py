from .structs import DbOperationResult as DbOperationResult
from .connection import Connection

#------------------------------------------------------
# Execute a select statement for mulitple records
#
# Args:
#   sql_stmt: sql statement to execute
#   parms: sql parms to pass to the engine
#   fetch_all: if true, fetch all records, otherwise fetch one
#------------------------------------------------------
def select(sql_stmt: str, parms: tuple=None, fetch_all: bool=True) -> DbOperationResult:
    db_result = DbOperationResult(successful=True)
    db = Connection()

    try:
        db.connect()
        cursor = db.getCursor(True)
        cursor.execute(sql_stmt, parms)

        if fetch_all:
            db_result.data = cursor.fetchall()
        else:
            db_result.data = cursor.fetchone()

    except Exception as e:
        db_result.error = e
        db_result.data = None
        db_result.successful = False
    finally:
        db.close()
    
    return db_result


#------------------------------------------------------
# Execute an insert, update, or delete sql command
#
# Args:
#   sql_stmt: sql statement to execute
#   parms: sql parms to pass to the engine
#
# Returns a DbOperationResult:
#   sets the data field to the row count
#------------------------------------------------------
def modify(sql_stmt: str, parms: tuple=None) -> DbOperationResult:
    result = DbOperationResult(successful=True)
    
    db = Connection()

    try:
        db.connect()
        cursor = db.getCursor(False)
        cursor.execute(sql_stmt, parms)
        db.commit()
        
        result.data = cursor.rowcount
    except Exception as e:
        result.error      = e
        result.successful = False
        result.data       = None
        
    finally:
        db.close()
    
    return result