# AccountsListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accounts** | [**List[Account]**](Account.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from postzen.models.accounts_list_response import AccountsListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AccountsListResponse from a JSON string
accounts_list_response_instance = AccountsListResponse.from_json(json)
# print the JSON string representation of the object
print(AccountsListResponse.to_json())

# convert the object into a dict
accounts_list_response_dict = accounts_list_response_instance.to_dict()
# create an instance of AccountsListResponse from a dict
accounts_list_response_from_dict = AccountsListResponse.from_dict(accounts_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


