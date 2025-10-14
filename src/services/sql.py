class SQLService: 
    def __init__(self):
        self.db = mysql.connector.connect(**db_config)