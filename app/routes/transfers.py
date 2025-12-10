from flask import Blueprint, request, jsonify
from app import db
from app.models.log import Log

bp = Blueprint('transfers', __name__, url_prefix='/api')

def _validate_request(data, required_fields):
    """Helper function to validate incoming request data."""
    if not data:
        return {"error": "Invalid request body"}, 400
    if not all(field in data for field in required_fields) or not isinstance(data.get('items'), list):
        return {"error": "Missing or invalid required fields (source/destination/items)"}, 400
    return None, None

@bp.route('/dispatch/warehouse', methods=['POST'])
def dispatch_from_warehouse():
    """
    Logs the dispatch of one or more items from a warehouse to a kitchen.
    Expects a JSON body with source_warehouse_id, destination_kitchen_id, and an array of items.
    """
    data = request.get_json()
    error, status = _validate_request(data, ['source_warehouse_id', 'destination_kitchen_id', 'items'])
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
    Logs the receipt of one or more items at a kitchen from a warehouse.
    Expects receiving_kitchen_id, source_warehouse_id, and an array of items.
    """
    data = request.get_json()
    error, status = _validate_request(data, ['receiving_kitchen_id', 'source_warehouse_id', 'items'])
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
    Logs the dispatch of one or more items from a kitchen to a school.
    Expects source_kitchen_id, destination_school_id, and an array of items.
    """
    data = request.get_json()
    error, status = _validate_request(data, ['source_kitchen_id', 'destination_school_id', 'items'])
    if error:
        return jsonify(error), status

    newly_created_logs = []
    for item_data in data['items']:
        if not ('item_id' in item_data and 'quantity' in item_data):
            continue

        new_log = Log(
            log_type='dispatch_from_kitchen',
            kitchen_id=data['source_kitchen_id'],
            school_id=data['destination_school_id'],
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

@bp.route('/receipt/school', methods=['POST'])
def receipt_at_school():
    """
    Logs the receipt of one or more items at a school from a kitchen.
    Expects receiving_school_id, source_kitchen_id, and an array of items.
    """
    data = request.get_json()
    error, status = _validate_request(data, ['receiving_school_id', 'source_kitchen_id', 'items'])
    if error:
        return jsonify(error), status

    newly_created_logs = []
    for item_data in data['items']:
        if not ('item_id' in item_data and 'quantity' in item_data):
            continue

        new_log = Log(
            log_type='receipt_at_school',
            school_id=data['receiving_school_id'],
            kitchen_id=data['source_kitchen_id'],
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
