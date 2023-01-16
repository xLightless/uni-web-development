import mysql.connector
import warnings
import pandas as pd

# Disables pandas sql warning
warnings.simplefilter(action='ignore', category=UserWarning)

class Database(object):
    def __init__(
        self,
        host:str = "localhost",
        user:str = "root",
        password:str = "Password1",
        database:str = "ht_database"
    ):
        """ Establish a mysql connection 

        Args:
            host (str, optional): Name or IP address of the server host - and TCP/IP port.
            user (str, optional): Name of the user to connect with. Defaults to "root".
            password (str, optional): The user's password.
            database (str, optional): The name of the database.

        """
    
        self.__db = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        
        self.cursor = self.__db.cursor()
        
    def get_table(self, table:str, dataframe:bool = False):
        """ Gets the raw table of a database. Can be used in polymorphism

        Args:
            table (str): Name of the table to display.
            dataframe (bool, optional): Display a Pandas DataFrame of 'table'. Defaults to False.

        """
        
        query = "SELECT * FROM %s;" % table
        if dataframe == False:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.__db.commit()
            return result

        dataframe = pd.read_sql_query(query, self.__db)
        df = pd.DataFrame(dataframe)
        return df
    
    def get_table_header_x(self, table:str, column_name:str):
        """ Returns the integer position and name of a table column name

        Args:
            table (str): Name of the table.
            column_name (str): Column name of 'table'

        Returns:
            tuple: (column_name, column_x)
        """
        
        # Fetches a new table result
        self.get_table(table)
        try:
            col_int = 0
            for item in self.cursor.column_names:
                col_int += 1
                if item == column_name:
                    # Set parent table header and header position int
                    head_id = item
                    head_id_int = col_int
                    return head_id,head_id_int
        except IndexError:
            pass
    
    def get_table_record(self, table:str, row:int, dataframe: bool = False):
        """ Gets a single row from a table via row number

        Args:
            table (str): Name of the table.
            row (int): The row or record index of a tuple in a table.
            dataframe (bool, optional): Display a Pandas DataFrame of 'table'. Defaults to False.

        Returns:
            tuple | DataFrame: Returns record of table.
        """
        
        query = "SELECT * FROM %s;" % table
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.__db.commit()
        if dataframe == False:
            try:
                return (result[row] if row <= len(result) else IndexError)
            except IndexError:
                return f"Invalid row/record in {table}."
        
        dataframe = pd.read_sql_query(query, self.__db)
        df = pd.DataFrame(dataframe)
        return "%s" %  df.iloc[[row]]
    
    def get_table_value_record(self, table:str, column_name:str, value:str):
        """ Gets a table record by value rather than row number

        Args:
            table (str): Name of the table.
            column_name (str): The column name in 'table'.
            value (str): The value in 'column_name' to get a record.

        Returns:
            tuple: Returns record of table.
        """
        
        try:
            query = "SELECT * FROM %s WHERE %s = '%s'" % (table, column_name, value)
            self.cursor.execute(query)
            return self.cursor.fetchall()[0]
        except IndexError:
            return f"Invalid row/record in {table}."
    
    def get_table_column(self, table:str, column_name:str) -> tuple:
        """ Gets the column header and values from a table

        Args:
            table (str): Name of the table.
            column_name|key (str): FK or PK or column name of table

        Returns:
            tuple: (column_name, column_y)
        """
        
        query = "SELECT %s FROM %s;" % (column_name, table)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if self.cursor.column_names[0] == column_name:
            return (self.cursor.column_names[0], result)
        
    def get_table_cell(self, table:str, column_name:str, row:int):
        """ Gets the unknown cell data of a column in a table

        Args:
            table (str): Name of the table.
            column_name (str): The column name in 'table'.
            row (int): The iterable row of the record.
        """
        
        query = "SELECT * FROM %s WHERE %s = %s;" % (table, column_name, row)
        self.cursor.execute(query)
        self.cursor.fetchall()
        
        # Passes stubhead into function to return column_name position as integer
        column_int = int(self.get_table_header_x(table, column_name)[1])
        
        try:
            # Gets a record from a table using the row given by the user
            record = self.get_table_record(table, row)
            
            # Uses column_int to go across the record row to find the value of a cell
            for x in range(len(record)):
                if x == column_int-1:
                    return record[x]
        except IndexError:
            pass
        
    def count_table_rows(self, table:str) -> int:
        """ Returns the total record rows in a table

        Args:
            table (str): Name of the table.

        Returns:
            int: Total number of rows in 'table'.
        """
        
        query = "SELECT * FROM %s" % table
        self.cursor.execute(query)
        self.cursor.fetchall()
        rows = int(self.cursor.rowcount)
        return rows
        
    def set_table_record(self, table:str, pk_id:int, values:tuple):
        """ Insert a new record of tuple values into a database table

        Args:
            table (str): Name of the table.
            pk_id (int): Primary key value to enter into 'table'.
            values (tuple): Tuple of values to insert into 'table'.
        """
        
        record_values = "', '".join((values))
        query = f"INSERT INTO {table} VALUES ({pk_id}, '{record_values}')"
        self.cursor.execute(query)
        self.__db.commit()
        
    def is_value_in_table(self, table:str, column_name:str, value:str) -> bool:
        """ Checks if value is in a table already """
        
        # Probably an inefficient method on a large scale of table data
        # Checks if table is empty and returns False if so        
        table_column = self.get_table_column(table, column_name=column_name)[1]
        for column in table_column:
            for row in column:
                if row == value:
                    return True if row == value else False
        # return True if row == value else False
    
    def get_table_record_y(self, table:str, column_name:str, value:str) -> tuple:
        """ Returns the integer value of a tuple row

        Args:
            table (str): Name of the table.
            column_name (str): The column name in 'table'.
            value (str): The value in 'column_name' to return integer position

        Returns:
            tuple: (record, record_y)
        """
        
        tbl = self.get_table_column(table, column_name)[1]
        row_int = 0
        for column in tbl:
            for row in column:
                row_int += 1
                if row == value:
                    # break
                    return (row, row_int)
    
    def get_map_of(self, table:str, column_name:str, value:str) -> tuple:
        """ Returns the physical table (row, col) number of f(X) -> Y.
            Can be really useful for comparing coordinates of a table to their values.

        Args:
            table (str): Name of the table.
            column_name (str): The column name in 'table'.
            value (str): The value in 'column_name' to return integer position.

        Returns:
            tuple (int, int): x and y of 'table'.
        """
        # Get table col x
        # column_name = self.get_table_header_x(table, column_name)[0]
        
        x = self.get_table_header_x(table, column_name)[1]
        y = self.get_table_record_y(table, column_name, value=value)[1]
        return (x, y)
    
    def get_key_shift_value(self, table1:str, table2:str, primary_key:str, x1:int, column_name:str, value:str, x2:int) -> str:
        """ Compare two tables to see if key values exist on both then return a value of x2

        Args:
            table1 (str): Parent table.
            table2 (str): Child table.
            primary_key (str): The key to compare.
            x1 (int): Used to get on the left or right of the parent table cell. Subtracted by default.
            x2 (int): Move left or right of the child table cell to get a value.
            column_name (str): The column_name of the child table.
            value (str): The data used to reference left or right data of the parent table.

        Returns:
            str: Child table left or right cell data
        """

        # Map cell
        table1_map = self.get_map_of(table1, column_name, value)                # (2, 1)

        # Gets the XY from a table
        table1_xy = (table1_map[0]-x1, table1_map[1])                          # PK CID  (1, 1)

        # Map XY to table2 from table1 map
        table2_map = self.get_map_of(table2, primary_key, table1_map[1])       # FK CID(6, 1)
        table2_xy = (table2_map[0], table2_map[1])

        # Check if both locations are equal then do something
        table1_head = self.get_table_header_x(table1, primary_key)[1]
        
        foreign_key = primary_key
        table2_head = self.get_table_header_x(table2, foreign_key)[1]
        
        # Checks if map(x) = table_header_x
        if ((table1_xy[0] == table1_head) and (table2_xy[0] == table2_head)):
            record = self.get_table_record(table2, table2_xy[1]-1)
            return str(record[x2])
        
    def truncate_table_data(self, table:str) -> list:
        """ Removes all records from a table """
        
        query = "TRUNCATE TABLE %s" % table
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_primary_key_record(self, table:str, pk_id):
        """ Similar to get_table_record() except uses the primary key instead of row number """
        
        query = "SHOW COLUMNS FROM %s" % table
        self.cursor.execute(query)
        pk_column_name = str(self.cursor.fetchall()[0][0])
        
        query = "SELECT * FROM %s WHERE %s = '%s'" % (table, pk_column_name, pk_id)
        
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()[0]
        except IndexError:
            return "Primary key '%s' not found in '%s'." % (pk_id, table)
    
    def get_foreign_key_record():pass
    
    def update_table_record(self, table:str, column_name:str, set_value, pk_column_name:str, pk_id:int):
        """ Update a table record by setting a new value in a single row

        Args:
            table (str): Name of the table.
            column_name (str): The column name in 'table'.
            set_value (_type_): Updates the current value to a new value.
            pk_column_name (str): Primary key column name.
            pk_id (int): Primary key column name ID.
        """
        
        query = "UPDATE %s SET %s = '%s' WHERE %s = '%s'" % (table, column_name, set_value, pk_column_name, pk_id)
        self.cursor.execute(query)
        self.__db.commit()