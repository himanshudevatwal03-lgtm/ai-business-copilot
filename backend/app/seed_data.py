import datetime
import random
from sqlalchemy.orm import Session
from app.models import Customer, Product, SalesOrder, SalesOrderItem, Invoice, InventoryTransaction

CUSTOMERS_DATA = [
    {"name": "NeuralEdge Solutions", "email": "procurement@neuraledge.io", "phone": "+1-415-555-0101", "region": "North America", "segment": "Enterprise", "credit_limit": 100000.0, "status": "Active"},
    {"name": "Apex Robotics Corp", "email": "accounts@apexrobotics.com", "phone": "+1-650-555-0142", "region": "North America", "segment": "Enterprise", "credit_limit": 150000.0, "status": "Active"},
    {"name": "Quantix Logistics GmbH", "email": "finance@quantix.de", "phone": "+49-30-555-0199", "region": "Europe", "segment": "Enterprise", "credit_limit": 80000.0, "status": "Active"},
    {"name": "Pacific Telecom Ltd", "email": "billing@pacifictelecom.jp", "phone": "+81-3-555-0112", "region": "Asia Pacific", "segment": "Enterprise", "credit_limit": 120000.0, "status": "Active"},
    {"name": "BlueSky Retail Tech", "email": "ops@blueskyretail.com", "phone": "+1-206-555-0188", "region": "North America", "segment": "Mid-Market", "credit_limit": 50000.0, "status": "Active"},
    {"name": "CyberShield Labs", "email": "ap@cybershieldlabs.io", "phone": "+1-512-555-0177", "region": "North America", "segment": "Mid-Market", "credit_limit": 45000.0, "status": "Active"},
    {"name": "Titan Heavy Industries", "email": "supply@titanindustries.co.uk", "phone": "+44-20-555-0133", "region": "Europe", "segment": "Enterprise", "credit_limit": 90000.0, "status": "Delinquent"},
    {"name": "Optima Health AI", "email": "finance@optimahealth.org", "phone": "+1-617-555-0166", "region": "North America", "segment": "Enterprise", "credit_limit": 110000.0, "status": "Active"},
    {"name": "Nordic Smart Grid AS", "email": "invoice@nordicsmartgrid.no", "phone": "+47-22-555-0144", "region": "Europe", "segment": "Mid-Market", "credit_limit": 60000.0, "status": "Active"},
    {"name": "Vortex Autonomous Fleet", "email": "purchasing@vortextrans.com", "phone": "+1-408-555-0155", "region": "North America", "segment": "Enterprise", "credit_limit": 130000.0, "status": "Active"},
    {"name": "SingaTech IoT Hub", "email": "payments@singatech.sg", "phone": "+65-6555-0188", "region": "Asia Pacific", "segment": "Mid-Market", "credit_limit": 40000.0, "status": "Active"},
    {"name": "Solaria Energy Systems", "email": "procurement@solariaenergy.es", "phone": "+34-91-555-0122", "region": "Europe", "segment": "Mid-Market", "credit_limit": 35000.0, "status": "Delinquent"},
    {"name": "Metro Agritech", "email": "contact@metroagritech.com", "phone": "+1-312-555-0199", "region": "North America", "segment": "SMB", "credit_limit": 25000.0, "status": "Active"},
    {"name": "Hyperion Drone Dynamics", "email": "admin@hyperiondrones.com", "phone": "+1-858-555-0174", "region": "North America", "segment": "Enterprise", "credit_limit": 75000.0, "status": "Active"},
    {"name": "Kyoto Industrial AI", "email": "finance@kyotoai.jp", "phone": "+81-75-555-0183", "region": "Asia Pacific", "segment": "Mid-Market", "credit_limit": 55000.0, "status": "Active"},
    {"name": "Bavaria Automotive Tech", "email": "supplier@bavariauto.de", "phone": "+49-89-555-0167", "region": "Europe", "segment": "Enterprise", "credit_limit": 140000.0, "status": "Active"},
    {"name": "Aura BioMetrics", "email": "info@aurabiometrics.ch", "phone": "+41-44-555-0155", "region": "Europe", "segment": "SMB", "credit_limit": 20000.0, "status": "On-Hold"},
    {"name": "Zenith Cloud Services", "email": "billing@zenithcloud.com", "phone": "+1-703-555-0139", "region": "North America", "segment": "SMB", "credit_limit": 15000.0, "status": "Active"},
    {"name": "Atlas Smart Warehousing", "email": "ap@atlaswarehousing.com", "phone": "+1-404-555-0191", "region": "North America", "segment": "Mid-Market", "credit_limit": 50000.0, "status": "Active"},
    {"name": "InnoVision Edge Ltd", "email": "procurement@innovisionedge.co.uk", "phone": "+44-161-555-0182", "region": "Europe", "segment": "Mid-Market", "credit_limit": 65000.0, "status": "Active"}
]

