from db import DataBaseHandler
from prometheus_client import start_http_server, Gauge
from settings import prom_exp_port

db_handler = DataBaseHandler()

start_http_server(int(prom_exp_port))
pglt = Gauge("page_load_time", "Avito Page loading time")