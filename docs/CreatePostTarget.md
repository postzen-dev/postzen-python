# CreatePostTarget


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**platform** | [**PublicPlatformInput**](PublicPlatformInput.md) |  | 
**account_id** | **str** | PostZen account id or provider account id. | 
**custom_content** | **str** | Overrides shared &#x60;content&#x60; for this platform. | [optional] 
**settings** | [**PostPlatformSettings**](PostPlatformSettings.md) |  | [optional] 

## Example

```python
from postzen.models.create_post_target import CreatePostTarget

# TODO update the JSON string below
json = "{}"
# create an instance of CreatePostTarget from a JSON string
create_post_target_instance = CreatePostTarget.from_json(json)
# print the JSON string representation of the object
print(CreatePostTarget.to_json())

# convert the object into a dict
create_post_target_dict = create_post_target_instance.to_dict()
# create an instance of CreatePostTarget from a dict
create_post_target_from_dict = CreatePostTarget.from_dict(create_post_target_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


