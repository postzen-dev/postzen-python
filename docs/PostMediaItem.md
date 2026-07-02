# PostMediaItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | PostZen-hosted &#x60;publicUrl&#x60; from &#x60;POST /v1/media/presign&#x60;, or an external image/video URL. External URLs are downloaded and re-hosted by PostZen; they must resolve to an image or video (PDF is not supported) of at most 100 MB. | 
**title** | **str** | Optional alt text/title for the media item. | [optional] 

## Example

```python
from postzen.models.post_media_item import PostMediaItem

# TODO update the JSON string below
json = "{}"
# create an instance of PostMediaItem from a JSON string
post_media_item_instance = PostMediaItem.from_json(json)
# print the JSON string representation of the object
print(PostMediaItem.to_json())

# convert the object into a dict
post_media_item_dict = post_media_item_instance.to_dict()
# create an instance of PostMediaItem from a dict
post_media_item_from_dict = PostMediaItem.from_dict(post_media_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


