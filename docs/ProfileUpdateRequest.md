# ProfileUpdateRequest

Include at least one field.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** | Pass an empty string or &#x60;null&#x60; to clear the description. | [optional] 
**color** | **str** |  | [optional] 
**is_default** | **bool** | Set to &#x60;true&#x60; to make this the default profile. | [optional] 

## Example

```python
from postzen.models.profile_update_request import ProfileUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ProfileUpdateRequest from a JSON string
profile_update_request_instance = ProfileUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(ProfileUpdateRequest.to_json())

# convert the object into a dict
profile_update_request_dict = profile_update_request_instance.to_dict()
# create an instance of ProfileUpdateRequest from a dict
profile_update_request_from_dict = ProfileUpdateRequest.from_dict(profile_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