PRODUCTS_DATA = [
    {"sku": "QCOM-NPU-X1", "name": "Snapdragon Edge AI Accelerator Dev Kit", "category": "Edge AI Hardware", "unit_price": 499.00, "unit_cost": 270.00, "stock_quantity": 42, "reorder_threshold": 20, "description": "High-efficiency NPU development kit for on-device inference"},
    {"sku": "QCOM-VIS-MOD", "name": "Qualcomm Vision Intelligence Core Module", "category": "Edge AI Hardware", "unit_price": 780.00, "unit_cost": 420.00, "stock_quantity": 18, "reorder_threshold": 25, "description": "Multi-camera computer vision processing unit"},
    {"sku": "IOT-IMU-600", "name": "Industrial High-Precision 6-DoF IMU", "category": "IoT Sensors", "unit_price": 85.00, "unit_cost": 38.00, "stock_quantity": 140, "reorder_threshold": 50, "description": "Vibration and orientation tracking for industrial machines"},
    {"sku": "IOT-TMP-IND", "name": "Harsh-Environment Temperature & Humidity Probe", "category": "IoT Sensors", "unit_price": 65.00, "unit_cost": 26.00, "stock_quantity": 210, "reorder_threshold": 60, "description": "Ruggedized wireless temperature telemetry sensor"},
    {"sku": "IOT-ACOU-40", "name": "Acoustic Predictive Maintenance Sensor", "category": "IoT Sensors", "unit_price": 145.00, "unit_cost": 65.00, "stock_quantity": 12, "reorder_threshold": 30, "description": "Ultrasound bearing fault detection sensor"},
    {"sku": "SW-EDGE-ENT", "name": "Edge Vision Analytics Engine - Annual Enterprise", "category": "Enterprise Software", "unit_price": 2400.00, "unit_cost": 200.00, "stock_quantity": 999, "reorder_threshold": 10, "description": "Real-time edge model deployment & telemetry license"},
    {"sku": "SW-OPT-LITE", "name": "Model Quantization & NPU Optimizer Tool", "category": "Enterprise Software", "unit_price": 1200.00, "unit_cost": 100.00, "stock_quantity": 999, "reorder_threshold": 10, "description": "Automated INT8/FP16 quantization workflow suite"},
    {"sku": "ACC-PWR-IND", "name": "Industrial 24V Din-Rail Power Supply Unit", "category": "Accessories", "unit_price": 55.00, "unit_cost": 22.00, "stock_quantity": 85, "reorder_threshold": 30, "description": "Surge-protected industrial power converter"},
    {"sku": "ACC-M12-CAB", "name": "IP67 Shielded M12 Sensor Cable Pack (5x)", "category": "Accessories", "unit_price": 45.00, "unit_cost": 15.00, "stock_quantity": 9, "reorder_threshold": 25, "description": "Heavy-duty waterproof Ethernet and signal cables"},
    {"sku": "QCOM-GW-820", "name": "Snapdragon Industrial IoT Gateway Box", "category": "Edge AI Hardware", "unit_price": 890.00, "unit_cost": 490.00, "stock_quantity": 31, "reorder_threshold": 20, "description": "Rugged fanless edge gateway with cellular 5G and NPU"},
    {"sku": "IOT-OPT-CAM", "name": "Global Shutter Machine Vision Sensor", "category": "IoT Sensors", "unit_price": 320.00, "unit_cost": 150.00, "stock_quantity": 15, "reorder_threshold": 20, "description": "High-framerate optical inspection camera"},
    {"sku": "SW-FLEET-SUB", "name": "Fleet Device Management Cloud Connector", "category": "Enterprise Software", "unit_price": 850.00, "unit_cost": 50.00, "stock_quantity": 999, "reorder_threshold": 10, "description": "Over-the-air fleet firmware & model updates"}
]

