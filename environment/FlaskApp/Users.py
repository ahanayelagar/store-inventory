import boto3

table_name = "Users"

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Access the DynamoDB table
table = dynamodb.Table(table_name)
