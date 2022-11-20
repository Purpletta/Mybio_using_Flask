from datetime import datetime

SQLITE_DATABASE_NAME = "guestbook.db"
SQLITE_DATABASE_BACKUP_NAME = "guestbook_backup" + datetime.today().strftime("%Y-%m-%d") + ".db"

POST_MAX_NAME_LENGTH = 50
POST_MAX_TEXT_LENGTH = 250