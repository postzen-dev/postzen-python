# AccountProfileSummary


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**slug** | **str** |  | 
**color** | **str** |  | 

## Example

```python
from postzen.models.account_profile_summary import AccountProfileSummary

# TODO update the JSON string below
json = "{}"
# create an instance of AccountProfileSummary from a JSON string
account_profile_summary_instance = AccountProfileSummary.from_json(json)
# print the JSON string representation of the object
print(AccountProfileSummary.to_json())

# convert the object into a dict
account_profile_summary_dict = account_profile_summary_instance.to_dict()
# create an instance of AccountProfileSummary from a dict
account_profile_summary_from_dict = AccountProfileSummary.from_dict(account_profile_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


