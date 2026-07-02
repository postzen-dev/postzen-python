# PaymentRequiredError


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** |  | 
**code** | **str** |  | 
**reason** | **str** |  | 
**documentation_url** | **str** |  | 
**dashboard_url** | **str** |  | 
**details** | [**PaymentRequiredErrorDetails**](PaymentRequiredErrorDetails.md) |  | [optional] 

## Example

```python
from postzen.models.payment_required_error import PaymentRequiredError

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentRequiredError from a JSON string
payment_required_error_instance = PaymentRequiredError.from_json(json)
# print the JSON string representation of the object
print(PaymentRequiredError.to_json())

# convert the object into a dict
payment_required_error_dict = payment_required_error_instance.to_dict()
# create an instance of PaymentRequiredError from a dict
payment_required_error_from_dict = PaymentRequiredError.from_dict(payment_required_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


