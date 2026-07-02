# TikTokSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
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

## Example

```python
from postzen.models.tik_tok_settings import TikTokSettings

# TODO update the JSON string below
json = "{}"
# create an instance of TikTokSettings from a JSON string
tik_tok_settings_instance = TikTokSettings.from_json(json)
# print the JSON string representation of the object
print(TikTokSettings.to_json())

# convert the object into a dict
tik_tok_settings_dict = tik_tok_settings_instance.to_dict()
# create an instance of TikTokSettings from a dict
tik_tok_settings_from_dict = TikTokSettings.from_dict(tik_tok_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


