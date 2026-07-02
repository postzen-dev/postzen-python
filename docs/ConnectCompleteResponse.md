# ConnectCompleteResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | 
**platform** | [**PublicPlatformOutput**](PublicPlatformOutput.md) |  | 
**profile_id** | **str** |  | 
**status** | **str** |  | 
**missing_scopes** | **List[str]** |  | [optional] 
**connected_account_count** | **int** |  | [optional] 
**accounts** | [**List[Account]**](Account.md) |  | [optional] 

## Example

```python
from postzen.models.connect_complete_response import ConnectCompleteResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectCompleteResponse from a JSON string
connect_complete_response_instance = ConnectCompleteResponse.from_json(json)
# print the JSON string representation of the object
print(ConnectCompleteResponse.to_json())

# convert the object into a dict
connect_complete_response_dict = connect_complete_response_instance.to_dict()
# create an instance of ConnectCompleteResponse from a dict
connect_complete_response_from_dict = ConnectCompleteResponse.from_dict(connect_complete_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


