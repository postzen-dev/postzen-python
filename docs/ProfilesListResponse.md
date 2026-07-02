# ProfilesListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**profiles** | [**List[Profile]**](Profile.md) |  | 

## Example

```python
from postzen.models.profiles_list_response import ProfilesListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProfilesListResponse from a JSON string
profiles_list_response_instance = ProfilesListResponse.from_json(json)
# print the JSON string representation of the object
print(ProfilesListResponse.to_json())

# convert the object into a dict
profiles_list_response_dict = profiles_list_response_instance.to_dict()
# create an instance of ProfilesListResponse from a dict
profiles_list_response_from_dict = ProfilesListResponse.from_dict(profiles_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


