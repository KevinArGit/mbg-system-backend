# API Documentation

This document details the API endpoints for logging item transfers between different locations (checkpoints).

## Base URL

All endpoints are prefixed with `/api`.

---

## 1. Dispatch from Warehouse

Logs the dispatch of one or more items from a warehouse to a kitchen.

- **Endpoint:** `/api/dispatch/warehouse`
- **Method:** `POST`
- **Content-Type:** `application/json`

### Request Body

```json
{
  "source_warehouse_id": 1,
  "destination_kitchen_id": 5,
  "items": [
    { "item_id": 123, "quantity": 100 },
    { "item_id": 456, "quantity": 250 }
  ]
}
```

### Responses

- **Success (201 Created)**
  ```json
  {
    "message": "Successfully created 2 dispatch logs.",
    "log_ids": [1, 2]
  }
  ```

- **Error (400 Bad Request)**
  ```json
  {
    "error": "Missing or invalid required fields (source/destination/items)"
  }
  ```

---

## 2. Receive at Kitchen

Logs the receipt of one or more items at a kitchen, presumably from a warehouse.

- **Endpoint:** `/api/receipt/kitchen`
- **Method:** `POST`
- **Content-Type:** `application/json`

### Request Body

```json
{
  "receiving_kitchen_id": 5,
  "source_warehouse_id": 1,
  "items": [
    { "item_id": 123, "quantity": 100 },
    { "item_id": 456, "quantity": 248 }
  ]
}
```

### Responses

- **Success (201 Created)**
  ```json
  {
    "message": "Successfully created 2 receipt logs.",
    "log_ids": [3, 4]
  }
  ```

- **Error (400 Bad Request)**
  ```json
  {
    "error": "No valid items to log"
  }
  ```

---

## 3. Dispatch from Kitchen (Menu-Based)

Logs the dispatch of one or more menus from a kitchen to a school. The API will automatically "explode" the menus into their raw item components and create individual logs for each item.

- **Endpoint:** `/api/dispatch/kitchen`
- **Method:** `POST`
- **Content-Type:** `application/json`

### Request Body

```json
{
  "source_kitchen_id": 1,
  "destination_school_id": 1,
  "menus": [
    { "menu_id": 1, "quantity": 5 },
    { "menu_id": 2, "quantity": 10 }
  ]
}
```

### Responses

- **Success (201 Created)**
  ```json
  {
    "message": "Successfully created 5 item dispatch logs from menus.",
    "log_ids": [5, 6, 7, 8, 9]
  }
  ```

- **Error (400 Bad Request)**
  ```json
  {
    "error": "Missing or invalid required fields (source/destination/menus)"
  }
  ```

---

## 4. Receive at School (Menu-Based)

Logs the receipt of one or more menus at a school. The API will automatically "explode" the menus into their raw item components and create individual receipt logs for each item.

- **Endpoint:** `/api/receipt/school`
- **Method:** `POST`
- **Content-Type:** `application/json`

### Request Body

```json
{
  "receiving_school_id": 1,
  "source_kitchen_id": 1,
  "menus": [
    { "menu_id": 1, "quantity": 5 },
    { "menu_id": 2, "quantity": 9 }
  ]
}
```

### Responses

- **Success (201 Created)**
  ```json
  {
    "message": "Successfully created 5 item receipt logs from menus.",
    "log_ids": [10, 11, 12, 13, 14]
  }
  ```

- **Error (400 Bad Request)**
  ```json
  {
    "error": "No valid menu items to log"
  }
  ```
