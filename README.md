# Home Assignment

## Setup guide
* Provide AWS Account ID for `ACCOUNT` variable in **cdk.ts**
  * **For example**: `472233445566`
* Provide AWS Region Name for `REGION` variable in **cdk.ts**
  * **For example**: `eu-north-1`
* Provide Cognito Pool Issuer URL for `USER_POOL_ISSUER_URL` variable in **cdk.ts**
* Provide Cognito Pool Client ID for `USER_POOL_CLIENT_ID` variable in **cdk.ts**
* Create a session with a sufficient privileged AWS User
  * **For example**: `aws sso login --profile MainAdmin`
* Run `cdk deploy`
  * **For example**: `cdk deploy '**' --profile MainAdmin`
* Run `cdk destroy` when it is not needed anymore
  * **For example**: `cdk destroy '**' --profile MainAdmin`

## Testing
For testing I see both the following ways applicable:
* Unit testing and mocking AWS Resources
* Integration test on "real" test resources

As the main points that need to be tested are the same I chose the first one.
I did not go into code implementation, but provided all the scenarios I would test for.
Steps I would take:
* To test the business functionality, I would use standard unit testing approach / framework 
* To mock the AWS Resources, I would use Moto Library (https://pypi.org/project/moto/)
  * Init environ variables and DynamoDB resources in **setUp**
  * Reset these in **tearDown**
  * Add the test cases as **def** blocks
    * The list of these cases are listed in "..._test" files near .py files

## Questions
* Why is this a **TS** project, while the assignment states the logic should be written in Python?
  * The assignment requires only the backend logic, no logging, deployment, security, etc. is needed
  * The backend logic can be found in separate Lambdas, which are implemented in Python
  * The reasoning for additional TS part can be found under the next question


* Why the **CDK** needed?
  * I found it more realistic to provide an AWS environment for the demo, as there were no restrictions on how to 
    do this (as it is optional), I went with TS + CDK
  * Another reason behind this, that my applications are using these as well, so I could re-use some code


* Why **Cognito**?
  * As I am using Identity Center and Cognito already for my applications, it was easy to extend them for 
    the assignment's needs
  * This is why I did not choose IAM auth on Lambdas, but rather went with Cognito auth on Gateway level
  * Leaving the endpoints without security is no option, not even for a demo application, due to possible cost impact
    coming from unauthorized use


* Why not using **OpenAPI**?
  * Normally I would definitely go with OpenAPI 3.0 design, and import the HTTP API from that
  * The reason to not follow this approach is that the infra is not scope of this assignment, therefore I went with 
  the faster approach, as I already had this approach developed and ready to use

* Why using **HTTP API** instead of REST API?
  * Unlike REST API, HTTP API supports JWT Authorizer which is the easiest option with Cognito, 
    also provides smaller cost for API calls

* Why not using **bcrypt** for hashing?
  * I had only a MAC and a Windows PC available for building the package, but AWS requires Linux built package to run.
