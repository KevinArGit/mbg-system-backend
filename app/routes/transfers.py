from flask import Blueprint, request, jsonify
from app import db
from app.models.log import Log

bp = Blueprint('transfers', __name__, url_prefix='/api')

def _validate_request(data, required_fields, array_field):
    """Generic helper function to validate incoming request data."""
    if not data:
        return {"error": "Invalid request body"}, 400
    if not all(field in data for field in required_fields) or not isinstance(data.get(array_field), list):
        return {"error": f"Missing or invalid fields. Required: {required_fields} and a '{array_field}' array."}, 400
    return None, None

@bp.route('/dispatch/warehouse', methods=['POST'])
def dispatch_from_warehouse():
    """
    Logs the dispatch of one or more raw items from a warehouse to a kitchen.
    """
    data = request.get_json()
    error, status = _validate_request(data, ['source_warehouse_id', 'destination_kitchen_id'], 'items')
    if error:
        return jsonify(error), status

    newly_created_logs = []
    for item_data in data['items']:
        if not ('item_id' in item_data and 'quantity' in item_data):
            continue

        new_log = Log(
            log_type='dispatch_from_warehouse',
            warehouse_id=data['source_warehouse_id'],
            kitchen_id=data['destination_kitchen_id'],
            item_id=item_data['item_id'],
            current_quantity=item_data['quantity']
        )
        db.session.add(new_log)
        newly_created_logs.append(new_log)

    if not newly_created_logs:
        return jsonify({"error": "No valid items to log"}), 400

    db.session.commit()
    log_ids = [log.id for log in newly_created_logs]
    return jsonify({"message": f"Successfully created {len(log_ids)} dispatch logs.", "log_ids": log_ids}), 201

@bp.route('/receipt/kitchen', methods=['POST'])
def receipt_at_kitchen():
    """
    Logs the receipt of one or more raw items at a kitchen from a warehouse.
    """
    data = request.get_json()
    error, status = _validate_request(data, ['receiving_kitchen_id', 'source_warehouse_id'], 'items')
    if error:
        return jsonify(error), status

    newly_created_logs = []
    for item_data in data['items']:
        if not ('item_id' in item_data and 'quantity' in item_data):
            continue

        new_log = Log(
            log_type='receipt_at_kitchen',
            kitchen_id=data['receiving_kitchen_id'],
            warehouse_id=data['source_warehouse_id'],
            item_id=item_data['item_id'],
            current_quantity=item_data['quantity']
        )
        db.session.add(new_log)
        newly_created_logs.append(new_log)

    if not newly_created_logs:
        return jsonify({"error": "No valid items to log"}), 400

    db.session.commit()
    log_ids = [log.id for log in newly_created_logs]
    return jsonify({"message": f"Successfully created {len(log_ids)} receipt logs.", "log_ids": log_ids}), 201

@bp.route('/dispatch/kitchen', methods=['POST'])
def dispatch_from_kitchen():
    """
    Logs the dispatch of one or more menus from a kitchen to a school.
    "Explodes" menus into their constituent raw items.
    """
    data = request.get_json()
    error, status = _validate_request(data, ['source_kitchen_id', 'destination_school_id'], 'menus')
    if error:
        return jsonify(error), status

    from app.models.menu_item import MenuItem

    raw_items_to_log = {}
    for menu_data in data['menus']:
        if not ('menu_id' in menu_data and 'quantity' in menu_data):
            continue
        
        menu_id = menu_data['menu_id']
        menu_quantity = menu_data['quantity']
        
        recipe_items = MenuItem.query.filter_by(menu_id=menu_id).all()
        for recipe_item in recipe_items:
            total_item_quantity = menu_quantity * recipe_item.quantity
            raw_items_to_log[recipe_item.item_id] = raw_items_to_log.get(recipe_item.item_id, 0) + total_item_quantity

    if not raw_items_to_log:
        return jsonify({"error": "No valid menu items to log"}), 400

    newly_created_logs = []
    for item_id, total_quantity in raw_items_to_log.items():
        new_log = Log(
            log_type='dispatch_from_kitchen',
            kitchen_id=data['source_kitchen_id'],
            school_id=data['destination_school_id'],
            item_id=item_id,
            current_quantity=total_quantity
        )
        db.session.add(new_log)
        newly_created_logs.append(new_log)

    db.session.commit()
    log_ids = [log.id for log in newly_created_logs]
    return jsonify({"message": f"Successfully created {len(log_ids)} item dispatch logs from menus.", "log_ids": log_ids}), 201

@bp.route('/receipt/school', methods=['POST'])
def receipt_at_school():
    """
    Logs the receipt of one or more menus at a school from a kitchen.
    "Explodes" menus into their constituent raw items.
    """
    data = request.get_json()
    error, status = _validate_request(data, ['receiving_school_id', 'source_kitchen_id'], 'menus')
    if error:
        return jsonify(error), status

    from app.models.menu_item import MenuItem
    
    raw_items_to_log = {}
    for menu_data in data['menus']:
        if not ('menu_id' in menu_data and 'quantity' in menu_data):
            continue

        menu_id = menu_data['menu_id']
        menu_quantity = menu_data['quantity']

        recipe_items = MenuItem.query.filter_by(menu_id=menu_id).all()
        for recipe_item in recipe_items:
            total_item_quantity = menu_quantity * recipe_item.quantity
            raw_items_to_log[recipe_item.item_id] = raw_items_to_log.get(recipe_item.item_id, 0) + total_item_quantity
            
    if not raw_items_to_log:
        return jsonify({"error": "No valid menu items to log"}), 400

    newly_created_logs = []
    for item_id, total_quantity in raw_items_to_log.items():
        new_log = Log(
            log_type='receipt_at_school',
            school_id=data['receiving_school_id'],
            kitchen_id=data['source_kitchen_id'],
            item_id=item_id,
            current_quantity=total_quantity
        )
        db.session.add(new_log)
        newly_created_logs.append(new_log)

    db.session.commit()
    log_ids = [log.id for log in newly_created_logs]
    return jsonify({"message": f"Successfully created {len(log_ids)} item receipt logs from menus.", "log_ids": log_ids}), 201