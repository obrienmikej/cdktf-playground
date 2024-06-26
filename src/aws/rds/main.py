from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.provider import AwsProvider, rds
from cdktf_cdktf_provider_aws.instance import Instance

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        AwsProvider(self, "AWS", region="us-west-2")

        # Define RDS Aurora Cluster
        aurora_cluster = rds.RdsCluster(
            self, "MyAuroraCluster",
            cluster_identifier="my-aurora-cluster",
            engine="aurora-mysql",
            master_username="admin",
            master_password="password123",  # Replace with your own secure password
            skip_final_snapshot=True,
            backup_retention_period=0,  # No backups
        )

        # Define RDS Aurora Instance
        aurora_instance = rds.RdsClusterInstance(
            self, "MyAuroraInstance",
            identifier="my-aurora-instance",
            cluster_identifier=aurora_cluster.cluster_identifier,
            instance_class="db.t3.small",  # Smallest instance type
            engine="aurora-mysql",
        )

        # Output the endpoint of the Aurora Cluster
        TerraformOutput(self, "aurora_endpoint",
                        value=aurora_cluster.endpoint)

app = App()
MyStack(app, "aws-rds-aurora")

app.synth()