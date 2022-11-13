"""this file contains functions that call the AWS API"""
import boto3


def print_info(message):
    """ Prints info message in a unified format. """
    print(f'[RUN INFO] {message}')


def print_error(message):
    """ Prints error message in a unified format. """
    print(f'[ERROR] {message}')


def get_vpc(silent=False):
    """ Gets the VPC from AWS. """
    client = boto3.client('ec2')
    try:
        response = client.describe_vpcs()
        return response['Vpcs'][0]['VpcId']
    except Exception as e:
        if not silent:
            print(e)


def create_security_group(
        vpc_id,
        name="log8145-security-group",
        description="SG for VMs used in LOG8145",
        silent=False
        ) -> dict:
    """ Creates a new security group with a specific name and description. """
    client = boto3.client('ec2')

    try:
        response = client.create_security_group(GroupName=name,
                                                Description=description,
                                                VpcId=vpc_id)
        security_group_id = response['GroupId']

        data = client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        if not silent:
            print_info('Ingress Successfully Set %s' % data)
        return response
        
    except Exception as e:
        if not silent:
            print(e)


def describe_security_group_id_by_name(
        name,
        silent=False
        ) -> dict:
    """ Describes the security group based on its name. """
    client = boto3.client('ec2')

    try:
        response = client.describe_security_groups(GroupNames=[name])
        return response

    except Exception as e:
        if not silent:
            print(e)


def describe_instance_by_id(
        instance_id,
        silent=False
        ):
    """ Describes the instance based on its ID. """
    client = boto3.client('ec2')

    try:
        response = client.describe_instances(
            InstanceIds=[instance_id]
        )

        return response

    except Exception as e:
        if not silent:
            print(e)


def create_key_pair(
        name="log8145-key-pair",
        silent=False
        ) -> dict:
    """ Creates a new key pair with a specific name. """
    client = boto3.client('ec2')

    try:
        response = client.create_key_pair(KeyName=name)

        pem_file = open(f"./keys/{name}.pem", "w")
        n = pem_file.write(response['KeyMaterial'])
        pem_file.close()

        return f"./keys/{name}.pem"
    except Exception as e:
        if not silent:
            print(e)


def create_ec2_instances(
        security_group_id,
        key_name,
        instance_type="t2.micro",
        count=1,
        ami="ami-0149b2da6ceec4bb0",
        silent=False,
        user_data=""
        ) -> dict:
    """ Creates proposed number of AWS instances of specified type with a given security group ID. """
    client = boto3.client('ec2')

    try:
        response = client.run_instances(
            ImageId=ami,
            InstanceType=instance_type,
            KeyName=key_name,
            MaxCount=count,
            MinCount=count,
            Monitoring={
                'Enabled': True
            },
            SecurityGroupIds=[
                security_group_id,
            ],
            UserData=user_data
        )
        return response

    except Exception as e:
        if not silent:
            print(e)


def wait_for_instances(
        ids,
        state,
        silent=False
        ) -> dict:
    """ Makes the program wait until instances specified by ids are all in the proposed state. """
    client = boto3.client('ec2')

    try:
        waiter = client.get_waiter(state)
        waiter.wait(
            InstanceIds=ids,
            WaiterConfig={
                'Delay': 10,
                'MaxAttempts': 30
            }
        )
    except Exception as e:
        if not silent:
            print(e)


def terminate_ec2_instances(instance_ids, silent=False) -> dict:
    """ Terminates instances based on specified IDs. """
    client = boto3.client('ec2')

    try:
        response = client.terminate_instances(InstanceIds=instance_ids)
        return response
    except Exception as e:
        if not silent:
            print(e)


def delete_security_group(group_id, silent=False) -> dict:
    """ Deletes security group based on its ID. """
    client = boto3.client('ec2')

    try: 
        response = client.delete_security_group(GroupId=group_id)
        return response

    except Exception as e:
        if not silent:
            print(e)


def delete_key_pair(key_pair_name, silent=False) -> dict:
    """ Deletes key pair based on its name. """
    client = boto3.client('ec2')

    try: 
        response = client.delete_key_pair(KeyName=key_pair_name)
        return response

    except Exception as e:
        if not silent:
            print(e)
