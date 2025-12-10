# app/services/log_processor.py

from datetime import datetime, timedelta
from app import db
from app.models.log import Log
from app.models.anomaly import Anomaly
from app.models.inventory import Inventory

# Define the timeout period for a pending dispatch.
DISPATCH_TIMEOUT_HOURS = 24

# --- Configuration for Transfer Matching ---
TRANSFER_MAP = {
    ('dispatch_from_warehouse', 'receipt_at_kitchen'): ('warehouse_id', 'kitchen_id'),
    ('dispatch_from_kitchen', 'receipt_at_school'): ('kitchen_id', 'school_id'),
}
# -----------------------------------------

def _update_inventory(item_id, location_type, location_id, quantity_change):
    """
    Finds or creates an inventory record and updates its quantity.
    A positive quantity_change increases stock, a negative decreases it.
    """
    inventory = Inventory.query.filter_by(
        item_id=item_id,
        location_type=location_type,
        location_id=location_id
    ).first()

    if inventory:
        inventory.quantity += quantity_change
    else:
        inventory = Inventory(
            item_id=item_id,
            location_type=location_type,
            location_id=location_id,
            quantity=quantity_change
        )
        db.session.add(inventory)
    
    print(f"    - Inventory updated for item {item_id} at {location_type}:{location_id}. New quantity: {inventory.quantity}")

def process_pending_logs():
    """
    Main service function. Iterates through defined transfer types and processes pending logs.
    """
    print("Starting log processing service...")
    
    for (dispatch_type, receipt_type), (source_field, dest_field) in TRANSFER_MAP.items():
        print(f"Processing transfers: {dispatch_type} -> {receipt_type}")
        
        pending_dispatches = Log.query.filter(
            Log.log_type == dispatch_type,
            Log.status == 'pending'
        ).all()

        for dispatch_log in pending_dispatches:
            dispatch_source_id = getattr(dispatch_log, source_field, None)
            dispatch_dest_id = getattr(dispatch_log, dest_field, None)

            if not all([dispatch_source_id, dispatch_dest_id]):
                continue

            potential_receipts = Log.query.filter(
                Log.log_type == receipt_type,
                Log.status == 'pending',
                Log.item_id == dispatch_log.item_id,
                getattr(Log, source_field) == dispatch_source_id,
                getattr(Log, dest_field) == dispatch_dest_id,
                Log.timestamp > dispatch_log.timestamp
            ).all()
            
            dispatched_quantity = dispatch_log.current_quantity
            total_received_quantity = sum(receipt.current_quantity for receipt in potential_receipts)
            is_timed_out = datetime.utcnow() > dispatch_log.timestamp + timedelta(hours=DISPATCH_TIMEOUT_HOURS)

            if total_received_quantity == dispatched_quantity:
                # --- Perfect Match ---
                print(f"  Match found for dispatch {dispatch_log.id}. Status -> verified.")
                dispatch_log.status = 'verified'
                for receipt_log in potential_receipts:
                    receipt_log.status = 'verified'
                    receipt_log.parent_log_id = dispatch_log.id

                # --- Update Inventory ---
                # Decrement from source
                source_location_type = source_field.split('_')[0]
                _update_inventory(dispatch_log.item_id, source_location_type, dispatch_source_id, -dispatched_quantity)

                # Increment at destination
                dest_location_type = dest_field.split('_')[0]
                _update_inventory(dispatch_log.item_id, dest_location_type, dispatch_dest_id, total_received_quantity)
                # ------------------------
            
            elif total_received_quantity > dispatched_quantity:
                print(f"  Mismatch found for dispatch {dispatch_log.id} (over-delivery). Status -> mismatch.")
                _create_anomaly(dispatch_log, "mismatch_overdelivery", total_received_quantity)
                dispatch_log.status = 'mismatch'
                for receipt_log in potential_receipts:
                    receipt_log.status = 'mismatch'
                    receipt_log.parent_log_id = dispatch_log.id

            elif is_timed_out:
                if total_received_quantity < dispatched_quantity:
                    print(f"  Mismatch found for dispatch {dispatch_log.id} (incomplete_delivery). Status -> mismatch.")
                    _create_anomaly(dispatch_log, "mismatch_incompletedelivery", total_received_quantity)
                    dispatch_log.status = 'mismatch'
                    for receipt_log in potential_receipts:
                        receipt_log.status = 'mismatch'
                        receipt_log.parent_log_id = dispatch_log.id
                elif total_received_quantity == 0:
                    print(f"  Mismatch found for dispatch {dispatch_log.id} (no_delivery). Status -> mismatch.")
                    _create_anomaly(dispatch_log, "mismatch_nodelivery", 0)
                    dispatch_log.status = 'mismatch'

    db.session.commit()
    print("Log processing finished.")

def _create_anomaly(dispatch_log, anomaly_type, actual_quantity):
    """Helper function to create and save a new Anomaly."""
    anomaly = Anomaly(
        anomaly_type=anomaly_type,
        severity='critical' if 'no_delivery' in anomaly_type else 'warning',
        log_id=dispatch_log.id,
        expected_quantity=dispatch_log.current_quantity,
        actual_quantity=actual_quantity
    )
    db.session.add(anomaly)
