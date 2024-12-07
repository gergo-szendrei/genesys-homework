import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as app from '../bin/cdk';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigatewayv2 from 'aws-cdk-lib/aws-apigatewayv2';
import * as apigatewayv2i from 'aws-cdk-lib/aws-apigatewayv2-integrations';
import * as apigatewayv2a from 'aws-cdk-lib/aws-apigatewayv2-authorizers';

// API
const API_PREFIX = "/api";
const API_USER = API_PREFIX + "/user";

export class HttpApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, lambdaFunctionWrappers: app.LambdaFunctionWrapper[],
              props?: cdk.StackProps
  ) {
    super(scope, id, props);
    const httpApi: apigatewayv2.HttpApi = this.createHttpApi(app.RESOURCE_PREFIX + 'http-api');
    const authorizer: apigatewayv2a.HttpJwtAuthorizer = this.createAuthorizer(
      app.RESOURCE_PREFIX + 'http-api-authorizer');
    lambdaFunctionWrappers.forEach((lambdaFunctionWrapper: app.LambdaFunctionWrapper) => {
      this.createIntegrationAndRoute(lambdaFunctionWrapper, authorizer, httpApi);
    });
  }

  private createHttpApi(httpApiId: string): apigatewayv2.HttpApi {
    return new apigatewayv2.HttpApi(this, httpApiId, {
      apiName: httpApiId
    });
  }

  private createAuthorizer(authorizerId: string): apigatewayv2a.HttpJwtAuthorizer {
    return new apigatewayv2a.HttpJwtAuthorizer(authorizerId, app.USER_POOL_ISSUER_URL, {
      authorizerName: authorizerId,
      jwtAudience: [app.USER_POOL_CLIENT_ID]
    })
  }

  private createIntegrationAndRoute(lambdaFunctionWrapper: app.LambdaFunctionWrapper,
                                    authorizer: apigatewayv2a.HttpJwtAuthorizer, httpApi: apigatewayv2.HttpApi) {
    const integration: apigatewayv2i.HttpLambdaIntegration = this.createIntegration(
      app.RESOURCE_PREFIX + lambdaFunctionWrapper.lambdaFunctionType + '-lambda-integration',
      lambdaFunctionWrapper.lambdaFunction);
    const routeKey: apigatewayv2.HttpRouteKey = this.createRouteKey(lambdaFunctionWrapper.lambdaFunctionType)
    this.createRoute(app.RESOURCE_PREFIX + lambdaFunctionWrapper.lambdaFunctionType + '-lambda-route',
      authorizer, httpApi, integration, routeKey);
  }

  private createIntegration(integrationId: string, lambdaFunction: lambda.Function)
    : apigatewayv2i.HttpLambdaIntegration {
    return new apigatewayv2i.HttpLambdaIntegration(integrationId, lambdaFunction);
  }

  private createRouteKey(lambdaFunctionType: app.LambdaFunctionType): apigatewayv2.HttpRouteKey {
    if (lambdaFunctionType === 'create_user') {
      return apigatewayv2.HttpRouteKey.with(API_USER, apigatewayv2.HttpMethod.POST)
    }
    if (lambdaFunctionType === 'update_user') {
      return apigatewayv2.HttpRouteKey.with(API_USER, apigatewayv2.HttpMethod.PUT)
    }
    if (lambdaFunctionType === 'delete_user') {
      return apigatewayv2.HttpRouteKey.with(API_USER + '/{uuid}', apigatewayv2.HttpMethod.DELETE)
    }
    if (lambdaFunctionType === 'get_user') {
      return apigatewayv2.HttpRouteKey.with(API_USER + '/{uuid}', apigatewayv2.HttpMethod.GET)
    }
    throw new Error('Not Implemented!');
  }

  private createRoute(routeId: string, authorizer: apigatewayv2a.HttpJwtAuthorizer, httpApi: apigatewayv2.IHttpApi,
                      integration: apigatewayv2i.HttpLambdaIntegration, routeKey: apigatewayv2.HttpRouteKey
  ): void {
    new apigatewayv2.HttpRoute(this, routeId, {
      authorizer,
      httpApi,
      integration,
      routeKey
    });
  }
}
