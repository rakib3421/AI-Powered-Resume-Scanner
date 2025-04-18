import json
import random

from faker import Faker

# Initialize Faker instance
fake = Faker()


# Function to generate random user data
def generate_user_data(num_users):
    users = []
    for _ in range(num_users):
        user = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "age": random.randint(18, 80),
            "address": fake.address().replace("\n", ", "),
            "occupation": fake.job(),
            "religion": random.choice(
                ["Christianity", "Islam", "Hinduism", "Buddhism", "Judaism", "Other"]
            ),
        }
        users.append(user)
    return users


# Generate 500k users
user_data = generate_user_data(500000)

# Write the generated data to a JSON file
file_path = "users_data.json"
with open(file_path, "w") as json_file:
    json.dump(user_data, json_file, indent=4)

print(f"Data has been saved to {file_path}")
