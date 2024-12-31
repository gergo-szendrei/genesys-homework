## Important
* The shared validation logics can be outsourced, but for easier read I put them here
* Raise validation cases can be tested by checking against 400 response status and corresponding error message

## Input validation

### Request
* refer the cases from create_user_test.md "Request" section

### Body
* refer the cases from create_user_test.md "Body" section
* should_raise_DictValidationException___when_uuid_field_not_provided
  * Send the body without uuid field

### Full name
* refer the cases from create_user_test.md "Full name" section

### Email address
* refer the cases from create_user_test.md "Email address" section

### Password
* refer the cases from create_user_test.md "Password" section

### UUID
* should_raise_FieldValidationException___when_uuid_not_provided
  * Send field with None or empty value
* should_raise_FieldValidationException___when_uuid_bad_format
  * Send field with invalid uuid format value

## Logic validation
* should_raise_ExistValidationException___when_user_is_not_found
  * Send a proper request, that passes all checks listed so far
  * Uuid value must not be present in DynamoDB
* should_raise_ExistValidationException___when_email_address_is_already_in_use
  * Send a proper request, that passes all checks listed so far
  * Email address value must match with an (other) already existing user's email address

## Success
* should_update_user___when_all_is_ok
  * Send proper request, that passes all checks listed so far
  * Assert DynamoDB update_item is called with proper params
  * Assert DynamoDB has the new values stored for the updated user
  * Assert returned object has matching values with the ones sent in the request
  * Assert status code is 200
