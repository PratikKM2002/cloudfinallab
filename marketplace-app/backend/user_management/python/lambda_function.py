

# import json
# import pymysql
# import os
# import hashlib

# # Get environment variables for RDS connection
# DB_HOST = os.getenv('RDS_HOST')
# DB_USER = os.getenv('RDS_USERNAME')
# DB_PASSWORD = os.getenv('RDS_PASSWORD')
# DB_NAME = os.getenv('RDS_DB_NAME')

# # Function to hash passwords using SHA256
# def hash_password(password):
#     return hashlib.sha256(password.encode('utf-8')).hexdigest()

# # Establish a database connection
# def connect_to_db():
#     try:
#         print(f"Connecting to database at {DB_HOST}")
#         connection = pymysql.connect(
#             host=DB_HOST,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             database=DB_NAME
#         )
#         print("Successfully connected to the database.")
#         return connection
#     except Exception as e:
#         print(f"Error connecting to the database: {e}")
#         raise e

# def lambda_handler(event, context):
#     try:
#         print(f"Received event: {json.dumps(event)}")  # Log the entire event for debugging

#         # Handle POST method: Add user or product
#         if event.get('httpMethod') == 'POST':
#             body = json.loads(event.get('body', '{}'))  # Safely load body, default to empty dict

#             # Check if it's a user or product request
#             if 'username' in body and 'password' in body:
#                 # Handle adding a user
#                 username = body.get('username')
#                 password = body.get('password')

#                 if not username or not password:
#                     print(f"Missing username or password. Username: {username}, Password: {password}")
#                     return {
#                         'statusCode': 400,
#                         'body': json.dumps({'message': 'Invalid request. Username and password are required.'})
#                     }

#                 # Hash the password before storing it
#                 hashed_password = hash_password(password)
#                 print(f"Hashed password: {hashed_password}")  # Log the hashed password

#                 # Insert the user into the database
#                 connection = connect_to_db()
#                 with connection.cursor() as cursor:
#                     sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
#                     cursor.execute(sql, (username, hashed_password))
#                     connection.commit()

#                 return {
#                     'statusCode': 200,
#                     'body': json.dumps({'message': 'User added successfully'})
#                 }

#             elif 'product_name' in body and 'product_price' in body:
#                 # Handle adding a product
#                 product_name = body.get('product_name')
#                 product_price = body.get('product_price')

#                 if not product_name or not product_price:
#                     print(f"Missing product name or price. Product name: {product_name}, Price: {product_price}")
#                     return {
#                         'statusCode': 400,
#                         'body': json.dumps({'message': 'Invalid request. Product name and price are required.'})
#                     }

#                 # Insert the product into the database
#                 connection = connect_to_db()
#                 with connection.cursor() as cursor:
#                     sql = "INSERT INTO products (product_name, price) VALUES (%s, %s)"
#                     cursor.execute(sql, (product_name, product_price))

#                     connection.commit()


# import json
# import pymysql
# import os
# import hashlib

# # Get environment variables for RDS connection
# DB_HOST = os.getenv('RDS_HOST')
# DB_USER = os.getenv('RDS_USERNAME')
# DB_PASSWORD = os.getenv('RDS_PASSWORD')
# DB_NAME = os.getenv('RDS_DB_NAME')

# # Function to hash passwords using SHA256
# def hash_password(password):
#     return hashlib.sha256(password.encode('utf-8')).hexdigest()

# # Establish a database connection
# def connect_to_db():
#     try:
#         print(f"Connecting to database at {DB_HOST}")
#         connection = pymysql.connect(
#             host=DB_HOST,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             database=DB_NAME
#         )
#         print("Successfully connected to the database.")
#         return connection
#     except Exception as e:
#         print(f"Error connecting to the database: {e}")
#         raise e

# def lambda_handler(event, context):
#     try:
#         print(f"Received event: {json.dumps(event)}")  # Log the entire event for debugging

#         # Handle POST method: Add product
#         if event.get('httpMethod') == 'POST':
#             body = json.loads(event.get('body', '{}'))  # Safely load body, default to empty dict
#             product_name = body.get('product_name')
#             product_price = body.get('product_price')

