import pandas as pd
from psycopg2 import pool


class NeonDatabase:
    def __init__(self, connection_string: str):

        # Create a connection pool
        self.connection_pool = pool.SimpleConnectionPool(
            1,  # Minimum number of connections in the pool
            10,  # Maximum number of connections in the pool
            connection_string,
        )

        # Check if the pool was created successfully
        if self.connection_pool:
            print("Connection pool created successfully")

    def upload_df_to_neon(self, df: pd.DataFrame):
        """
        Assumes df is constructed with scrape.
        """

        # Get a connection from the pool
        self.conn = self.connection_pool.getconn()
        # Create a cursor object
        cur = self.conn.cursor()

        # SQL query to insert data
        insert_query = """
        INSERT INTO passengers (date, control_point, identity, arrivals, departures)
        VALUES (%s, %s, %s, %s, %s)
        """

        # Iterate over DataFrame rows
        for _, row in df.iterrows():

            cur.execute(insert_query, tuple([row[i] for i in df.columns]))

        self.conn.commit()
        # Close the cursor and return the connection to the pool
        cur.close()
        self.connection_pool.putconn(self.conn)
        return

    def __del__(self):
        # Close all connections in the pool
        self.connection_pool.closeall()
