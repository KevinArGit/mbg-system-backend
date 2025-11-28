"""
General recommendation for the models:

Primary Keys:
For consistency, it's recommended to use 'id' as the primary key for all models.

Foreign Keys:
For foreign keys, it's recommended to use the convention '{table_name}_id'.
For example, in the 'inventory' model, the foreign key to the 'warehouse' model would be 'warehouse_id'.
"""

from .anomaly import Anomaly
from .inventory import Inventory
from .item import Item
from .kitchen import Kitchen
from .log import Log
from .menu_item import MenuItem
from .menu import Menu
from .school import School
from .warehouse import Warehouse