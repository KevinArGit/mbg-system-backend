from flask import Blueprint, request, jsonify
from app import db
from app.models import School, Warehouse, Kitchen, Item, Menu, Inventory, Log, Anomaly, MenuItem
from sqlalchemy.orm import joinedload

bp = Blueprint('queries', __name__, url_prefix='/api')

def _serialize_model(model_instance):
    """A simple helper to serialize a SQLAlchemy model, handling datetimes."""
    if not model_instance:
        return None
    d = {}
    for column in model_instance.__table__.columns:
        val = getattr(model_instance, column.name)
        if hasattr(val, 'isoformat'): # Handles datetime objects
            d[column.name] = val.isoformat()
        else:
            d[column.name] = val
    return d

# --- Entity Listing & Details ---

@bp.route('/schools', methods=['GET'])
def list_schools():
    schools = School.query.all()
    return jsonify([_serialize_model(s) for s in schools])

@bp.route('/schools/<int:id>', methods=['GET'])
def get_school(id):
    school = School.query.get_or_404(id)
    return jsonify(_serialize_model(school))

@bp.route('/warehouses', methods=['GET'])
def list_warehouses():
    warehouses = Warehouse.query.all()
    return jsonify([_serialize_model(w) for w in warehouses])

@bp.route('/warehouses/<int:id>', methods=['GET'])
def get_warehouse(id):
    warehouse = Warehouse.query.get_or_404(id)
    return jsonify(_serialize_model(warehouse))

@bp.route('/kitchens', methods=['GET'])
def list_kitchens():
    kitchens = Kitchen.query.all()
    return jsonify([_serialize_model(k) for k in kitchens])

@bp.route('/kitchens/<int:id>', methods=['GET'])
def get_kitchen(id):
    kitchen = Kitchen.query.get_or_404(id)
    return jsonify(_serialize_model(kitchen))

@bp.route('/items', methods=['GET'])
def list_items():
    items = Item.query.all()
    return jsonify([_serialize_model(i) for i in items])

@bp.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(_serialize_model(item))

@bp.route('/menus', methods=['GET'])
def list_menus():
    menus = Menu.query.all()
    return jsonify([_serialize_model(m) for m in menus])

@bp.route('/menus/<int:id>', methods=['GET'])
def get_menu(id):
    menu = Menu.query.options(joinedload(Menu.menu_items).joinedload(MenuItem.item)).get_or_404(id)
    menu_data = _serialize_model(menu)
    menu_data['menu_items'] = [
        {"item_id": mi.item.id, "item_name": mi.item.name, "quantity": mi.quantity} 
        for mi in menu.menu_items
    ]
    return jsonify(menu_data)

# --- Inventory Queries ---

@bp.route('/inventory', methods=['GET'])
def list_inventory():
    query = Inventory.query
    if request.args.get('location_type'):
        query = query.filter_by(location_type=request.args.get('location_type'))
    if request.args.get('location_id'):
        query = query.filter_by(location_id=request.args.get('location_id'))
    if request.args.get('item_id'):
        query = query.filter_by(item_id=request.args.get('item_id'))
    
    inventories = query.all()
    return jsonify([_serialize_model(i) for i in inventories])

@bp.route('/inventory/<string:location_type>/<int:location_id>', methods=['GET'])
def get_inventory_for_location(location_type, location_id):
    inventory = Inventory.query.filter_by(location_type=location_type, location_id=location_id).all()
    return jsonify([_serialize_model(i) for i in inventory])

@bp.route('/inventory/<string:location_type>/<int:location_id>/<int:item_id>', methods=['GET'])
def get_inventory_item_at_location(location_type, location_id, item_id):
    inventory_item = Inventory.query.filter_by(
        location_type=location_type, location_id=location_id, item_id=item_id
    ).first_or_404()
    return jsonify(_serialize_model(inventory_item))

# --- Log & Anomaly Queries ---

@bp.route('/logs', methods=['GET'])
def list_logs():
    query = Log.query
    # Add filtering based on query parameters
    if request.args.get('log_type'):
        query = query.filter(Log.log_type == request.args.get('log_type'))
    if request.args.get('status'):
        query = query.filter(Log.status == request.args.get('status'))
    if request.args.get('item_id'):
        query = query.filter(Log.item_id == request.args.get('item_id'))
    # You can add more filters for date ranges, etc.
    
    logs = query.order_by(Log.timestamp.desc()).all()
    return jsonify([_serialize_model(l) for l in logs])

@bp.route('/logs/<int:id>', methods=['GET'])
def get_log(id):
    log = Log.query.get_or_404(id)
    return jsonify(_serialize_model(log))

@bp.route('/anomalies', methods=['GET'])
def list_anomalies():
    query = Anomaly.query
    # Add filtering
    if request.args.get('anomaly_type'):
        query = query.filter(Anomaly.anomaly_type.like(f"%{request.args.get('anomaly_type')}%"))
    if request.args.get('severity'):
        query = query.filter(Anomaly.severity == request.args.get('severity'))

    anomalies = query.order_by(Anomaly.timestamp.desc()).all()
    return jsonify([_serialize_model(a) for a in anomalies])

@bp.route('/anomalies/<int:id>', methods=['GET'])
def get_anomaly(id):
    anomaly = Anomaly.query.options(joinedload(Anomaly.log)).get_or_404(id)
    anomaly_data = _serialize_model(anomaly)
    if anomaly.log:
        anomaly_data['log'] = _serialize_model(anomaly.log)
    
    return jsonify(anomaly_data)
