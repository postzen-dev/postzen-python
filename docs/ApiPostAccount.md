# ApiPostAccount


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**platform** | [**PublicPlatformInput**](PublicPlatformInput.md) |  | 
**username** | **str** |  | 
**display_name** | **str** |  | 
**is_active** | **bool** |  | 

## Example

```python
from postzen.models.api_post_account import ApiPostAccount

# TODO update the JSON string below
json = "{}"
# create an instance of ApiPostAccount from a JSON string
api_post_account_instance = ApiPostAccount.from_json(json)
# print the JSON string representation of the object
print(ApiPostAccount.to_json())

# convert the object into a dict
api_post_account_dict = api_post_account_instance.to_dict()
# create an instance of ApiPostAccount from a dict
api_post_account_from_dict = ApiPostAccount.from_dict(api_post_account_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


