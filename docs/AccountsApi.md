# postzen.AccountsApi

All URIs are relative to *https://api.postzen.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**disconnect_account**](AccountsApi.md#disconnect_account) | **DELETE** /v1/accounts/{accountId} | Disconnect an account
[**list_accounts**](AccountsApi.md#list_accounts) | **GET** /v1/accounts | List accounts


# **disconnect_account**
> MessageResponse disconnect_account(account_id)

Disconnect an account

Disconnects and removes a connected social account. Pending scheduled, queued, and publishing targets for that account are canceled. This endpoint requires a read-write API key.

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
    api_instance = postzen.AccountsApi(api_client)
    account_id = 'account_id_example' # str | PostZen account id.

    try:
        # Disconnect an account
        api_response = api_instance.disconnect_account(account_id)
        print("The response of AccountsApi->disconnect_account:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountsApi->disconnect_account: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account_id** | **str**| PostZen account id. | 

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
**200** | Account disconnected. |  -  |
**401** | Missing or invalid API key. |  -  |
**403** | The API key does not have sufficient permission or profile access. |  -  |
**404** | Resource not found. |  -  |
**500** | Unexpected server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_accounts**
> AccountsListResponse list_accounts(profile_id=profile_id, platform=platform, status=status, page=page, limit=limit)

List accounts

Returns connected social accounts available to the API key, sorted by connection date (newest first). Read-only and read-write API keys are accepted.

### Example

* Bearer Authentication (bearerAuth):

```python
import postzen
from postzen.models.accounts_list_response import AccountsListResponse
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
    api_instance = postzen.AccountsApi(api_client)
    profile_id = 'profile_id_example' # str | Filter accounts by profile id. (optional)
    platform = postzen.PublicPlatformInput() # PublicPlatformInput | Filter accounts by platform. `twitter` is accepted as an alias for `x`. (optional)
    status = 'status_example' # str | `connected` returns healthy accounts. `disconnected` returns accounts that need reconnection or are disabled. (optional)
    page = 56 # int | 1-based page number. Must be provided with `limit`. (optional)
    limit = 56 # int | Page size. Must be provided with `page`. (optional)

    try:
        # List accounts
        api_response = api_instance.list_accounts(profile_id=profile_id, platform=platform, status=status, page=page, limit=limit)
        print("The response of AccountsApi->list_accounts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountsApi->list_accounts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_id** | **str**| Filter accounts by profile id. | [optional] 
 **platform** | [**PublicPlatformInput**](.md)| Filter accounts by platform. &#x60;twitter&#x60; is accepted as an alias for &#x60;x&#x60;. | [optional] 
 **status** | **str**| &#x60;connected&#x60; returns healthy accounts. &#x60;disconnected&#x60; returns accounts that need reconnection or are disabled. | [optional] 
 **page** | **int**| 1-based page number. Must be provided with &#x60;limit&#x60;. | [optional] 
 **limit** | **int**| Page size. Must be provided with &#x60;page&#x60;. | [optional] 

### Return type

[**AccountsListResponse**](AccountsListResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Accounts returned. |  -  |
**400** | Invalid request. |  -  |
**401** | Missing or invalid API key. |  -  |
**403** | The API key does not have sufficient permission or profile access. |  -  |
**404** | Resource not found. |  -  |
**500** | Unexpected server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

