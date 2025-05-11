from flask import Flask
from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize data manager
data_manager = SQLiteDataManager(app)

# Test get_user_by_id method
with app.app_context():
    # Add a user
    user = data_manager.add_user('testuser')
    print(f"Added user: {user}")
    
    # Get the user by id
    retrieved_user = data_manager.get_user_by_id(user.id)
    print(f"Retrieved user: {retrieved_user}")
    
    # Test that the method works
    if retrieved_user:
        print("get_user_by_id method works!")
    else:
        print("get_user_by_id method failed!")