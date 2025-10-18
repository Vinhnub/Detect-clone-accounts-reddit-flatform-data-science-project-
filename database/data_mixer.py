from database.database_fetcher import DatabaseFetcher

oDatabase = DatabaseFetcher()

oDatabase.import_from_sqlite_folder('database/data')