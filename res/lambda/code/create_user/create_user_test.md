## Important
* The shared validation logics can be outsourced, but for easier read I put them here
* Raise validation cases can be tested by checking against 400 response status and corresponding error message

## Input validation

### Request
* should_raise_RequestValidationException___when_body_not_provided
  * Send the request without a body

### Body
* should_raise_DictValidationException___when_full_name_field_not_provided
  * Send the body without full_name field
* should_raise_DictValidationException___when_email_address_field_not_provided
  * Send the body without email_address field
* should_raise_DictValidationException___when_password_field_not_provided
  * Send the body without password field

### Full name
* should_raise_FieldValidationException___when_full_name_not_provided
  * Send field with None or empty value
* should_raise_FieldValidationException___when_full_name_too_short
  * Send field with value shorter than 3
* should_raise_FieldValidationException___when_full_name_too_long
  * Send field with value longer than 64
* should_raise_FieldValidationException___when_full_name_missing_space
  * Send field without space

### Email address
* should_raise_FieldValidationException___when_email_address_not_provided
  * Send field with None or empty value
* should_raise_FieldValidationException___when_email_address_too_short
  * Send field with value shorter than 6
* should_raise_FieldValidationException___when_email_address_too_long
  * Send field with value longer than 64
* should_raise_FieldValidationException___when_email_address_bad_format
  * Send field with invalid email format value

### Password
* should_raise_FieldValidationException___when_password_not_provided
  * Send field with None or empty value
* should_raise_FieldValidationException___when_password_too_short
  * Send field with value shorter than 12
* should_raise_FieldValidationException___when_password_too_long
  * Send field with value longer than 64
* should_raise_FieldValidationException___when_password_missing_uppercase
  * Send field without uppercase letter
* should_raise_FieldValidationException___when_password_missing_lowercase
  * Send field without lowercase letter
* should_raise_FieldValidationException___when_password_missing_number
  * Send field without numeric character
* should_raise_FieldValidationException___when_password_missing_special
  * Send field without special character

## Logic validation
* should_raise_ExistValidationException___when_email_address_is_already_in_use
  * Send proper request, that passes all checks listed so far
  * Send email address value, that already saved in DynamoDB

## Success
* should_save_user___when_all_is_ok
  * Send proper request, that passes all checks listed so far
  * Assert DynamoDB put_item is called with proper params
  * Assert DynamoDB has the new user stored
  * Assert returned object has matching values with the ones sent in the request
  * Assert status code is 201