#             if not product_name or not product_price:
#                 print(f"Missing product_name or product_price. Product name: {product_name}, Product price: {product_price}")
#                 return {
#                     'statusCode': 400,
#                     'body': json.dumps({'message': 'Invalid request. Product name and price are required.'})
#                 }

#             # Insert the product into the database
#             connection = connect_to_db()
#             with connection.cursor() as cursor:
#                 sql = "INSERT INTO products (product_name, price) VALUES (%s, %s)"
#                 cursor.execute(sql, (product_name, product_price))
#                 connection.commit()

#             return {
#                 'statusCode': 200,
#                 'body': json.dumps({'message': 'Product added successfully'})
#             }

#         # Handle GET method: Authenticate user or view product
#         elif event.get('httpMethod') == 'GET':
#             query_params = event.get('queryStringParameters', {})
#             if 'username' in query_params and 'password' in query_params:
#                 # User Authentication Logic
#                 username = query_params.get('username')
#                 password = query_params.get('password')

#                 print(f"Received GET request for authentication. Username: {username}, Password: {password}")

#                 if not username or not password:
#                     return {
#                         'statusCode': 400,
#                         'body': json.dumps({'message': 'Invalid request. Username and password are required.'})
#                     }

#                 # Hash the provided password
#                 hashed_password = hash_password(password)
#                 print(f"Hashed input password: {hashed_password}")

#                 # Authenticate the user
#                 connection = connect_to_db()
#                 with connection.cursor() as cursor:
#                     sql = "SELECT COUNT(*) FROM users WHERE username = %s AND password = %s"
#                     cursor.execute(sql, (username, hashed_password))
#                     result = cursor.fetchone()

#                 if result[0] > 0:
#                     return {
#                         'statusCode': 200,
#                         'body': json.dumps({'message': 'Authentication successful'})
#                     }
#                 else:
#                     return {
#                         'statusCode': 401,
#                         'body': json.dumps({'message': 'Authentication failed'})
#                     }

#             elif 'product_name' in query_params:
#                 # Product Viewing Logic
#                 product_name = query_params.get('product_name')

#                 print(f"Received GET request to view product. Product name: {product_name}")

#                 # Fetch the product details from the database
#                 connection = connect_to_db()
#                 with connection.cursor() as cursor:
#                     sql = "SELECT product_name, price FROM products WHERE product_name = %s"
#                     cursor.execute(sql, (product_name,))
#                     product = cursor.fetchone()

#                 if product:
#                     return {
#                         'statusCode': 200,
#                         'body': json.dumps({'product_name': product[0], 'price': float(product[1])})
#                     }
#                 else:
#                     return {
#                         'statusCode': 404,
#                         'body': json.dumps({'message': 'Product not found'})
#                     }

#             else:
#                 return {
#                     'statusCode': 400,
#                     'body': json.dumps({'message': 'Invalid request. Product name or username/password is required.'})
#                 }

#         # Handle DELETE method: Remove user or product
#         elif event.get('httpMethod') == 'DELETE':
#             body = json.loads(event.get('body', '{}'))  # Safely load body, default to empty dict
#             username = body.get('username')
#             product_name = body.get('product_name')

#             # Remove user from the database
#             if username:
#                 connection = connect_to_db()
#                 with connection.cursor() as cursor:
#                     sql = "DELETE FROM users WHERE username = %s"
#                     cursor.execute(sql, (username,))
#                     connection.commit()

#                 return {
#                     'statusCode': 200,
#                     'body': json.dumps({'message': 'User removed successfully'})
#                 }

#             # Remove product from the database
#             elif product_name:
#                 connection = connect_to_db()
#                 with connection.cursor() as cursor:
#                     sql = "DELETE FROM products WHERE product_name = %s"
#                     cursor.execute(sql, (product_name,))
#                     connection.commit()

#                 return {
#                     'statusCode': 200,
#                     'body': json.dumps({'message': 'Product removed successfully'})
#                 }

#             else:
#                 return {
#                     'statusCode': 400,
#                     'body': json.dumps({'message': 'Invalid request. Username or product_name is required.'})
#                 }

#         # Handle unsupported HTTP methods
#         else:
#             return {
#                 'statusCode': 405,
#                 'body': json.dumps({'message': 'Method not allowed'})
#             }

