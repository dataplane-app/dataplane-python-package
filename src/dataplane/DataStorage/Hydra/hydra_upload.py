"""
DBClient: Database Client (sqlalchemy.engine.Engine or sqlalchemy.engine.Connection)
SourceFilePath: /tmp/source.xlsx (needs UploadMethod="File")
TargetTableName: /General/hello.xlxs
UploadMethod: Object or File
"""


def hydra_upload(DBClient, TargetTableName, SourceFilePath="/tmp/default.txt", UploadMethod="Object", UploadObject=""):
   
    import sqlalchemy
    import pandas as pd
    from datetime import datetime
    import csv

    # Start the timer
    start = datetime.now()

    # ====== Obtain the file from disk ======
    if UploadMethod == "File":
        df = pd.read_csv(SourceFilePath)
    else:
        df = pd.read_csv(UploadObject)
    

    df.to_sql(TargetTableName,con=DBClient,method=_psql_insert_copy)

    duration = datetime.now() - start

    return {"result":"OK", "duration": str(duration)}



def _psql_insert_copy(table, conn, keys, data_iter):
    """
    Execute SQL statement inserting data
    Parameters
    ----------
    table : pandas.io.sql.SQLTable
    conn : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
    keys : list of str
        Column names
    data_iter : Iterable that iterates the values to be inserted
    """
    from io import StringIO
    import csv
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"%s"' % (k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)
