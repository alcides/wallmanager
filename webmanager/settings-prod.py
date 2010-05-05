from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alcides Fonseca', 'amaf@student.dei.uc.pt'),
)

MANAGERS = ADMINS

DATABASE_ENGINE='mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME='djangostack'             # Or path to database file if using sqlite3.
DATABASE_USER='bitnami'             # Not used with sqlite3.
DATABASE_PASSWORD='a23f155165'         # Not used with sqlite3.
DATABASE_HOST=''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT='3306'             # Set to empty string for default. Not used with sqlite3.