#     except Exception as e:
#         print(f"Error: {e}")
#         return {
#             'statusCode': 500,
#             'body': json.dumps({'message': 'Internal server error'})
#         }
#     finally:
#         if 'connection' in locals() and connection.open:
#             connection.close()






# import json
# import pymysql
# import os
# import hashlib

# # Get environment variables for RDS connection
# DB_HOST = os.getenv('RDS_HOST')
# DB_USER = os.getenv('RDS_USERNAME')
# DB_PASSWORD = os.getenv('RDS_PASSWORD')
# DB_NAME = os.getenv('RDS_DB_NAME')

# # Function to hash passwords using SHA256
# def hash_password(password):
#     return hashlib.sha256(password.encode('utf-8')).hexdigest()

# # Establish a database connection
# def connect_to_db():
#     try:
#         print(f"Connecting to database at {DB_HOST}")
#         connection = pymysql.connect(
#             host=DB_HOST,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             database=DB_NAME
#         )
#         print("Successfully connected to the database.")
#         return connection
#     except Exception as e:
#         print(f"Error connecting to the database: {e}")
#         raise e

# def lambda_handler(event, context):
#     try:
#         print(f"Received event: {json.dumps(event)}")  # Log the entire event for debugging

#         # Handle POST method: Add product
#         if event.get('httpMethod') == 'POST':
#             body = json.loads(event.get('body', '{}'))  # Safely load body, default to empty dict
#             product_name = body.get('product_name')
#             product_price = body.get('product_price')

#             if not product_name or not product_price:
#                 print(f"Missing product_name or product_price. Product name: {product_name}, Product price: {product_price}")
#                 return {
#                     'statusCode': 400,
#                     'body': json.dumps({'message': 'Invalid request. Product name and price are required.'})
#                 }

#             # Insert the product into the database
#             connection = connect_to_db()
#             with connection.cursor() as cursor:
#                 sql = "INSERT INTO products (product_name, price) VALUES (%s, %s)"
#                 cursor.execute(sql, (product_name, product_price))
#                 connection.commit()

#             return {
#                 'statusCode': 200,
#                 'body': json.dumps({'message': 'Product added successfully'})
#                 'headers': {
#         'Access-Control-Allow-Origin': '*',  # Allow all origins or your specific domain
#         'Access-Control-Allow-Methods': 'GET, POST, DELETE',
#         'Access-Control-Allow-Headers': 'Content-Type',
#     }
#                 'headers': {
#         'Access-Control-Allow-Origin': '*',  # Allow all origins or your specific domain
#         'Access-Control-Allow-Methods': 'GET, POST, DELETE',
#         'Access-Control-Allow-Headers': 'Content-Type',
#     }
#             }

#         # Handle GET method: Authenticate user or view product
#         elif event.get('httpMethod') == 'GET':
#             query_params = event.get('queryStringParameters', {})
#             if 'username' in query_params and 'password' in query_params:
#                 # User Authentication Logic
#                 username = query_params.get('username')
#                 password = query_params.get('password')

#                 print(f"Received GET request for authentication. Username: {username}, Password: {password}")

#                 if not username or not password:
#                     return {
#                         'statusCode': 400,
#                         'body': json.dumps({'message': 'Invalid request. Username and password are required.'})
#                     }

#                 # Hash the provided password
#                 hashed_password = hash_password(password)
#                 print(f"Hashed input password: {hashed_password}")

#                 # Authenticate the user
#                 connection = connect_to_db()
#                 with connection.cursor() as cursor:
#                     sql = "SELECT COUNT(*) FROM users WHERE username = %s AND password = %s"
#                     cursor.execute(sql, (username, hashed_password))
#                     result = cursor.fetchone()

#                 if result[0] > 0:
#                     return {
#                         'statusCode': 200,
#                         'body': json.dumps({'message': 'Authentication successful'})
#                         'headers': {
#         'Access-Control-Allow-Origin': '*',  # Allow all origins or your specific domain
#         'Access-Control-Allow-Methods': 'GET, POST, DELETE',
#         'Access-Control-Allow-Headers': 'Content-Type',
#     }
#                     }
#                 else:
#                     return {
#                         'statusCode': 401,
#                         'body': json.dumps({'message': 'Authentication failed'})
#                     }

#             elif 'product_name' in query_params:
#                 # Product Viewing Logic
#                 product_name = query_params.get('product_name')

