# FacebookSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**link** | **str** |  | [optional] 
**first_comment** | **str** |  | [optional] 

## Example

```python
from postzen.models.facebook_settings import FacebookSettings

# TODO update the JSON string below
json = "{}"
# create an instance of FacebookSettings from a JSON string
facebook_settings_instance = FacebookSettings.from_json(json)
# print the JSON string representation of the object
print(FacebookSettings.to_json())

# convert the object into a dict
facebook_settings_dict = facebook_settings_instance.to_dict()
# create an instance of FacebookSettings from a dict
facebook_settings_from_dict = FacebookSettings.from_dict(facebook_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


