# YouTubeSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**privacy_status** | **str** |  | [optional] 
**tags** | [**YouTubeSettingsTags**](YouTubeSettingsTags.md) |  | [optional] 
**category_id** | **str** |  | [optional] 
**made_for_kids** | **bool** |  | [optional] 
**notify_subscribers** | **bool** |  | [optional] 

## Example

```python
from postzen.models.you_tube_settings import YouTubeSettings

# TODO update the JSON string below
json = "{}"
# create an instance of YouTubeSettings from a JSON string
you_tube_settings_instance = YouTubeSettings.from_json(json)
# print the JSON string representation of the object
print(YouTubeSettings.to_json())

# convert the object into a dict
you_tube_settings_dict = you_tube_settings_instance.to_dict()
# create an instance of YouTubeSettings from a dict
you_tube_settings_from_dict = YouTubeSettings.from_dict(you_tube_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


