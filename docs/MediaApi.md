# postzen.MediaApi

All URIs are relative to *https://api.postzen.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_media_presign**](MediaApi.md#create_media_presign) | **POST** /v1/media/presign | Create a presigned media upload URL


# **create_media_presign**
> MediaPresignResponse create_media_presign(media_presign_request)

Create a presigned media upload URL

Creates a presigned URL for uploading an image, video, GIF, or PDF to PostZen-hosted storage. Upload the file with an HTTP `PUT` to `uploadUrl`, then reference `publicUrl` in post `mediaItems`. This endpoint requires a read-write API key.

### Example

* Bearer Authentication (bearerAuth):

```python
import postzen
from postzen.models.media_presign_request import MediaPresignRequest
from postzen.models.media_presign_response import MediaPresignResponse
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
    api_instance = postzen.MediaApi(api_client)
    media_presign_request = {"filename":"launch-video.mp4","contentType":"video/mp4","size":10485760} # MediaPresignRequest | 

    try:
        # Create a presigned media upload URL
        api_response = api_instance.create_media_presign(media_presign_request)
        print("The response of MediaApi->create_media_presign:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MediaApi->create_media_presign: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **media_presign_request** | [**MediaPresignRequest**](MediaPresignRequest.md)|  | 

### Return type

[**MediaPresignResponse**](MediaPresignResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Presigned upload URL created. |  -  |
**400** | Invalid request. |  -  |
**401** | Missing or invalid API key. |  -  |
**403** | The API key does not have sufficient permission or profile access. |  -  |
**404** | Resource not found. |  -  |
**500** | Unexpected server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

