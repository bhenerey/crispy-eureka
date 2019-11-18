import boto3

debug=True


def get_regions():
    ''' Get all the AWS regions '''

    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2')

    region_list=[]
    response = client.describe_regions()
    for region in response['Regions']:
        region_list.append(region['RegionName'])

    return(region_list)


def get_vpc_ids(region='us-east-1'):
    ''' Get the AWS VPC IDs '''

    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2', region_name=region)

    vpc_id_list=[]
    response = client.describe_vpcs()

    for vpc in response['Vpcs']:
        vpc_id_list.append(vpc['VpcId'])

    return vpc_id_list



def get_ec2_instances(vpcid, region='us-east-1'):
    ''' List EC2 instances by VPC '''


    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2', region_name=region)

    instance_list=[]
    response = client.describe_instances(
                    Filters=[
                        {
                            'Name': 'vpc-id',
                            'Values': [
                                vpcid,
                            ]
                        },
                    ]
                )

    for r in response['Reservations']:
        for instance in r['Instances']:
            instance_list.append(instance['InstanceId'])

    return instance_list

#TODO: This is still in progress. Not all ENIs have the same attributes.
def get_enis(vpcid, region='us-east-1'):
    ''' List EC2 instances by VPC '''


    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2', region_name=region)

    eni_list=[]
    response = client.describe_network_interfaces(
                    Filters=[
                        {
                            'Name': 'vpc-id',
                            'Values': [
                                vpcid,
                            ]
                        },
                    ]
                )

    interfaces = response['NetworkInterfaces']
    for i in interfaces:
        print(i.keys())
        #TODO: not all interfaces have the same attributes
    return len(response['NetworkInterfaces'])




if debug == True:
    region_list = ['us-east-1']
else:
    region_list = get_regions()

for r in region_list:
    print(r)
    print("")

    vpc_id_list=get_vpc_ids(region=r)

    for vpc_id in vpc_id_list:
        print(vpc_id, get_ec2_instances(vpc_id))
        print("")
