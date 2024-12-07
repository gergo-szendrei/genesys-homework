import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as app from '../bin/cdk';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class DynamoDbStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    this.createTableWithGsi(app.DYNAMO_DB_USER_TABLE, 'uuid',
      app.DYNAMO_DB_USER_TABLE_EMAIL_ADDRESS_GSI_NAME, 'email_address');
  }

  // --- ARCHITECTURE POINT - CAPACITY ---
  // As this is just a PoC version, capacity is more than enough to be set on 2 / 2
  // Production version would either need proper calculation based capacity setup or on-demand setup
  private createTableWithGsi(tableId: string, partitionKeyId: string, gsiIndexName: string,
                             gsiPartitionKey: string): void {
    const table: dynamodb.Table = this.createTable(tableId, partitionKeyId);
    table.addGlobalSecondaryIndex({
      indexName: gsiIndexName,
      partitionKey: {name: gsiPartitionKey, type: dynamodb.AttributeType.STRING},
      projectionType: dynamodb.ProjectionType.ALL,
      readCapacity: 2,
      writeCapacity: 2,
    });
  }

  // --- ARCHITECTURE POINT - CAPACITY ---
  // As this is just a PoC version, capacity is more than enough to be set on 2 / 2
  // Production version would either need proper calculation based capacity setup or on-demand setup

  // --- ARCHITECTURE POINT - REMOVAL ---
  // As this is just a PoC version, it does not matter much if the data gets destroyed on cdk destroy
  // Production version should have the RETAIN option selected
  private createTable(tableId: string, partitionKeyId: string): dynamodb.Table {
    return new dynamodb.Table(this, tableId, {
      billingMode: dynamodb.BillingMode.PROVISIONED,
      partitionKey: {
        name: partitionKeyId,
        type: dynamodb.AttributeType.STRING
      },
      readCapacity: 2,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      tableName: tableId,
      writeCapacity: 2
    });
  }
}
