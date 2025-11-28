# mbg-system-backend

## Database Schema

### Anomaly Table
| Attribute | Type | Description |
|---|---|---|
| id | int | Primary Key |
| date | timestamp | |
| type | string | warning or critical |
| log_id | int | Foreign Key to Log table |
| type | string | unsyncronized, mismatch, or no_delivery |

### Inventory Table
| Attribute | Type | Description |
|---|---|---|
| id | int | Primary Key |
| warehouse_id | int | Foreign Key to Warehouse table |
| item_id | int | Foreign Key to Item table |
| quantity | int | |

### Item Table
| Attribute | Type | Description |
|---|---|---|
| id | int | Primary Key |
| name | string | |

### Kitchen Table
| Attribute | Type | Description |
|---|---|---|
| id | int | Primary Key |
| name | string | |
| desc | string | |
| warehouse_id | int | Foreign Key to Warehouse table |

### Log Table
| Attribute | Type | Description |
|---|---|---|
| id | int | Primary Key |
| timestamp | time | |
| type | string | change, leave, or enter |
| warehouse_id | int | Foreign Key to Warehouse table |
| kitchen_id | int | Foreign Key to Kitchen table |

### Menu Table
| Attribute | Type | Description |
|---|---|---|
| id | int | Primary Key |
| name | string | |
| desc | string | |

### School Table
| Attribute | Type | Description |
|---|---|---|
| id | int | Primary Key |
| name | string | |
| desc | string | |
| address | string | |
| kitchen_id | int | Foreign Key to Kitchen table |

### Warehouse Table
| Attribute | Type | Description |
|---|---|---|
| id | int | Primary Key |
| name | string | |
| desc | string | |

### Menu Item Table
| Attribute | Type | Description |
|---|---|---|
| menu_id | int | Foreign Key to Menu table |
| item_id | int | Foreign Key to Item table |
| quantity | int | |