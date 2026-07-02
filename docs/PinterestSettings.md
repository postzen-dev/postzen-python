# PinterestSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**board_id** | **str** | Pinterest board to publish the pin to. | [optional] 
**title** | **str** | Pin title. | [optional] 
**link** | **str** | Destination link for the pin. | [optional] 
**alt_text** | **str** |  | [optional] 

## Example

```python
from postzen.models.pinterest_settings import PinterestSettings

# TODO update the JSON string below
json = "{}"
# create an instance of PinterestSettings from a JSON string
pinterest_settings_instance = PinterestSettings.from_json(json)
# print the JSON string representation of the object
print(PinterestSettings.to_json())

# convert the object into a dict
pinterest_settings_dict = pinterest_settings_instance.to_dict()
# create an instance of PinterestSettings from a dict
pinterest_settings_from_dict = PinterestSettings.from_dict(pinterest_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


