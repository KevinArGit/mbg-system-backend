from app import create_app, db
from app.models import anomaly, inventory, item, kitchen, log, menu_item, menu, school, warehouse
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Anomaly=anomaly, Inventory=inventory, Item=item, Kitchen=kitchen, Log=log, 
                MenuItem=menu_item, Menu=menu, School=school, Warehouse=warehouse)

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')):
            db.create_all()
    app.run(debug=True)
