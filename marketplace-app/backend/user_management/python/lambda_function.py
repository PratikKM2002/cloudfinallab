# import json
# import pymysql
# import os

# # Get environment variables for RDS connection
# DB_HOST = os.getenv('RDS_HOST')
# DB_USER = os.getenv('RDS_USERNAME')
# DB_PASSWORD = os.getenv('RDS_PASSWORD')
# DB_NAME = os.getenv('RDS_DB_NAME')

# # Establish a database connection
# def connect_to_db():
#     try:
#         return pymysql.connect(
#             host=DB_HOST,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             database=DB_NAME
#         )
#     except Exception as e:
#         print(f"Error connecting to the database: {e}")
#         raise e

# def lambda_handler(event, context):
#     try:
#         print(f"Received event: {json.dumps(event)}")  # Log the entire event for debugging

#         # Handle POST method: Add user
#         if event.get('httpMethod') == 'POST':
#             body = json.loads(event.get('body', '{}'))  # Safely load body, default to empty dict
#             username = body.get('username')
#             password = body.get('password')

#             if not username or not password:
#                 print(f"Missing username or password. Username: {username}, Password: {password}")
#                 return {
#                     'statusCode': 400,
#                     'body': json.dumps({'message': 'Invalid request. Username and password are required.'})
#                 }

#             # Insert the user into the database
#             connection = connect_to_db()
#             with connection.cursor() as cursor:
#                 sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
#                 cursor.execute(sql, (username, password))
#                 connection.commit()

#             return {
#                 'statusCode': 200,
#                 'body': json.dumps({'message': 'User added successfully'})
#             }

#         # Handle GET method: Authenticate user
#         elif event.get('httpMethod') == 'GET':
#             query_params = event.get('queryStringParameters', {})
#             username = query_params.get('username')
#             password = query_params.get('password')

#             print(f"Received GET request. Username: {username}, Password: {password}")  # Log the username and password

#             if not username or not password:
#                 print(f"Missing username or password. Username: {username}, Password: {password}")
#                 return {
#                     'statusCode': 400,
#                     'body': json.dumps({'message': 'Invalid request. Username and password are required.'})
#                 }

#             # Authenticate the user
#             connection = connect_to_db()
#             with connection.cursor() as cursor:
#                 sql = "SELECT COUNT(*) FROM users WHERE username = %s AND password = %s"
#                 cursor.execute(sql, (username, password))
#                 result = cursor.fetchone()

#             if result[0] > 0:
#                 return {
#                     'statusCode': 200,
#                     'body': json.dumps({'message': 'Authentication successful'})
#                 }
#             else:
#                 return {
#                     'statusCode': 401,
#                     'body': json.dumps({'message': 'Authentication failed'})
#                 }

#         # Handle DELETE method: Remove user
#         elif event.get('httpMethod') == 'DELETE':
#             body = json.loads(event.get('body', '{}'))  # Safely load body, default to empty dict
#             username = body.get('username')

#             if not username:
#                 return {
#                     'statusCode': 400,
#                     'body': json.dumps({'message': 'Invalid request. Username is required.'})
#                 }

#             # Remove the user from the database
#             connection = connect_to_db()
#             with connection.cursor() as cursor:
#                 sql = "DELETE FROM users WHERE username = %s"
#                 cursor.execute(sql, (username,))
#                 connection.commit()

#             return {
#                 'statusCode': 200,
#                 'body': json.dumps({'message': 'User removed successfully'})
#             }

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
import bcrypt  # Import bcrypt for password hashing

# Get environment variables for RDS connection
DB_HOST = os.getenv('RDS_HOST')
DB_USER = os.getenv('RDS_USERNAME')
DB_PASSWORD = os.getenv('RDS_PASSWORD')
DB_NAME = os.getenv('RDS_DB_NAME')

# Validate environment variables
if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
    raise ValueError("Missing required environment variables for database connection.")

# CORS headers (to be used in all responses)
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",  # Allow all domains, or replace with specific domain
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS, DELETE",  # Allow methods
    "Access-Control-Allow-Headers": "Content-Type, Authorization"  # Allow specific headers
}

# Establish a database connection
def connect_to_db():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor  # Return results as dictionaries
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise e

def lambda_handler(event, context):
    try:
        # Handle preflight OPTIONS request
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': CORS_HEADERS,
                'body': json.dumps({'message': 'CORS preflight successful'})
            }

        # Handle POST method: Add user
        if event.get('httpMethod') == 'POST':
            body = json.loads(event.get('body', '{}'))  # Safely load body, default to empty dict
            username = body.get('username')
            password = body.get('password')

            if not username or not password:
                return {
                    'statusCode': 400,
                    'headers': CORS_HEADERS,
                    'body': json.dumps({'message': 'Invalid request. Username and password are required.'})
                }

            # Hash the password before storing it
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert the user into the database
            connection = connect_to_db()
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(sql, (username, hashed_password))
                connection.commit()

            return {
                'statusCode': 200,
                'headers': CORS_HEADERS,
                'body': json.dumps({'message': 'User added successfully'})
            }

        # Handle GET method: Authenticate user
        elif event.get('httpMethod') == 'GET':
            query_params = event.get('queryStringParameters', {})
            username = query_params.get('username')
            password = query_params.get('password')

            if not username or not password:
                return {
                    'statusCode': 400,
                    'headers': CORS_HEADERS,
                    'body': json.dumps({'message': 'Invalid request. Username and password are required.'})
                }

            # Authenticate the user by comparing hashed passwords
            connection = connect_to_db()
            with connection.cursor() as cursor:
                sql = "SELECT password FROM users WHERE username = %s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()

            if result and bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8')):
                return {
                    'statusCode': 200,
                    'headers': CORS_HEADERS,
                    'body': json.dumps({'message': 'Authentication successful'})
                }
            else:
                return {
                    'statusCode': 401,
                    'headers': CORS_HEADERS,
                    'body': json.dumps({'message': 'Authentication failed'})
                }

        # Handle DELETE method: Remove user
        elif event.get('httpMethod') == 'DELETE':
            body = json.loads(event.get('body', '{}'))  # Safely load body, default to empty dict
            username = body.get('username')

            if not username:
                return {
                    'statusCode': 400,
                    'headers': CORS_HEADERS,
                    'body': json.dumps({'message': 'Invalid request. Username is required.'})
                }

            # Remove the user from the database
            connection = connect_to_db()
            with connection.cursor() as cursor:
                sql = "DELETE FROM users WHERE username = %s"
                cursor.execute(sql, (username,))
                connection.commit()

            return {
                'statusCode': 200,
                'headers': CORS_HEADERS,
                'body': json.dumps({'message': 'User removed successfully'})
            }

        # Handle unsupported HTTP methods
        else:
            return {
                'statusCode': 405,
                'headers': CORS_HEADERS,
                'body': json.dumps({'message': 'Method not allowed'})
            }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': 'Internal server error'})
        }
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
