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

## 3. Dispatch from Kitchen

Logs the dispatch of one or more items from a kitchen to a school.

- **Endpoint:** `/api/dispatch/kitchen`
- **Method:** `POST`
- **Content-Type:** `application/json`

### Request Body

```json
{
  "source_kitchen_id": 5,
  "destination_school_id": 10,
  "items": [
    { "item_id": 789, "quantity": 50 }
  ]
}
```

### Responses

- **Success (201 Created)**
  ```json
  {
    "message": "Successfully created 1 dispatch logs.",
    "log_ids": [5]
  }
  ```

- **Error (400 Bad Request)**
  ```json
  {
    "error": "Missing or invalid required fields (source/destination/items)"
  }
  ```

---

## 4. Receive at School

Logs the receipt of one or more items at a school, presumably from a kitchen.

- **Endpoint:** `/api/receipt/school`
- **Method:** `POST`
- **Content-Type:** `application/json`

### Request Body

```json
{
  "receiving_school_id": 10,
  "source_kitchen_id": 5,
  "items": [
    { "item_id": 789, "quantity": 50 }
  ]
}
```

### Responses

- **Success (201 Created)**
  ```json
  {
    "message": "Successfully created 1 receipt logs.",
    "log_ids": [6]
  }
  ```

- **Error (400 Bad Request)**
  ```json
  {
    "error": "No valid items to log"
  }
  ```
