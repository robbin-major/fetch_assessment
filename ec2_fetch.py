import boto3
import yaml
ec2 = boto3.resource('ec2')
'''
# create a file to store the key locally
outfile = open('key.pem','w')

# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName='key')

# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
print(KeyPairOut)
outfile.write(KeyPairOut)
'''
fetch_client = boto3.resource('ec2', region_name= 'us-east-2')

with open('config.yaml', 'r') as f:
    fetchdata = yaml.safe_load(f)
    print(fetchdata["server"])
#3. Take the information from yaml file and convert it over to the format of the data that’s needed from the EC2 instances. Translate the info

server =  fetchdata['server']
ami_type = server['ami_type']
arc = server['architecture']
instanceType = server['instance_type']
root_device_type = server['root_device_type']
virtualization_type = server['virtualization_type']
serv_min_count = server['min_count']
serv_max_count = server['max_count']

volumes = server['volumes']
device1 = volumes[0]['device']
size_gb1 = volumes[0]['size_gb']
volumes_type1 = volumes[0]['type']
volumes_mount1 = volumes[0]['mount']

volumes = server['volumes']
device2 = volumes[1]['device']
size_gb2 = volumes[1]['size_gb']
volumes_type2 = volumes[1]['type']
volumes_mount2 = volumes[1]['mount']

user = server['users']
login1 = user[0]['login']
ssh_key1 = user[0]['ssh_key']

user = server['users']
login2 = user[1]['login']
ssh_key2 = user[1]['ssh_key']

# possible values: x86_64, and arm_64
# possible ami_types: amzn2, redhat, unbu20

if ami_type == 'amzn2'and arc == 'x86_64':
    ImageId ='ami-0b614a5d911900a9b'

if ami_type == 'amzn2' and arc == 'arm_64':
    ImageId = 'ami-02af65b2d1ebdfafc'

if ami_type == 'redhat8' and arc == 'x86_64':
    ImageId = 'ami-0ba62214afa52bec7'

if ami_type == 'ubun20' and arc == 'x86_64':
    ImageId = 'ami-0fb653ca2d3203ac1'



user_data = '#!/bin/bash\n'
# create user1
user_data += 'adduser %s\n'        % login1
#user_data += 'su - %s\n'           % (user1['login'])
user_data += 'mkdir /home/%s/.ssh\n' % login1
#user_data += 'chmod 700 .ssh\n'
user_data += 'touch /home/%s/.ssh/authorized_keys\n' % login1
#user_data += 'chmod 600 .ssh/authorized_keys\n'
user_data += 'echo %s > /home/%s/.ssh/authorized_keys\n' % (ssh_key1, login1)
# create user2
user_data += 'adduser %s\n'        % login2 
user_data += 'mkdir /home/%s/.ssh\n' % login2 
user_data += 'touch /home/%s/.ssh/authorized_keys\n' % login2 
user_data += 'echo %s > /home/%s/.ssh/authorized_keys\n' % (ssh_key2, login2 )

#fetch_client.run_instances(**fetchdata)
# create a new EC2 instance
instances = ec2.create_instances(
     ImageId = ImageId,
     MinCount=server['min_count'],
     MaxCount=server['max_count'],
     InstanceType=instanceType,
     UserData=user_data,
     KeyName='key',
     BlockDeviceMappings=[
            {
                'DeviceName': volumes[0]['device'],
                'Ebs': {
                    'VolumeSize':volumes[0]['size_gb']
                }
            },
            {
                'DeviceName': volumes[1]['device'],
                'Ebs': {
                    'VolumeSize': volumes[1]['size_gb']
                }
            }
        ]
 )
