# MediaPresignResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**upload_url** | **str** | Use this URL for the direct file upload. | 
**public_url** | **str** | Use this URL in post &#x60;mediaItems&#x60;. | 
**key** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from postzen.models.media_presign_response import MediaPresignResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MediaPresignResponse from a JSON string
media_presign_response_instance = MediaPresignResponse.from_json(json)
# print the JSON string representation of the object
print(MediaPresignResponse.to_json())

# convert the object into a dict
media_presign_response_dict = media_presign_response_instance.to_dict()
# create an instance of MediaPresignResponse from a dict
media_presign_response_from_dict = MediaPresignResponse.from_dict(media_presign_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


