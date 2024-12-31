## Important
* The shared validation logics can be outsourced, but for easier read I put them here
* Raise validation cases can be tested by checking against 400 response status and corresponding error message

## Input validation

### Request
* refer the cases from create_user_test.md "Request" section

### Body
* should_raise_DictValidationException___when_limit_field_not_provided
  * Send the body without limit field

### Limit
* should_raise_FieldValidationException___when_limit_is_too_small
  * Send field with value smaller than 1

### UUID
* should_raise_FieldValidationException___when_uuid_bad_format
  * Send field with invalid uuid format value

## Success
* SetUp DynamoDB to have 5 users stored
* should_list_users___when_fetched_without_uuid
  * Send proper request, that passes all checks listed so far, with limit: 2, uuid: None
  * Assert DynamoDB scan is called with proper params
  * Assert 1. and 2. users are returned
  * Assert status code is 200
* should_list_users___when_fetched_with_uuid
  * Send proper request, that passes all checks listed so far, with limit: 2, uuid: (2. user's uuid)
  * Assert DynamoDB scan is called with proper params
  * Assert 3. and 4. users are returned
  * Assert status code is 200
