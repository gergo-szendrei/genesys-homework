import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as app from '../bin/cdk';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as logs from 'aws-cdk-lib/aws-logs';

export class LambdaStack extends cdk.Stack {
  readonly lambdaFunctionWrappers: app.LambdaFunctionWrapper[] = [];

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    const lambdaLayers: lambda.LayerVersion[] = this.createLambdaLayers();
    app.LAMBDA_FUNCTION_TYPES.forEach((lambdaFunctionType: app.LambdaFunctionType) => {
      this.addLambdaFunction(lambdaFunctionType, lambdaLayers);
    });
  }

  private createLambdaLayers(): lambda.LayerVersion[] {
    return [
      this.createLambdaLayer(app.RESOURCE_PREFIX + 'validator-lambda-layer',
        'res/lambda/layer/validator/python.zip'),
      this.createLambdaLayer(app.RESOURCE_PREFIX + 'dynamo-lambda-layer',
        'res/lambda/layer/dynamo/python.zip'),
      this.createLambdaLayer(app.RESOURCE_PREFIX + 'hash-lambda-layer',
        'res/lambda/layer/hash/python.zip')
    ];
  }

  private createLambdaLayer(layerId: string, codePath: string): lambda.LayerVersion {
    return new lambda.LayerVersion(this, layerId, {
      code: lambda.Code.fromAsset(codePath),
      compatibleArchitectures: [lambda.Architecture.ARM_64],
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_12],
      layerVersionName: layerId,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
  }

  private addLambdaFunction(lambdaFunctionType: app.LambdaFunctionType, lambdaLayers: lambda.LayerVersion[]): void {
    const lambdaEnvironment: { [key: string]: string } = this.createLambdaEnvironment();
    const lambdaLogGroup: logs.LogGroup = this.createLambdaLogGroup(
      app.RESOURCE_PREFIX + lambdaFunctionType + '-lambda-log-group');
    const lambdaPolicies: iam.IManagedPolicy[] = this.createLambdaPolicies(lambdaFunctionType);
    const lambdaRole: iam.Role = this.createLambdaRole(
      app.RESOURCE_PREFIX + lambdaFunctionType + '-lambda-role', lambdaPolicies);
    const lambdaFunction: lambda.Function = this.createLambdaFunction(
      app.RESOURCE_PREFIX + lambdaFunctionType + '-lambda-function', 'res/lambda/code/' + lambdaFunctionType,
      lambdaEnvironment, lambdaFunctionType + '.lambda_handler', lambdaLayers, lambdaLogGroup, lambdaRole);
    this.lambdaFunctionWrappers.push({
      lambdaFunction,
      lambdaFunctionType
    });
  }

  private createLambdaEnvironment(): { [key: string]: string } {
    return {
      DYNAMO_DB_USER_TABLE: app.DYNAMO_DB_USER_TABLE,
      DYNAMO_DB_USER_TABLE_EMAIL_ADDRESS_GSI_NAME: app.DYNAMO_DB_USER_TABLE_EMAIL_ADDRESS_GSI_NAME
    };
  }

  private createLambdaLogGroup(logGroupId: string): logs.LogGroup {
    return new logs.LogGroup(this, logGroupId, {
      logGroupName: logGroupId,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });
  }

  private createLambdaPolicies(lambdaFunctionType: app.LambdaFunctionType): iam.IManagedPolicy[] {
    const commonPolicy: iam.IManagedPolicy = iam.ManagedPolicy.fromAwsManagedPolicyName(
      'service-role/AWSLambdaBasicExecutionRole');
    if (lambdaFunctionType === 'create_user') {
      return [
        this.createLambdaPolicy(app.RESOURCE_PREFIX + lambdaFunctionType + '-lambda-custom-policy-gsi',
          ['dynamodb:Query'],
          ['arn:aws:dynamodb:' + app.REGION + ':' + app.ACCOUNT + ':table/' + app.DYNAMO_DB_USER_TABLE + '/index/'
          + app.DYNAMO_DB_USER_TABLE_EMAIL_ADDRESS_GSI_NAME]),
        this.createLambdaPolicy(app.RESOURCE_PREFIX + lambdaFunctionType + '-lambda-custom-policy-table',
          ['dynamodb:PutItem'],
          ['arn:aws:dynamodb:' + app.REGION + ':' + app.ACCOUNT + ':table/' + app.DYNAMO_DB_USER_TABLE]),
        commonPolicy
      ];
    }
    if (lambdaFunctionType === 'update_user') {
      return [
        this.createLambdaPolicy(app.RESOURCE_PREFIX + lambdaFunctionType + '-lambda-custom-policy-gsi',
          ['dynamodb:Query'],
          ['arn:aws:dynamodb:' + app.REGION + ':' + app.ACCOUNT + ':table/' + app.DYNAMO_DB_USER_TABLE + '/index/'
          + app.DYNAMO_DB_USER_TABLE_EMAIL_ADDRESS_GSI_NAME]),
        this.createLambdaPolicy(app.RESOURCE_PREFIX + lambdaFunctionType + '-lambda-custom-policy-table',
          ['dynamodb:Query', 'dynamodb:UpdateItem'],
          ['arn:aws:dynamodb:' + app.REGION + ':' + app.ACCOUNT + ':table/' + app.DYNAMO_DB_USER_TABLE]),
        commonPolicy
      ];
    }
    if (lambdaFunctionType === 'delete_user') {
      return [
        this.createLambdaPolicy(app.RESOURCE_PREFIX + lambdaFunctionType + '-lambda-custom-policy-table',
          ['dynamodb:Query', 'dynamodb:DeleteItem'],
          ['arn:aws:dynamodb:' + app.REGION + ':' + app.ACCOUNT + ':table/' + app.DYNAMO_DB_USER_TABLE]),
        commonPolicy
      ];
    }
    if (lambdaFunctionType === 'get_user') {
      return [
        this.createLambdaPolicy(app.RESOURCE_PREFIX + lambdaFunctionType + '-lambda-custom-policy-table',
          ['dynamodb:Query'],
          ['arn:aws:dynamodb:' + app.REGION + ':' + app.ACCOUNT + ':table/' + app.DYNAMO_DB_USER_TABLE]),
        commonPolicy
      ];
    }
    if (lambdaFunctionType === 'list_users') {
      return [
        this.createLambdaPolicy(app.RESOURCE_PREFIX + lambdaFunctionType + '-lambda-custom-policy-table',
          ['dynamodb:Scan'],
          ['arn:aws:dynamodb:' + app.REGION + ':' + app.ACCOUNT + ':table/' + app.DYNAMO_DB_USER_TABLE]),
        commonPolicy
      ];
    }
    throw new Error('Not Implemented!');
  }

  private createLambdaPolicy(policyId: string, actions: string[], resources: string[]): iam.ManagedPolicy {
    return new iam.ManagedPolicy(this, policyId, {
      statements: [
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions,
          resources
        })
      ]
    });
  }

  private createLambdaRole(roleId: string, lambdaPolicies: iam.IManagedPolicy[]): iam.Role {
    return new iam.Role(this, roleId, {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: lambdaPolicies,
      roleName: roleId
    });
  }

  private createLambdaFunction(lambdaFunctionId: string, assetPath: string, lambdaEnvironment: {
                                 [key: string]: string
                               },
                               handler: string, lambdaLayers: lambda.LayerVersion[],
                               lambdaLogGroup: logs.LogGroup, lambdaRole: iam.Role
  ): lambda.Function {
    return new lambda.Function(this, lambdaFunctionId, {
      architecture: lambda.Architecture.ARM_64,
      code: lambda.Code.fromAsset(assetPath),
      environment: lambdaEnvironment,
      functionName: lambdaFunctionId,
      handler,
      layers: lambdaLayers,
      logGroup: lambdaLogGroup,
      role: lambdaRole,
      runtime: lambda.Runtime.PYTHON_3_12,
    });
  }
}
