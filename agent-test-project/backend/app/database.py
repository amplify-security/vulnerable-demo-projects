import logging

import pymysql
from pymysql.cursors import DictCursor

from app.config import CONFIG

logger = logging.getLogger(__name__)


def get_db_connection():
    try:
        connection = pymysql.connect(
            host=CONFIG.MYSQL_HOST(),
            port=CONFIG.MYSQL_PORT(),
            user=CONFIG.MYSQL_USER(),
            password=CONFIG.MYSQL_PASSWORD(),
            database=CONFIG.MYSQL_DATABASE(),
            cursorclass=DictCursor,
        )
        return connection
    except pymysql.Error as e:
        logger.error(f"Failed to connect to MySQL: {e}")
        exit(-1337)
