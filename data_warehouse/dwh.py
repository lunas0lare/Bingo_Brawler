from data_utils import get_conn_cursor, close_conn_cursor, create_table, create_schema
from data_modification import *
from data_loading import *

conn, cur = get_conn_cursor()

create_schema('staging')
create_table("staging")

datasets = load_data(5)

insert_to_staging(conn, cur, datasets['player'], 'player')