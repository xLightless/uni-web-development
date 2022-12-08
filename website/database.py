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
    ) -> str:
        """ Establish mysql connection """
    
        self.__db = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        
        self.cursor = self.__db.cursor()
        
    def get_table(self, table:str, dataframe:bool = False):
        """ Gets the raw table of a database. Can be used in polymorphism """
        
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
        """ Returns the integer position of a table column name """
        
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
        """ Gets a single row from a table """
        
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
    
    def get_table_column(self, table:str, column:str):
        """ Gets the column header and values from a table

        Args:
            table (str): table to look for
            key (str): FK or PK or column name of table

        Returns:
            tuple: (column_name, column)
        """
        
        query = "SELECT %s FROM %s;" % (column, table)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if self.cursor.column_names[0] == column:
            return (self.cursor.column_names[0], result)
        
    def get_table_cell(self, table:str, column_name:str, row:int):
        """ Gets the unknown cell data of a column in a table

        Args:
            table (str): The table to look in the database for
            column (str): The column name of table
            row (int): The iterable row of the record
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
