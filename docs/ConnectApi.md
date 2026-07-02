# postzen.ConnectApi

All URIs are relative to *https://api.postzen.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**complete_connect**](ConnectApi.md#complete_connect) | **POST** /v1/connect/{platform} | Complete an OAuth connection
[**create_connect_url**](ConnectApi.md#create_connect_url) | **GET** /v1/connect/{platform} | Create an OAuth connect URL


# **complete_connect**
> ConnectCompleteResponse complete_connect(platform, connect_complete_request)

Complete an OAuth connection

Exchanges an OAuth authorization code for tokens and connects the account to the specified profile. This endpoint requires a read-write API key.

### Example

* Bearer Authentication (bearerAuth):

```python
import postzen
from postzen.models.connect_complete_request import ConnectCompleteRequest
from postzen.models.connect_complete_response import ConnectCompleteResponse
from postzen.models.public_platform_input import PublicPlatformInput
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
    api_instance = postzen.ConnectApi(api_client)
    platform = postzen.PublicPlatformInput() # PublicPlatformInput | Social platform to connect. `twitter` is accepted as an alias for `x`.
    connect_complete_request = {"code":"AQTF0v6PZnq1yTkGxg3M4S8d","state":"3q2Xv8Zk1mR5tY7wA9bC4dE6","profileId":"jh72r5nqk9wx3v8m1t4cz6bs0fy5dg3e"} # ConnectCompleteRequest | 

    try:
        # Complete an OAuth connection
        api_response = api_instance.complete_connect(platform, connect_complete_request)
        print("The response of ConnectApi->complete_connect:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectApi->complete_connect: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **platform** | [**PublicPlatformInput**](.md)| Social platform to connect. &#x60;twitter&#x60; is accepted as an alias for &#x60;x&#x60;. | 
 **connect_complete_request** | [**ConnectCompleteRequest**](ConnectCompleteRequest.md)|  | 

### Return type

[**ConnectCompleteResponse**](ConnectCompleteResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Account connected. |  -  |
**400** | Invalid request, expired OAuth state, or a failed platform callback. Callback failures return a camelCase error code with an optional &#x60;errorDescription&#x60;. |  -  |
**401** | Missing or invalid API key. |  -  |
**402** | A billing limit prevents the requested connection. |  -  |
**403** | The API key does not have access to the profile, or the OAuth state belongs to a different user or profile. |  -  |
**404** | Resource not found. |  -  |
**500** | The platform token exchange failed or an unexpected server error occurred. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_connect_url**
> ConnectStartResponse create_connect_url(profile_id, platform, redirect_url=redirect_url)

Create an OAuth connect URL

Initiates an OAuth connection flow and returns an authorization URL to redirect the user to. The OAuth state expires after 10 minutes. This endpoint requires a read-write API key.

### Example

* Bearer Authentication (bearerAuth):

```python
import postzen
from postzen.models.connect_start_response import ConnectStartResponse
from postzen.models.public_platform_input import PublicPlatformInput
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
    api_instance = postzen.ConnectApi(api_client)
    profile_id = 'profile_id_example' # str | PostZen profile id to attach the connected account to.
    platform = postzen.PublicPlatformInput() # PublicPlatformInput | Social platform to connect. `twitter` is accepted as an alias for `x`.
    redirect_url = 'redirect_url_example' # str | Custom URL PostZen redirects to after the connection completes. (optional)

    try:
        # Create an OAuth connect URL
        api_response = api_instance.create_connect_url(profile_id, platform, redirect_url=redirect_url)
        print("The response of ConnectApi->create_connect_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectApi->create_connect_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_id** | **str**| PostZen profile id to attach the connected account to. | 
 **platform** | [**PublicPlatformInput**](.md)| Social platform to connect. &#x60;twitter&#x60; is accepted as an alias for &#x60;x&#x60;. | 
 **redirect_url** | **str**| Custom URL PostZen redirects to after the connection completes. | [optional] 

### Return type

[**ConnectStartResponse**](ConnectStartResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OAuth URL created. |  -  |
**400** | Invalid request. |  -  |
**401** | Missing or invalid API key. |  -  |
**402** | A billing limit prevents the requested connection. |  -  |
**403** | The API key does not have sufficient permission or profile access. |  -  |
**404** | Resource not found. |  -  |
**500** | Unexpected server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

