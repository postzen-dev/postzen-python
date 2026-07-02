# PaymentRequiredErrorDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**free_tier_account_limit** | **float** |  | [optional] 
**current_account_count** | **float** |  | [optional] 
**has_payment_method** | **bool** |  | [optional] 

## Example

```python
from postzen.models.payment_required_error_details import PaymentRequiredErrorDetails

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentRequiredErrorDetails from a JSON string
payment_required_error_details_instance = PaymentRequiredErrorDetails.from_json(json)
# print the JSON string representation of the object
print(PaymentRequiredErrorDetails.to_json())

# convert the object into a dict
payment_required_error_details_dict = payment_required_error_details_instance.to_dict()
# create an instance of PaymentRequiredErrorDetails from a dict
payment_required_error_details_from_dict = PaymentRequiredErrorDetails.from_dict(payment_required_error_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


