# InstagramSettingsUserTagsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **str** |  | 
**x** | **float** |  | 
**y** | **float** |  | 

## Example

```python
from postzen.models.instagram_settings_user_tags_inner import InstagramSettingsUserTagsInner

# TODO update the JSON string below
json = "{}"
# create an instance of InstagramSettingsUserTagsInner from a JSON string
instagram_settings_user_tags_inner_instance = InstagramSettingsUserTagsInner.from_json(json)
# print the JSON string representation of the object
print(InstagramSettingsUserTagsInner.to_json())

# convert the object into a dict
instagram_settings_user_tags_inner_dict = instagram_settings_user_tags_inner_instance.to_dict()
# create an instance of InstagramSettingsUserTagsInner from a dict
instagram_settings_user_tags_inner_from_dict = InstagramSettingsUserTagsInner.from_dict(instagram_settings_user_tags_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


