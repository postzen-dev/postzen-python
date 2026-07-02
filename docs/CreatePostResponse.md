# CreatePostResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**post** | [**ApiPost**](ApiPost.md) |  | 
**message** | **str** |  | 

## Example

```python
from postzen.models.create_post_response import CreatePostResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreatePostResponse from a JSON string
create_post_response_instance = CreatePostResponse.from_json(json)
# print the JSON string representation of the object
print(CreatePostResponse.to_json())

# convert the object into a dict
create_post_response_dict = create_post_response_instance.to_dict()
# create an instance of CreatePostResponse from a dict
create_post_response_from_dict = CreatePostResponse.from_dict(create_post_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


