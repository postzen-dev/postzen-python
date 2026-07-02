# postzen.ProfilesApi

All URIs are relative to *https://api.postzen.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_profile**](ProfilesApi.md#create_profile) | **POST** /v1/profiles | Create a profile
[**delete_profile**](ProfilesApi.md#delete_profile) | **DELETE** /v1/profiles/{profileId} | Delete a profile
[**get_profile**](ProfilesApi.md#get_profile) | **GET** /v1/profiles/{profileId} | Get a profile
[**list_profiles**](ProfilesApi.md#list_profiles) | **GET** /v1/profiles | List profiles
[**update_profile**](ProfilesApi.md#update_profile) | **PUT** /v1/profiles/{profileId} | Update a profile


# **create_profile**
> ProfileWriteResponse create_profile(profile_create_request)

Create a profile

Creates a profile. This endpoint requires a read-write API key with access to all profiles.

### Example

* Bearer Authentication (bearerAuth):

```python
import postzen
from postzen.models.profile_create_request import ProfileCreateRequest
from postzen.models.profile_write_response import ProfileWriteResponse
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
    api_instance = postzen.ProfilesApi(api_client)
    profile_create_request = {"name":"Marketing Team","description":"Profile for marketing campaigns","color":"#4caf50"} # ProfileCreateRequest | 

    try:
        # Create a profile
        api_response = api_instance.create_profile(profile_create_request)
        print("The response of ProfilesApi->create_profile:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfilesApi->create_profile: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_create_request** | [**ProfileCreateRequest**](ProfileCreateRequest.md)|  | 

### Return type

[**ProfileWriteResponse**](ProfileWriteResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Profile created. |  -  |
**400** | Invalid request. |  -  |
**401** | Missing or invalid API key. |  -  |
**403** | The API key does not have sufficient permission or profile access. |  -  |
**500** | Unexpected server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_profile**
> MessageResponse delete_profile(profile_id)

Delete a profile

Deletes a profile. The default profile cannot be deleted, and profiles with connected accounts must be disconnected first.

### Example

* Bearer Authentication (bearerAuth):

```python
import postzen
from postzen.models.message_response import MessageResponse
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
    api_instance = postzen.ProfilesApi(api_client)
    profile_id = 'profile_id_example' # str | PostZen profile id.

    try:
        # Delete a profile
        api_response = api_instance.delete_profile(profile_id)
        print("The response of ProfilesApi->delete_profile:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfilesApi->delete_profile: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_id** | **str**| PostZen profile id. | 

### Return type

[**MessageResponse**](MessageResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Profile deleted. |  -  |
**400** | Invalid request. |  -  |
**401** | Missing or invalid API key. |  -  |
**403** | The API key does not have sufficient permission or profile access. |  -  |
**404** | Resource not found. |  -  |
**500** | Unexpected server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_profile**
> ProfileResponse get_profile(profile_id)

Get a profile

Returns a single profile visible to the API key.

### Example

* Bearer Authentication (bearerAuth):

```python
import postzen
from postzen.models.profile_response import ProfileResponse
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
    api_instance = postzen.ProfilesApi(api_client)
    profile_id = 'profile_id_example' # str | PostZen profile id.

    try:
        # Get a profile
        api_response = api_instance.get_profile(profile_id)
        print("The response of ProfilesApi->get_profile:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfilesApi->get_profile: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_id** | **str**| PostZen profile id. | 

### Return type

[**ProfileResponse**](ProfileResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Profile returned. |  -  |
**401** | Missing or invalid API key. |  -  |
**403** | The API key does not have sufficient permission or profile access. |  -  |
**404** | Resource not found. |  -  |
**500** | Unexpected server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_profiles**
> ProfilesListResponse list_profiles()

List profiles

Returns profiles available to the API key, sorted by creation date (oldest first). Read-only and read-write API keys are accepted.

### Example

* Bearer Authentication (bearerAuth):

```python
import postzen
from postzen.models.profiles_list_response import ProfilesListResponse
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
    api_instance = postzen.ProfilesApi(api_client)

    try:
        # List profiles
        api_response = api_instance.list_profiles()
        print("The response of ProfilesApi->list_profiles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfilesApi->list_profiles: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ProfilesListResponse**](ProfilesListResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Profiles returned. |  -  |
**401** | Missing or invalid API key. |  -  |
**500** | Unexpected server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_profile**
> ProfileWriteResponse update_profile(profile_id, profile_update_request)

Update a profile

Updates one or more profile fields. This endpoint requires a read-write API key.

### Example

* Bearer Authentication (bearerAuth):

```python
import postzen
from postzen.models.profile_update_request import ProfileUpdateRequest
from postzen.models.profile_write_response import ProfileWriteResponse
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
    api_instance = postzen.ProfilesApi(api_client)
    profile_id = 'profile_id_example' # str | PostZen profile id.
    profile_update_request = {"name":"Marketing Team (Updated)","description":"Updated profile description","color":"#2196f3","isDefault":true} # ProfileUpdateRequest | 

    try:
        # Update a profile
        api_response = api_instance.update_profile(profile_id, profile_update_request)
        print("The response of ProfilesApi->update_profile:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfilesApi->update_profile: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_id** | **str**| PostZen profile id. | 
 **profile_update_request** | [**ProfileUpdateRequest**](ProfileUpdateRequest.md)|  | 

### Return type

[**ProfileWriteResponse**](ProfileWriteResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Profile updated. |  -  |
**400** | Invalid request. |  -  |
**401** | Missing or invalid API key. |  -  |
**403** | The API key does not have sufficient permission or profile access. |  -  |
**404** | Resource not found. |  -  |
**500** | Unexpected server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

