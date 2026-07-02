# XSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reply_settings** | **str** |  | [optional] 

## Example

```python
from postzen.models.x_settings import XSettings

# TODO update the JSON string below
json = "{}"
# create an instance of XSettings from a JSON string
x_settings_instance = XSettings.from_json(json)
# print the JSON string representation of the object
print(XSettings.to_json())

# convert the object into a dict
x_settings_dict = x_settings_instance.to_dict()
# create an instance of XSettings from a dict
x_settings_from_dict = XSettings.from_dict(x_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


