import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as dynamoDbStack from '../lib/dynamo-db-stack';
import * as lambdaStack from '../lib/lambda-stack';
import * as httpApiStack from '../lib/http-api-stack';

// --- ARCHITECTURE POINT - STACKS ---
// My chosen approach is to separate each main blocks of the architecture into different stacks
// This way we can have kind of "independent" stacks, which are easier to reuse, maintain and handle
// There are still some dependency between stacks (order, reference, etc.), so it is not complete independent relation

// --- DEVELOPMENT POINT - CONSTANTS ---
// Single-stack, single-use values are provided directly in the given stack's constructor or in iterator step
// Single-stack, multi-use values are provided as const at the top of given stack
// Cross-stack, multi-use values and dynamic values are provided as const and exported at the top of cdk.ts

// --- DEVELOPMENT POINT - CASING ---
// Default AWS resource / element casing uses '-' symbols
// However in python related scenarios this is changed to '_' symbols

// GENERAL
export const ACCOUNT = '';
export const REGION = 'eu-north-1';
export const RESOURCE_PREFIX = 'umas-';

// DYNAMO
export const DYNAMO_DB_USER_TABLE = RESOURCE_PREFIX + 'user';
export const DYNAMO_DB_USER_TABLE_EMAIL_ADDRESS_GSI_NAME = 'email_address_index';

// LAMBDA
export const LAMBDA_FUNCTION_TYPES: string[] = [
  'create_user',
  'update_user',
  'delete_user'
];
export type LambdaFunctionType = typeof LAMBDA_FUNCTION_TYPES[number];

export interface LambdaFunctionWrapper {
  lambdaFunction: lambda.Function;
  lambdaFunctionType: LambdaFunctionType;
}

// COGNITO
// Created and exists independently of this application as other applications are using it as well
export const USER_POOL_ISSUER_URL = '';
export const USER_POOL_CLIENT_ID = '';

// MAIN
const env: cdk.Environment = {account: ACCOUNT, region: REGION};
const app = new cdk.App();
new dynamoDbStack.DynamoDbStack(app, RESOURCE_PREFIX + 'dynamo-db-stack', {env});
const ls = new lambdaStack.LambdaStack(app, RESOURCE_PREFIX + 'lambda-stack', {env});
new httpApiStack.HttpApiStack(app, RESOURCE_PREFIX + 'http-api-stack', ls.lambdaFunctionWrappers, {env});
