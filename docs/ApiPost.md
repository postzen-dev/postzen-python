# ApiPost


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**title** | **str** |  | 
**content** | **str** |  | 
**status** | **str** |  | 
**scheduled_for** | **datetime** |  | 
**timezone** | **str** |  | 
**platforms** | [**List[ApiPostPlatformResult]**](ApiPostPlatformResult.md) |  | 

## Example

```python
from postzen.models.api_post import ApiPost

# TODO update the JSON string below
json = "{}"
# create an instance of ApiPost from a JSON string
api_post_instance = ApiPost.from_json(json)
# print the JSON string representation of the object
print(ApiPost.to_json())

# convert the object into a dict
api_post_dict = api_post_instance.to_dict()
# create an instance of ApiPost from a dict
api_post_from_dict = ApiPost.from_dict(api_post_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


