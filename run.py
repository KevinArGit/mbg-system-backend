from app import create_app, db
from app.models import anomaly, inventory, item, kitchen, log, menu_item, menu, school, warehouse
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Anomaly=anomaly.Anomaly, Inventory=inventory.Inventory, Item=item.Item, Kitchen=kitchen.Kitchen, Log=log.Log, 
                MenuItem=menu_item.MenuItem, Menu=menu.Menu, School=school.School, Warehouse=warehouse.Warehouse)

@app.cli.command("process-logs")
def process_logs_command():
    """Runs the log processing service to check for anomalies."""
    from app.services import log_processor
    print("Starting log processing from CLI...")
    log_processor.process_pending_logs()
    print("Log processing from CLI finished.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
