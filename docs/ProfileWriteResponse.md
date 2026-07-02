# ProfileWriteResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | 
**profile** | [**Profile**](Profile.md) |  | 

## Example

```python
from postzen.models.profile_write_response import ProfileWriteResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProfileWriteResponse from a JSON string
profile_write_response_instance = ProfileWriteResponse.from_json(json)
# print the JSON string representation of the object
print(ProfileWriteResponse.to_json())

# convert the object into a dict
profile_write_response_dict = profile_write_response_instance.to_dict()
# create an instance of ProfileWriteResponse from a dict
profile_write_response_from_dict = ProfileWriteResponse.from_dict(profile_write_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


