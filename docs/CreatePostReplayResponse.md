# CreatePostReplayResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**existing_post** | [**ApiPost**](ApiPost.md) |  | 
**message** | **str** |  | 

## Example

```python
from postzen.models.create_post_replay_response import CreatePostReplayResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreatePostReplayResponse from a JSON string
create_post_replay_response_instance = CreatePostReplayResponse.from_json(json)
# print the JSON string representation of the object
print(CreatePostReplayResponse.to_json())

# convert the object into a dict
create_post_replay_response_dict = create_post_replay_response_instance.to_dict()
# create an instance of CreatePostReplayResponse from a dict
create_post_replay_response_from_dict = CreatePostReplayResponse.from_dict(create_post_replay_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


