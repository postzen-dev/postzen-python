# Account


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**platform** | [**PublicPlatformOutput**](PublicPlatformOutput.md) |  | 
**provider_account_id** | **str** |  | 
**profile_id** | [**AccountProfileSummary**](AccountProfileSummary.md) |  | 
**username** | **str** |  | 
**display_name** | **str** |  | 
**profile_url** | **str** |  | [optional] 
**avatar_url** | **str** |  | [optional] 
**status** | **str** |  | 
**is_active** | **bool** |  | 
**connected_at** | **datetime** |  | 
**last_synced_at** | **datetime** |  | [optional] 

## Example

```python
from postzen.models.account import Account

# TODO update the JSON string below
json = "{}"
# create an instance of Account from a JSON string
account_instance = Account.from_json(json)
# print the JSON string representation of the object
print(Account.to_json())

# convert the object into a dict
account_dict = account_instance.to_dict()
# create an instance of Account from a dict
account_from_dict = Account.from_dict(account_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


