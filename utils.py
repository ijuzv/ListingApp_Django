import pandas as pd
from products.models import Vehicle
from django.contrib.auth.models import User

def import_vehicles_with_pandas(file_path):
    """
    Reads a CSV file and imports vehicle data into the database.
    """
    df = pd.read_csv(file_path)

    vehicles = []
    for _, row in df.iterrows():
        user = User.objects.get(id=row['user_id'])  # Ensure user exists
        
        vehicle = Vehicle(
            product_id=row['product_id'],
            user=user,
            brand=row['brand'],
            model_year=row['model_year'],
            fuel_type=row['fuel_type'],
            km_driven=row['km_driven'],
            title=row.get('title', ''),  # Auto-generate if blank
            description=row.get('description', ''),
            price=row['price'],
            owners=row['owners'],
            insurance=row['insurance']
        )
        vehicles.append(vehicle)

    Vehicle.objects.bulk_create(vehicles)
    print("✅ Successfully imported vehicle data!")
