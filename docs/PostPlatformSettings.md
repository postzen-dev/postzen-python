# PostPlatformSettings

Platform-specific publishing options. Unknown keys are ignored.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**post_type** | **str** |  | [optional] [default to 'feed']
**collaborators** | **List[str]** |  | [optional] 
**user_tags** | [**List[InstagramSettingsUserTagsInner]**](InstagramSettingsUserTagsInner.md) |  | [optional] 
**first_comment** | **str** |  | [optional] 
**share_to_feed** | **bool** |  | [optional] 
**link** | **str** | Destination link for the pin. | [optional] 
**reply_control** | **str** |  | [optional] 
**privacy_level** | **str** |  | [optional] 
**allow_comments** | **bool** |  | [optional] 
**allow_duet** | **bool** |  | [optional] 
**allow_stitch** | **bool** |  | [optional] 
**disable_comment** | **bool** |  | [optional] 
**disable_duet** | **bool** |  | [optional] 
**disable_stitch** | **bool** |  | [optional] 
**video_cover_timestamp_ms** | **float** |  | [optional] 
**upload_as_draft** | **bool** |  | [optional] 
**brand_content_toggle** | **bool** |  | [optional] 
**brand_organic_toggle** | **bool** |  | [optional] 
**visibility** | **str** |  | [optional] 
**reply_settings** | **str** |  | [optional] 
**title** | **str** | Pin title. | [optional] 
**privacy_status** | **str** |  | [optional] 
**tags** | [**YouTubeSettingsTags**](YouTubeSettingsTags.md) |  | [optional] 
**category_id** | **str** |  | [optional] 
**made_for_kids** | **bool** |  | [optional] 
**notify_subscribers** | **bool** |  | [optional] 
**board_id** | **str** | Pinterest board to publish the pin to. | [optional] 
**alt_text** | **str** |  | [optional] 

## Example

```python
from postzen.models.post_platform_settings import PostPlatformSettings

# TODO update the JSON string below
json = "{}"
# create an instance of PostPlatformSettings from a JSON string
post_platform_settings_instance = PostPlatformSettings.from_json(json)
# print the JSON string representation of the object
print(PostPlatformSettings.to_json())

# convert the object into a dict
post_platform_settings_dict = post_platform_settings_instance.to_dict()
# create an instance of PostPlatformSettings from a dict
post_platform_settings_from_dict = PostPlatformSettings.from_dict(post_platform_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


