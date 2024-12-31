## Important
* The shared validation logics can be outsourced, but for easier read I put them here
* Raise validation cases can be tested by checking against 400 response status and corresponding error message

## Input validation

### Request
* should_raise_RequestValidationException___when_path_params_not_provided
  * Send the request without path params

### Path parameters
* should_raise_DictValidationException___when_uuid_field_not_provided
  * Send the request without uuid

### UUID
* should_raise_FieldValidationException___when_uuid_not_provided
  * Send field with None or empty value
* should_raise_FieldValidationException___when_uuid_bad_format
  * Send field with invalid uuid format value

## Logic validation
* should_raise_ExistValidationException___when_user_is_not_found
  * Send a proper request, that passes all checks listed so far
  * Uuid value must not be present in DynamoDB

## Success
* SetUp DynamoDB to have 2 users stored
* should_get_user___when_all_is_ok
  * Send proper request, that passes all checks listed so far, uuid: (1. user's uuid)
  * Assert DynamoDB query is called with proper params
  * Assert 1. user is returned
  * Assert status code is 200
