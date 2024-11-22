import csv
from faker import Faker
import random
from google.cloud import storage

# Initialize the Faker instance
fake = Faker()

# Function to generate a random password
def generate_password(length=10):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

# Function to generate dummy employee data
def generate_employee_data(num_records=10):
    data = []
    
    for _ in range(num_records):
        employee = {
            "EmployeeID": fake.unique.random_int(min=1000, max=9999),
            "FirstName": fake.first_name(),
            "LastName": fake.last_name(),
            "Email": fake.email(),
            "PhoneNumber": fake.phone_number(),
            "Address": fake.address().replace('\n', ', '),
            "DateOfBirth": fake.date_of_birth(minimum_age=22, maximum_age=65).strftime("%Y-%m-%d"),
            "Password": generate_password(),
            "Salary": round(random.uniform(30000, 150000), 2),
            "Department": fake.job(),
        }
        data.append(employee)
    
    return data

# Function to write data to a CSV file
def write_to_csv(data, filename='employee_data.csv'):
    fieldnames = data[0].keys()
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data has been written to {filename}")

# Function to upload a file to a GCS bucket
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    # Initialize a Google Cloud Storage client
    storage_client = storage.Client()
    
    # Get the bucket and upload the file
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_filename(source_file_name)
    
    print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")

# Generate 100 dummy employee records
employee_data = generate_employee_data(100)
csv_filename = 'employee_data.csv'
write_to_csv(employee_data, csv_filename)

# Upload the CSV file to a GCS bucket
bucket_name = 'employee-bkt1'  # Replace with your bucket name
destination_blob_name = csv_filename  # The name of the file in GCS
upload_to_gcs(bucket_name, csv_filename, destination_blob_name)
