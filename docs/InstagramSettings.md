# InstagramSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**post_type** | **str** |  | [optional] [default to 'feed']
**collaborators** | **List[str]** |  | [optional] 
**user_tags** | [**List[InstagramSettingsUserTagsInner]**](InstagramSettingsUserTagsInner.md) |  | [optional] 
**first_comment** | **str** |  | [optional] 
**share_to_feed** | **bool** |  | [optional] 

## Example

```python
from postzen.models.instagram_settings import InstagramSettings

# TODO update the JSON string below
json = "{}"
# create an instance of InstagramSettings from a JSON string
instagram_settings_instance = InstagramSettings.from_json(json)
# print the JSON string representation of the object
print(InstagramSettings.to_json())

# convert the object into a dict
instagram_settings_dict = instagram_settings_instance.to_dict()
# create an instance of InstagramSettings from a dict
instagram_settings_from_dict = InstagramSettings.from_dict(instagram_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


