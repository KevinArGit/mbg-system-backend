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
  - **Example Response:** 
    ```json
    [
      {
        "id": 1,
        "name": "Northwood Elementary",
        "desc": "Main elementary school",
        "address": "123 Learning Lane",
        "kitchen_id": 1
      }
    ]
    ```
- `GET /api/schools/<id>`
  - **Description:** Retrieves details for a specific school.
  - **Example Response:**
    ```json
    {
      "id": 1,
      "name": "Northwood Elementary",
      "desc": "Main elementary school",
      "address": "123 Learning Lane",
      "kitchen_id": 1
    }
    ```

### Warehouses
- `GET /api/warehouses`
  - **Description:** Lists all registered warehouses.
  - **Example Response:**
    ```json
    [
      {
        "id": 1,
        "name": "Central Warehouse",
        "desc": "Primary distribution center"
      }
    ]
    ```
- `GET /api/warehouses/<id>`
  - **Description:** Retrieves details for a specific warehouse.
  - **Example Response:**
    ```json
    {
      "id": 1,
      "name": "Central Warehouse",
      "desc": "Primary distribution center"
    }
    ```

### Kitchens
- `GET /api/kitchens`
  - **Description:** Lists all registered kitchens.
  - **Example Response:**
    ```json
    [
      {
        "id": 1,
        "name": "Main Kitchen",
        "desc": "Prepares food for elementary schools",
        "warehouse_id": 1
      }
    ]
    ```
- `GET /api/kitchens/<id>`
  - **Description:** Retrieves details for a specific kitchen.
  - **Example Response:**
    ```json
    {
      "id": 1,
      "name": "Main Kitchen",
      "desc": "Prepares food for elementary schools",
      "warehouse_id": 1
    }
    ```

### Items
- `GET /api/items`
  - **Description:** Lists all defined inventory items.
  - **Example Response:**
    ```json
    [
      {
        "id": 101,
        "name": "Apple"
      },
      {
        "id": 102,
        "name": "Banana"
      }
    ]
    ```
- `GET /api/items/<id>`
  - **Description:** Retrieves details for a specific item.
  - **Example Response:**
    ```json
    {
      "id": 101,
      "name": "Apple"
    }
    ```

### Menus
- `GET /api/menus`
  - **Description:** Lists all defined menus.
  - **Example Response:**
    ```json
    [
      {
        "id": 1,
        "name": "Fruit Pack A",
        "desc": "An apple and a banana"
      }
    ]
    ```
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
  - **Optional Query Params:** `location_type`, `location_id`, `item_id`
  - **Example:** `/api/inventory?location_type=kitchen&location_id=1`
  - **Example Response:**
    ```json
    [
        {
            "id": 1,
            "location_type": "kitchen",
            "location_id": 1,
            "item_id": 101,
            "quantity": 50
        }
    ]
    ```

- `GET /api/inventory/<location_type>/<location_id>`
  - **Description:** Returns all inventory items for a specific location.
  - **Example:** `/api/inventory/kitchen/1`
  - **Example Response:**
    ```json
    [
        {
            "id": 1,
            "location_type": "kitchen",
            "location_id": 1,
            "item_id": 101,
            "quantity": 50
        },
        {
            "id": 2,
            "location_type": "kitchen",
            "location_id": 1,
            "item_id": 102,
            "quantity": 120
        }
    ]
    ```

- `GET /api/inventory/<location_type>/<location_id>/<item_id>`
  - **Description:** Returns the quantity for a single item at a single location.
  - **Example:** `/api/inventory/kitchen/1/101`
  - **Example Response:**
    ```json
    {
        "id": 1,
        "location_type": "kitchen",
        "location_id": 1,
        "item_id": 101,
        "quantity": 50
    }
    ```

---

## 3. Log & Anomaly Endpoints

For auditing transfers and viewing flagged issues.

- `GET /api/logs`
  - **Description:** Returns a list of all log entries.
  - **Optional Query Params:** `log_type`, `status`, `item_id`
  - **Example Response:**
    ```json
    [
        {
            "id": 1,
            "timestamp": "2025-12-11T10:00:00",
            "log_type": "dispatch_from_warehouse",
            "item_id": 101,
            "warehouse_id": 1,
            "kitchen_id": 1,
            "school_id": null,
            "previous_quantity": null,
            "current_quantity": 100,
            "status": "verified",
            "parent_log_id": null
        }
    ]
    ```

- `GET /api/logs/<id>`
  - **Description:** Returns a single detailed log entry.
  - **Example Response:**
    ```json
    {
        "id": 1,
        "timestamp": "2025-12-11T10:00:00",
        "log_type": "dispatch_from_warehouse",
        "item_id": 101,
        "warehouse_id": 1,
        "kitchen_id": 1,
        "school_id": null,
        "previous_quantity": null,
        "current_quantity": 100,
        "status": "verified",
        "parent_log_id": null
    }
    ```

- `GET /api/anomalies`
  - **Description:** Returns a list of all anomalies.
  - **Optional Query Params:** `anomaly_type`, `severity`
  - **Example Response:**
    ```json
    [
        {
            "id": 1,
            "timestamp": "2025-12-11T12:00:00",
            "anomaly_type": "mismatch_incompletedelivery",
            "severity": "critical",
            "log_id": 123,
            "expected_quantity": 100,
            "actual_quantity": 98
        }
    ]
    ```

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
