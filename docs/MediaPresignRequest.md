# MediaPresignRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filename** | **str** | Original file name. PostZen sanitizes it for storage. | 
**content_type** | **str** |  | 
**size** | **int** | File size in bytes. | [optional] 
**profile_id** | **str** | Optional profile scope. If provided, the API key must have access to the profile. | [optional] 

## Example

```python
from postzen.models.media_presign_request import MediaPresignRequest

# TODO update the JSON string below
json = "{}"
# create an instance of MediaPresignRequest from a JSON string
media_presign_request_instance = MediaPresignRequest.from_json(json)
# print the JSON string representation of the object
print(MediaPresignRequest.to_json())

# convert the object into a dict
media_presign_request_dict = media_presign_request_instance.to_dict()
# create an instance of MediaPresignRequest from a dict
media_presign_request_from_dict = MediaPresignRequest.from_dict(media_presign_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


