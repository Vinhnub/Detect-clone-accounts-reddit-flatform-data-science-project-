from database.database_fetcher import DatabaseFetcher

oDatabase = DatabaseFetcher()
oDatabase.get_size()

oDatabase.import_from_sqlite_folder('database/data')
oDatabase.get_size()
