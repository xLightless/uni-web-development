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
        password:str = "password1",
        database:str = "horizon_travels"
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
        """ Returns the integer position of a table column name

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
        """ Gets a single row from a table

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
    
    def get_table_column(self, table:str, column_name:str):
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
            column (str): The column name in 'table'.
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
        
    def count_table_rows(self, table:str):
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
        
    def is_value_in_table(self, table:str, column_name:str, value:str):
        """ Checks if value is in a table already """

        # Probably an inefficient method on a large scale of table data
        # Checks if table is empty and returns False if so
        if len(self.get_table_column(table, column_name=column_name)[1]) == 0:
            return False
        else:
            # If not empty and has value return True
            for column in self.get_table_column(table, column_name=column_name)[1]:
                for row in column:
                    if str(row) == value:
                        return True

            
# db = Database()
# x = db.is_value_in_table('customer', 'email', 'lightlessgaming@gmail.com')
# print(x)