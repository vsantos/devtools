from decimal import *
from boto3 import resource
from boto3.dynamodb.conditions import Key


def scan_table_allpages(filter_key=None, filter_value=None):
    """
    Perform a scan operation on table. 
    Can specify filter_key (col name) and its value to be filtered. 
    This gets all pages of results. Returns list of items.
    """

    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()

    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(FilterExpression=filtering_exp,ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break

    return items

def update_table_item(primary_partition_value, primary_classification_value, attribute, value):
    """
        Update a single table item based on a column's atttribute.
        Can specify attribute (col name) and its value to be changed along with the needed primary keys. Ex: 
    """
    return table.update_item(
        Key={
            "TenantAccountTimestamp": primary_partition_value,
            "Timestamp": primary_classification_value
        },
        UpdateExpression='SET {} = :value'.format(attribute),
        ExpressionAttributeValues={
            ':value': value
        }
    )

DYNAMODB_TABLE_NAME = 'MyDynameTable'
# Search all attribute's value ocorrences to be posterior replaced
DYNAMODB_ATTRIBUTE_SEARCH = 'ColumnNameMatch'
DYNAMODB_VALUE_SEARCH = 'ColumnValueMatch'
# Replace value (DYNAMODB_VALUE_REPLACE) from attribute (DYNAMODB_ATTRIBUTE_REPLACE) from all ocorrences
DYNAMODB_ATTRIBUTE_REPLACE = 'ColumnNameToUpdate'
DYNAMODB_VALUE_REPLACE = 'ColumnNewValue'

dynamodb_resource = resource('dynamodb')
table = dynamodb_resource.Table(DYNAMODB_TABLE_NAME)

scan = scan_table_allpages(DYNAMODB_ATTRIBUTE_SEARCH,DYNAMODB_VALUE_SEARCH)
user_input = input("[INFO]: Found a total of '{}' itens from DynamoDB scan. Continue? [y/Y]\n> ".format(len(scan)))

if user_input in ['y', 'Y']:
    print("[INFO]: Starting massive update...")
    for entry in scan:
        print("[INFO]: Updating item for key '{}' and tenant '{}'".format(entry['TenantAccountTimestamp'],entry['Tenant']))
        update_table_item(
            primary_partition_value=entry['TenantAccountTimestamp'],
            primary_classification_value=entry['Timestamp'],
            attribute=DYNAMODB_ATTRIBUTE_REPLACE,
            value=DYNAMODB_VALUE_REPLACE
        )
