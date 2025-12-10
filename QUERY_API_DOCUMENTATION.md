# Query API Documentation

This document details the read-only `GET` API endpoints for querying data from the system.

## Base URL

All endpoints are prefixed with `/api`.

---

## 1. Entity Endpoints

For fetching lists and details of core business entities.

### Schools
- `GET /api/schools`
  - **Description:** Lists all registered schools.
- `GET /api/schools/<id>`
  - **Description:** Retrieves details for a specific school.

### Warehouses
- `GET /api/warehouses`
  - **Description:** Lists all registered warehouses.
- `GET /api/warehouses/<id>`
  - **Description:** Retrieves details for a specific warehouse.

### Kitchens
- `GET /api/kitchens`
  - **Description:** Lists all registered kitchens.
- `GET /api/kitchens/<id>`
  - **Description:** Retrieves details for a specific kitchen.

### Items
- `GET /api/items`
  - **Description:** Lists all defined inventory items.
- `GET /api/items/<id>`
  - **Description:** Retrieves details for a specific item.

### Menus
- `GET /api/menus`
  - **Description:** Lists all defined menus.
- `GET /api/menus/<id>`
  - **Description:** Retrieves details for a specific menu, including its recipe of items and quantities.
  - **Example Response:**
    ```json
    {
      "id": 1,
      "name": "Menu A",
      "desc": "A sample menu",
      "menu_items": [
        { "item_id": 101, "item_name": "Apple", "quantity": 1 },
        { "item_id": 102, "item_name": "Banana", "quantity": 2 }
      ]
    }
    ```

---

## 2. Inventory Endpoints

For checking current stock levels at different locations.

- `GET /api/inventory`
  - **Description:** Lists all inventory records.
  - **Optional Query Params:**
    - `location_type` (e.g., `kitchen`)
    - `location_id` (e.g., `1`)
    - `item_id` (e.g., `101`)
  - **Example:** `/api/inventory?location_type=kitchen&location_id=1`

- `GET /api/inventory/<location_type>/<location_id>`
  - **Description:** Returns all inventory items for a specific location.
  - **Example:** `/api/inventory/kitchen/1`

- `GET /api/inventory/<location_type>/<location_id>/<item_id>`
  - **Description:** Returns the quantity for a single item at a single location.
  - **Example:** `/api/inventory/kitchen/1/101`

---

## 3. Log & Anomaly Endpoints

For auditing transfers and viewing flagged issues.

- `GET /api/logs`
  - **Description:** Returns a list of all log entries.
  - **Optional Query Params:**
    - `log_type` (e.g., `dispatch_from_warehouse`)
    - `status` (e.g., `pending`)
    - `item_id` (e.g., `101`)

- `GET /api/logs/<id>`
  - **Description:** Returns a single detailed log entry.

- `GET /api/anomalies`
  - **Description:** Returns a list of all anomalies.
  - **Optional Query Params:**
    - `anomaly_type` (e.g., `mismatch`)
    - `severity` (e.g., `critical`)

- `GET /api/anomalies/<id>`
  - **Description:** Returns a single detailed anomaly, including the full details of the `Log` entry that triggered it.
  - **Example Response:**
    ```json
    {
      "id": 1,
      "timestamp": "2025-12-11T12:00:00",
      "anomaly_type": "mismatch_incompletedelivery",
      "severity": "critical",
      "log_id": 123,
      "expected_quantity": 100,
      "actual_quantity": 98,
      "log": {
        "id": 123,
        "timestamp": "2025-12-10T18:00:00",
        "log_type": "dispatch_from_kitchen",
        "item_id": 101,
        "current_quantity": 100,
        "status": "mismatch",
        "..." : "..."
      }
    }
    ```
