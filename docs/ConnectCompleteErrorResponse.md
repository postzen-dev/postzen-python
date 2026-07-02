# ConnectCompleteErrorResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** | Human-readable message, or a camelCase error code (for example &#x60;oauthCallbackFailed&#x60;) when the platform callback fails. | 
**error_description** | **str** | Additional detail reported by the platform, when available. | [optional] 

## Example

```python
from postzen.models.connect_complete_error_response import ConnectCompleteErrorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectCompleteErrorResponse from a JSON string
connect_complete_error_response_instance = ConnectCompleteErrorResponse.from_json(json)
# print the JSON string representation of the object
print(ConnectCompleteErrorResponse.to_json())

# convert the object into a dict
connect_complete_error_response_dict = connect_complete_error_response_instance.to_dict()
# create an instance of ConnectCompleteErrorResponse from a dict
connect_complete_error_response_from_dict = ConnectCompleteErrorResponse.from_dict(connect_complete_error_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


