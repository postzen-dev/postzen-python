# ApiPostPlatformResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**platform** | [**PublicPlatformInput**](PublicPlatformInput.md) |  | 
**account_id** | [**ApiPostAccount**](ApiPostAccount.md) |  | 
**status** | **str** |  | 
**platform_post_url** | **str** |  | [optional] 
**error** | **str** |  | [optional] 

## Example

```python
from postzen.models.api_post_platform_result import ApiPostPlatformResult

# TODO update the JSON string below
json = "{}"
# create an instance of ApiPostPlatformResult from a JSON string
api_post_platform_result_instance = ApiPostPlatformResult.from_json(json)
# print the JSON string representation of the object
print(ApiPostPlatformResult.to_json())

# convert the object into a dict
api_post_platform_result_dict = api_post_platform_result_instance.to_dict()
# create an instance of ApiPostPlatformResult from a dict
api_post_platform_result_from_dict = ApiPostPlatformResult.from_dict(api_post_platform_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