#                 print(f"Received GET request to view product. Product name: {product_name}")

#                 # Fetch the product details from the database
#                 connection = connect_to_db()
#                 with connection.cursor() as cursor:
#                     sql = "SELECT product_name, price FROM products WHERE product_name = %s"
#                     cursor.execute(sql, (product_name,))
#                     product = cursor.fetchone()

#                 if product:
#                     return {
#                         'statusCode': 200,
#                         'body': json.dumps({'product_name': product[0], 'price': float(product[1])})
#                         'headers': {
#         'Access-Control-Allow-Origin': '*',  # Allow all origins or your specific domain
#         'Access-Control-Allow-Methods': 'GET, POST, DELETE',
#         'Access-Control-Allow-Headers': 'Content-Type',
#     }
#                     }
#                 else:
#                     return {
#                         'statusCode': 404,
#                         'body': json.dumps({'message': 'Product not found'})
#                     }

#             else:
#                 return {
#                     'statusCode': 400,
#                     'body': json.dumps({'message': 'Invalid request. Product name or username/password is required.'})
#                 }

#         # Handle DELETE method: Remove user or product
#         elif event.get('httpMethod') == 'DELETE':
#             body = json.loads(event.get('body', '{}'))  # Safely load body, default to empty dict
#             username = body.get('username')
#             product_name = body.get('product_name')

#             # Remove user from the database
#             if username:
#                 connection = connect_to_db()
#                 with connection.cursor() as cursor:
#                     sql = "DELETE FROM users WHERE username = %s"
#                     cursor.execute(sql, (username,))
#                     connection.commit()

#                 return {
#                     'statusCode': 200,
#                     'body': json.dumps({'message': 'User removed successfully'})
#                     'headers': {
#         'Access-Control-Allow-Origin': '*',  # Allow all origins or your specific domain
#         'Access-Control-Allow-Methods': 'GET, POST, DELETE',
#         'Access-Control-Allow-Headers': 'Content-Type',
#     }
#                 }

#             # Remove product from the database
#             elif product_name:
#                 connection = connect_to_db()
#                 with connection.cursor() as cursor:
#                     sql = "DELETE FROM products WHERE product_name = %s"
#                     cursor.execute(sql, (product_name,))
#                     connection.commit()

#                 return {
#                     'statusCode': 200,
#                     'body': json.dumps({'message': 'Product removed successfully'})
#                     'headers': {
#         'Access-Control-Allow-Origin': '*',  # Allow all origins or your specific domain
#         'Access-Control-Allow-Methods': 'GET, POST, DELETE',
#         'Access-Control-Allow-Headers': 'Content-Type',
#     }
#                 }

#             else:
#                 return {
#                     'statusCode': 400,
#                     'body': json.dumps({'message': 'Invalid request. Username or product_name is required.'})
#                 }

#         # Handle unsupported HTTP methods
#         else:
#             return {
#                 'statusCode': 405,
#                 'body': json.dumps({'message': 'Method not allowed'})
#             }

#     except Exception as e:
#         print(f"Error: {e}")
#         return {
#             'statusCode': 500,
#             'body': json.dumps({'message': 'Internal server error'})
#         }
#     finally:
#         if 'connection' in locals() and connection.open:
#             connection.close()













import json
import pymysql
import os
import hashlib

# Get environment variables for RDS connection
DB_HOST = os.getenv('RDS_HOST')
DB_USER = os.getenv('RDS_USERNAME')
DB_PASSWORD = os.getenv('RDS_PASSWORD')
DB_NAME = os.getenv('RDS_DB_NAME')

# Function to hash passwords using SHA256
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Establish a database connection
def connect_to_db():
    try:
        print(f"Connecting to database at {DB_HOST}")
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Successfully connected to the database.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise e

