# CreatePostRequest

Provide exactly one creation mode: `publishNow`, `scheduledFor`, or `isDraft`. `platforms` is required unless `isDraft` is true.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Internal post title. YouTube uses this as the fallback video title when &#x60;settings.title&#x60; is omitted. | [optional] 
**content** | **str** | Shared post text. Platform-specific validation still applies. | [optional] [default to '']
**media_items** | [**List[PostMediaItem]**](PostMediaItem.md) | Duplicate URLs are removed before the post is created. | [optional] 
**platforms** | [**List[CreatePostTarget]**](CreatePostTarget.md) |  | [optional] 
**scheduled_for** | **datetime** | ISO 8601 date for scheduled posts. Must be at least 60 seconds in the future. | [optional] 
**publish_now** | **bool** | Publish synchronously where possible. | [optional] 
**is_draft** | **bool** | Create a draft. &#x60;platforms&#x60; is optional for drafts. | [optional] 
**timezone** | **str** |  | [optional] [default to 'UTC']
**tags** | **List[str]** |  | [optional] 

## Example

```python
from postzen.models.create_post_request import CreatePostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreatePostRequest from a JSON string
create_post_request_instance = CreatePostRequest.from_json(json)
# print the JSON string representation of the object
print(CreatePostRequest.to_json())

# convert the object into a dict
create_post_request_dict = create_post_request_instance.to_dict()
# create an instance of CreatePostRequest from a dict
create_post_request_from_dict = CreatePostRequest.from_dict(create_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


