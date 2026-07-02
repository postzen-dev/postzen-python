# ConnectCompleteRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | OAuth authorization code returned by the platform. | 
**state** | **str** | State returned by &#x60;GET /v1/connect/{platform}&#x60;. | 
**profile_id** | **str** | PostZen profile id used when the connection was initiated. | 

## Example

```python
from postzen.models.connect_complete_request import ConnectCompleteRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectCompleteRequest from a JSON string
connect_complete_request_instance = ConnectCompleteRequest.from_json(json)
# print the JSON string representation of the object
print(ConnectCompleteRequest.to_json())

# convert the object into a dict
connect_complete_request_dict = connect_complete_request_instance.to_dict()
# create an instance of ConnectCompleteRequest from a dict
connect_complete_request_from_dict = ConnectCompleteRequest.from_dict(connect_complete_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


