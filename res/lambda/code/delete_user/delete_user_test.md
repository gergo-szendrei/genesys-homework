## Important
* The shared validation logics can be outsourced, but for easier read I put them here
* Raise validation cases can be tested by checking against 400 response status and corresponding error message

## Input validation

### Request
* refer the cases from get_user_test.md "Request" section

### Path parameters
* refer the cases from get_user_test.md "Path parameters" section

### UUID
* refer the cases from get_user_test.md "UUID" section

## Logic validation
* refer the cases from get_user_test.md "Logic validation" section

## Success
* SetUp DynamoDB to have 2 users stored
* should_delete_user___when_all_is_ok
  * Send proper request, that passes all checks listed so far, uuid: (1. user's uuid)
  * Assert DynamoDB query is called with proper params
  * Assert DynamoDB no longer has 1. user stored
  * Assert 1. user's uuid is returned
  * Assert status code is 200
