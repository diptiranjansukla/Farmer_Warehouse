import re
from app.models import FarmerWarehouseCommodity

# Helper function to validate receipt format
def validate_receipt(receipt):
    """
    Validates the receipt based on specific conditions:
    - Receipt should not be empty.
    - Receipt must start with 'R-' followed by at least 4 digits.
    - Receipt must be unique in the 'FarmerWarehouseCommodity' table.
    """
    # Check if receipt is empty or only contains whitespace
    if not receipt or receipt.strip() == "":
        return False, "Receipt cannot be empty."
    
    # Check if the receipt starts with 'R-' and is followed by at least 4 digits
    if not re.match(r'^R-\d{4,}', receipt):
        return False, "Receipt must start with 'R-' followed by at least 4 digits."
    
    # Check if the receipt already exists in the FarmerWarehouseCommodity table
    existing_receipt = FarmerWarehouseCommodity.query.filter_by(farmer_warehouse_commodity_receipt=receipt).first()
    if existing_receipt:
        return False, "Receipt already exists. Please provide a unique receipt."
    
    return True, None

# Function to hash the user's password (could be used for registering new users)
from werkzeug.security import generate_password_hash

def hash_password(password):
    """
    Generates a hashed version of the password using the werkzeug security library.
    """
    return generate_password_hash(password)

# Function to verify if the provided password matches the stored hashed password
from werkzeug.security import check_password_hash

def verify_password(stored_password, provided_password):
    """
    Verifies if the provided password matches the hashed password stored in the database.
    """
    return check_password_hash(stored_password, provided_password)