def seed_database(db: Session, force: bool = False):
    """Seed database with realistic ERP data if not already seeded."""
    if not force and db.query(Customer).count() > 0:
        return
    
    # Clean existing
    db.query(InventoryTransaction).delete()
    db.query(Invoice).delete()
    db.query(SalesOrderItem).delete()
    db.query(SalesOrder).delete()
    db.query(Product).delete()
    db.query(Customer).delete()
    db.commit()

    # Seed Customers
    customers = []
    for c_data in CUSTOMERS_DATA:
        c = Customer(**c_data)
        db.add(c)
        customers.append(c)
    db.commit()

    # Seed Products
    products = []
    for p_data in PRODUCTS_DATA:
        p = Product(**p_data)
        db.add(p)
        products.append(p)
    db.commit()

    # Seed Orders and Invoices over past 6 months
    today = datetime.date.today()
    random.seed(42) # Reproducible realistic seed
    
    order_counter = 1001
    invoice_counter = 5001

    for month_offset in range(5, -1, -1):
        # Determine month target
        # e.g., 0 = this month, 1 = 1 month ago
        # Generate 15-25 orders per month
        orders_this_month = random.randint(18, 26)
        
        # Approximate base date for the month
        base_days_ago = month_offset * 30
        
        for _ in range(orders_this_month):
            day_variation = random.randint(1, 28)
            order_date = today - datetime.timedelta(days=base_days_ago + (28 - day_variation))
            if order_date > today:
                order_date = today

            customer = random.choice(customers)
            order_number = f"SO-2026-{order_counter}"
            order_counter += 1

            # Select 1 to 4 items for this order
            item_count = random.randint(1, 4)
            chosen_products = random.sample(products, item_count)

            order_total = 0.0
            order_items = []

            for prod in chosen_products:
                qty = random.randint(1, 8) if "Software" not in prod.category else random.randint(1, 2)
                item_total = round(qty * prod.unit_price, 2)
                order_total += item_total
                order_items.append(
                    SalesOrderItem(
                        product_id=prod.id,
                        quantity=qty,
                        unit_price=prod.unit_price,
                        total_price=item_total
                    )
                )

            order = SalesOrder(
                order_number=order_number,
                customer_id=customer.id,
                order_date=order_date,
                status="Completed",
                total_amount=round(order_total, 2),
                items=order_items
            )
            db.add(order)
            db.flush()

            # Create corresponding Invoice
            due_date = order_date + datetime.timedelta(days=30)
            invoice_number = f"INV-2026-{invoice_counter}"
            invoice_counter += 1

            # Determine invoice status based on due date and customer status
            if due_date < today:
                # Past due date: either Paid or Overdue
                if customer.status == "Delinquent" or random.random() < 0.20:
                    status = "Overdue"
                    paid_amount = round(random.choice([0.0, order_total * 0.3, order_total * 0.5]), 2)
                    payment_date = None
                else:
                    status = "Paid"
                    paid_amount = round(order_total, 2)
                    payment_date = due_date - datetime.timedelta(days=random.randint(1, 10))
            else:
                # Due in the future: Pending or early Paid
                if random.random() < 0.40:
                    status = "Paid"
                    paid_amount = round(order_total, 2)
                    payment_date = order_date + datetime.timedelta(days=3)
                else:
                    status = "Pending"
                    paid_amount = 0.0
                    payment_date = None

            invoice = Invoice(
                invoice_number=invoice_number,
                order_id=order.id,
                customer_id=customer.id,
                issue_date=order_date,
                due_date=due_date,
                amount=round(order_total, 2),
                paid_amount=paid_amount,
                status=status,
                payment_date=payment_date
            )
            db.add(invoice)

    db.commit()
    print(f"Database seeded successfully: {db.query(Customer).count()} customers, {db.query(Product).count()} products, {db.query(SalesOrder).count()} orders, {db.query(Invoice).count()} invoices.")
