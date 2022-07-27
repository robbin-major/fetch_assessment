# fetch_assessment

Greetings! 

This project aims to develop an automated program that deploys a Linux AWS EC2 instance with two volumes and two users using a YAML configuration file.

Here are some guidelines to follow:

Create a YAML file based on the configuration provided below for consumption by your application
You may modify the configuration, but do not do so to the extent that you fundamentally change the exercise
Include the YAML config file in your repo
Use Python and Boto3
Do not use configuration management, provisioning, or IaC tools such as Ansible, CloudFormation, Terraform, etc.

# This YAML configuration specifies a server with two volumes and two users
  server:
    instance_type: t2.micro
    ami_type: amzn2
    architecture: x86_64
    root_device_type: ebs
    virtualization_type: hvm
    min_count: 1
    max_count: 1
    volumes:
      - device: /dev/xvda
        size_gb: 10
        type: ext4
        mount: /
      - device: /dev/xvdf
        size_gb: 100
        type: xfs
        mount: /data
    users:
      - login: user1
        ssh_key: --user1 ssh public key goes here-- user1@localhost
      - login: user2
        ssh_key: --user2 ssh public key goes here-- user2@localhost




