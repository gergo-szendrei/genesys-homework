## Important
* The shared validation logics can be outsourced, but for easier read I put them here
* Raise validation cases can be tested by checking against 400 response status and corresponding error message

## Input validation

### Request
* refer the cases from create_user_test.md "Request" section

### Body
* refer "email address" and "password" cases from create_user_test.md "Body" section

### Email address
* refer the cases from create_user_test.md "Email address" section

### Password
* refer the cases from create_user_test.md "Password" section

## Logic validation
* should_yield_unauthenticated___when_user_is_not_found
  * Send a proper request, that passes all checks listed so far
  * Email address value must not be present in DynamoDB
  * Assert status code is 401
* should_yield_unauthenticated___when_password_is_incorrect
  * Send a proper request, that passes all checks listed so far
  * Password must be incorrect
  * Assert status code is 401

## Success
* should_login_user___when_all_is_ok
  * Send proper request, that passes all checks listed so far
  * Assert DynamoDB update_item is called with proper params
  * Assert DynamoDB has the new last_login stored for the logged in user
  * Assert returned object has proper token set (now it is always "imagine_generated_token_here")
  * Assert status code is 200
