# postzen.PostsApi

All URIs are relative to *https://api.postzen.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_post**](PostsApi.md#create_post) | **POST** /v1/posts | Create a post


# **create_post**
> CreatePostReplayResponse create_post(create_post_request, x_request_id=x_request_id)

Create a post

Creates a draft, scheduled post, or immediate post. This endpoint requires a read-write API key. Provide exactly one creation mode: `publishNow`, `scheduledFor`, or `isDraft`.

### Example

* Bearer Authentication (bearerAuth):

```python
import postzen
from postzen.models.create_post_replay_response import CreatePostReplayResponse
from postzen.models.create_post_request import CreatePostRequest
from postzen.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.postzen.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = postzen.Configuration(
    host = "https://api.postzen.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = postzen.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with postzen.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = postzen.PostsApi(api_client)
    create_post_request = {"title":"Launch post","content":"We shipped the new release.","publishNow":true,"platforms":[{"platform":"twitter","accountId":"1934567890123456789"}]} # CreatePostRequest | 
    x_request_id = 'x_request_id_example' # str | Optional idempotency key. Repeating the same value returns the original post instead of creating a new one. (optional)

    try:
        # Create a post
        api_response = api_instance.create_post(create_post_request, x_request_id=x_request_id)
        print("The response of PostsApi->create_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PostsApi->create_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_post_request** | [**CreatePostRequest**](CreatePostRequest.md)|  | 
 **x_request_id** | **str**| Optional idempotency key. Repeating the same value returns the original post instead of creating a new one. | [optional] 

### Return type

[**CreatePostReplayResponse**](CreatePostReplayResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Idempotency replay. |  -  |
**201** | Post created. |  -  |
**400** | Invalid request. |  -  |
**401** | Missing or invalid API key. |  -  |
**403** | The API key does not have sufficient permission or profile access. |  -  |
**500** | Unexpected server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