def lambda_handler(event, context):
    try:
        print(f"Received event: {json.dumps(event)}")  # Log the entire event for debugging

        # Handle POST method: Add user or product
        if event.get('httpMethod') == 'POST':
            body = json.loads(event.get('body', '{}'))  # Safely load body, default to empty dict

            # Check if we are adding a user (based on username and password)
            if 'username' in body and 'password' in body:
                username = body.get('username')
                password = body.get('password')

                # Validate input
                if not username or not password:
                    print(f"Missing username or password. Username: {username}, Password: {password}")
                    return {
                        'statusCode': 400,
                        'body': json.dumps({'message': 'Invalid request. Username and password are required.'})
                    }

                # Hash the password before storing
                hashed_password = hash_password(password)
                print(f"Hashed password: {hashed_password}")  # Log the hashed password

                # Insert the user into the database
                connection = connect_to_db()
                with connection.cursor() as cursor:
                    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                    cursor.execute(sql, (username, hashed_password))
                    connection.commit()

                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'User added successfully'})
                }

            # If not a user, check if we are adding a product (based on product_name and product_price)
            elif 'product_name' in body and 'product_price' in body:
                product_name = body.get('product_name')
                product_price = body.get('product_price')

                if not product_name or not product_price:
                    print(f"Missing product_name or product_price. Product name: {product_name}, Product price: {product_price}")
                    return {
                        'statusCode': 400,
                        'body': json.dumps({'message': 'Invalid request. Product name and price are required.'})
                    }

                # Insert the product into the database
                connection = connect_to_db()
                with connection.cursor() as cursor:
                    sql = "INSERT INTO products (product_name, price) VALUES (%s, %s)"
                    cursor.execute(sql, (product_name, product_price))
                    connection.commit()

                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Product added successfully'})
                }

            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'message': 'Invalid request. Missing necessary fields for user or product.'})
                }

        # Handle GET method: Authenticate user or view product
        elif event.get('httpMethod') == 'GET':
            query_params = event.get('queryStringParameters', {})
            if 'username' in query_params and 'password' in query_params:
                # User Authentication Logic
                username = query_params.get('username')
                password = query_params.get('password')

                print(f"Received GET request for authentication. Username: {username}, Password: {password}")

                if not username or not password:
                    return {
                        'statusCode': 400,
                        'body': json.dumps({'message': 'Invalid request. Username and password are required.'})
                    }

                # Hash the provided password
                hashed_password = hash_password(password)
                print(f"Hashed input password: {hashed_password}")

                # Authenticate the user
                connection = connect_to_db()
                with connection.cursor() as cursor:
                    sql = "SELECT COUNT(*) FROM users WHERE username = %s AND password = %s"
                    cursor.execute(sql, (username, hashed_password))
                    result = cursor.fetchone()

                if result[0] > 0:
                    return {
                        'statusCode': 200,
                        'body': json.dumps({'message': 'Authentication successful Welcome back!!!'})
                    }
                else:
                    return {
                        'statusCode': 401,
                        'body': json.dumps({'message': 'Authentication failed Try Again'})
                    }

            elif 'product_name' in query_params:
                # Product Viewing Logic
                product_name = query_params.get('product_name')

                print(f"Received GET request to view product. Product name: {product_name}")

                # Fetch the product details from the database
                connection = connect_to_db()
                with connection.cursor() as cursor:
                    sql = "SELECT product_name, price FROM products WHERE product_name = %s"
                    cursor.execute(sql, (product_name,))
                    product = cursor.fetchone()

                if product:
                    return {
                        'statusCode': 200,
                        'body': json.dumps({'product_name': product[0], 'price': float(product[1])})
                    }
                else:
                    return {
                        'statusCode': 404,
                        'body': json.dumps({'message': 'Product not found'})
                    }

            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'message': 'Invalid request. Product name or username/password is required.'})
                }

        # Handle DELETE method: Remove user or product
        elif event.get('httpMethod') == 'DELETE':
            body = json.loads(event.get('body', '{}'))  # Safely load body, default to empty dict
            username = body.get('username')
            product_name = body.get('product_name')

            # Remove user from the database
            if username:
                connection = connect_to_db()
                with connection.cursor() as cursor:
                    sql = "DELETE FROM users WHERE username = %s"
                    cursor.execute(sql, (username,))
                    connection.commit()

                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'User removed successfully'})
                }

            # Remove product from the database
            elif product_name:
                connection = connect_to_db()
                with connection.cursor() as cursor:
                    sql = "DELETE FROM products WHERE product_name = %s"
                    cursor.execute(sql, (product_name,))
                    connection.commit()

                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Product removed successfully'})
                }

            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'message': 'Invalid request. Username or product_name is required.'})
                }

        # Handle unsupported HTTP methods
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'message': 'Method not allowed'})
            }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
