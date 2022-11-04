import boto3
# this file contains functions that call the AWS API

def print_info(message):
    print(f'[INFO] {message}')

def print_error(message):
    print(f'[Error] {message}')

def get_vpc(silent=False):
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
):
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

def describe_security_group_id_by_name(name, silent=False):
    client = boto3.client('ec2')

    try:
        response = client.describe_security_groups(GroupNames=[name])
        return response

    except Exception as e:
        if not silent:
            print(e)

def create_key_pair(name="log8145-key-pair", silent=False):
    client = boto3.client('ec2')

    try:
        response = client.create_key_pair(KeyName=name)

        pem_file = open(f"./keys/{name}.pem", "w")
        n = pem_file.write(response['KeyMaterial'])
        pem_file.close()

        if not silent:
            print_info("The new private key has been saved to ./keys directory.")

        return f"./keys/{name}.pem"
    except Exception as e:
        if not silent:
            print(e)

def create_ec2_instances(security_group_id,
                         key_name,
                         instance_type="t2.micro",
                         count=1,
                         ami="ami-0149b2da6ceec4bb0",
                         silent=False,
                         user_data=""
    ) -> dict:
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

def wait_for_instances(ids, state, silent=False):
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
    client = boto3.client('ec2')

    try:
        response = client.terminate_instances(InstanceIds=instance_ids)
        return response
    except Exception as e:
        if not silent:
            print(e)


def delete_security_group(group_id, silent=False):
    client = boto3.client('ec2')

    try: 
        response = client.delete_security_group(GroupId=group_id)
        return response

    except Exception as e:
        if not silent:
            print(e)

def delete_key_pair(key_pair_name, silent=False):
    client = boto3.client('ec2')

    try: 
        response = client.delete_key_pair(KeyName=key_pair_name)
        return response

    except Exception as e:
        if not silent:
            print(e)
