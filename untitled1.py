from datetime import datetime, timedelta
import re
import boto3

# Crie um cliente Lambda com a chave de API
lambda_client = boto3.client('lambda', aws_access_key_id='YOUR_ACCESS_KEY',
                               aws_secret_access_key='YOUR_SECRET_KEY')

# Chame a função Lambda
response = lambda_client.invoke(FunctionName='YOUR_FUNCTION_NAME',
                               InvocationType='RequestResponse')

# Obtenha o resultado da chamada
DATA_TXT = response['Payload'].read().decode('utf-8')

# Imprima o resultado
print(DATA_TXT)

# Crie um cliente S3 com a chave de API
s3_client = boto3.client('s3', aws_access_key_id='YOUR_ACCESS_KEY',
                               aws_secret_access_key='YOUR_SECRET_KEY')

# Conecte-se ao bucket S3
bucket_name = 'YOUR_BUCKET_NAME'
response = s3_client.list_objects(Bucket=bucket_name)

# Obtenha os nomes dos objetos no bucket
objects = response['Contents']
for obj in objects:
    print(obj['Key'])

# Crie um cliente RDS com a chave de API
rds_client = boto3.client('rds', aws_access_key_id='YOUR_ACCESS_KEY',
                               aws_secret_access_key='YOUR_SECRET_KEY')

# Conecte-se ao banco de dados RDS
db_instance_identifier = 'YOUR_DB_INSTANCE_IDENTIFIER'
db_username = 'YOUR_DB_USERNAME'
db_password = 'YOUR_DB_PASSWORD'
db_endpoint = 'YOUR_DB_ENDPOINT'

try:
    # Conecte-se ao banco de dados
    conn = rds_client.connect_db_instance(DBInstanceIdentifier=db_instance_identifier,
                                            Username=db_username,
                                            Password=db_password,
                                            Host=db_endpoint)

    # Crie um cursor para executar consultas
    cursor = conn.cursor()

    # Execute uma consulta
    cursor.execute("SELECT * FROM YOUR_TABLE")

    # Obtenha os resultados da consulta
    results = cursor.fetchall()

    # Imprima os resultados
    for result in results:
        print(result)

finally:
    # Feche a conexão com o banco de dados
    conn.close()

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY
dt_string = now.strftime("%d/%m/%Y")

def extract_date(date_string):
  """
  Extracts the date in the format "%d/%m/%Y" from a string in the format "%d/%m/%Y %H:%M:%S".
  """
  match = re.search(r"(\d{2})/(\d{2})/(\d{4})", date_string)
  if match:
    return f"{match.group(3)}-{match.group(2)}-{match.group(1)}"
  else:
    return None

# Apply the function to each element in the list DATA_TXT
filtered_dates = [extract_date(date) for date in DATA_TXT]

def check_date_and_continue(filtered_dates, dt_string):
  """
  Checks if the filtered_dates list contains a date equal to dt_string.
  If it does, the function continues execution. Otherwise, it prints a message and exits.
  """
  if dt_string in filtered_dates:
    # Continue with the code execution
    print("Date found. Continuing execution...")

    # Assign the found date to an object called dt_obj
    dt_obj = dt_string
  else:
    # Exit the program
    print("Date not found. Exiting program...")
    exit()

  # Convert dt_string to a datetime object
  dt_obj = datetime.strptime(dt_obj, "%Y-%m-%d")

  # Calculate the date two days before dt_string
  two_days_before = dt - timedelta(days=2)

  # Convert two_days_before to a string in the same format as the dates in filtered_dates
  two_days_before_str = two_days_before.strftime("%Y-%m-%d")

# Crie um cursor para executar consultas
cursor = conn.cursor()

# Execute uma consulta
cursor.execute("SELECT * FROM YOUR_TABLE WHERE date_column BETWEEN %s AND %s", (two_days_before_str, dt_string))

# Obtenha os resultados da consulta
results = cursor.fetchall()

# Imprima os resultados
for result in results:
    print(result)

# Feche a conexão com o banco de dados
conn.close()
