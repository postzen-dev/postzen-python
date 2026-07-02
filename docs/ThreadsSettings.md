# ThreadsSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reply_control** | **str** |  | [optional] 

## Example

```python
from postzen.models.threads_settings import ThreadsSettings

# TODO update the JSON string below
json = "{}"
# create an instance of ThreadsSettings from a JSON string
threads_settings_instance = ThreadsSettings.from_json(json)
# print the JSON string representation of the object
print(ThreadsSettings.to_json())

# convert the object into a dict
threads_settings_dict = threads_settings_instance.to_dict()
# create an instance of ThreadsSettings from a dict
threads_settings_from_dict = ThreadsSettings.from_dict(threads_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


