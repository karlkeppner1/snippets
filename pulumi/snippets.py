import pulumi
import pulumi_aws as aws
stackname = 'foo'

kms_key = aws.kms.Key(
    f'{stackname}-key', # str - resource name
    opts = None, # dict - https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    customer_master_key_spec = 'SYMMETRIC_DEFAULT', # must be symetric to be used in EKS
    deletion_window_in_days = 30, # Duration in days after which the key is deleted after destruction of the resource, must be between 7 and 30 days. Defaults to 30 days.
    description = f'Key to be used by EKS cluster {stackname}', # str - yo dawg... it's a description
    enable_key_rotation = True, # bool - defaults to false
    is_enabled = True, # bool - defaults to true
    key_usage = 'ENCRYPT_DECRYPT', # ENCRYPT_DECRYPT or SIGN_VERIFY, defaults to ENCRYPT_DECRYPT
    policy = None, # A key policy JSON document. If you do not provide a key policy, AWS KMS attaches a default key policy to the CMK.
    tags = {'Name': f'{stackname}-key', 'foo': 'bar'} # dict - put in required tags
    )

cluster_sg = aws.ec2.SecurityGroup(
    f'{stackname}-control-plane-sg', # str - resource name
    opts = None, # dict - https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    description = None, # str - yo dawg... it's a description
  # egress = [{cidr_blocks - list, description - str, from_port - float, ipv6_cidr_blocks - list, prefix_list_ids - list, protocol - str, security_groups - list, self - bool, to_port - float}]
    egress = [
        {[cidr_blocks], 'description', from_port, [ipv6_cidr_blocks], [prefix_list_ids], 'protocol', [security_groups], self, to_port},
        {[cidr_blocks], 'description', from_port, [ipv6_cidr_blocks], [prefix_list_ids], 'protocol', [security_groups], self, to_port}
    ], # list of dict - set self to True if you want the SG to reference itself, Can be specified multiple times for each egress rule
  # ingress = [{cidr_blocks - list, description - str, from_port - float, ipv6_cidr_blocks - list, prefix_list_ids - list, protocol - str, security_groups - list, self - bool, to_port - float}]
    ingress = [
        {[cidr_blocks], 'description', from_port, [ipv6_cidr_blocks], [prefix_list_ids], 'protocol', [security_groups], self, to_port},
        {[cidr_blocks], 'description', from_port, [ipv6_cidr_blocks], [prefix_list_ids], 'protocol', [security_groups], self, to_port}
    ], # list of dict - set self to True if you want the SG to reference itself, Can be specified multiple times for each egress rule
    name = None, # str - If you change this, it will cause a "replace" in AWS!
    name_prefix = None, # str - Creates a unique name beginning with the specified prefix. Conflicts with name
    revoke_rules_on_delete = None, # bool - Instruct this provider to revoke all of the Security Groups attached ingress and egress rules before deleting the rule itself. This is normally not needed, however certain AWS services such as Elastic Map Reduce may automatically add required rules to security groups used with the service, and those rules may contain a cyclic dependency that prevent the security groups from being destroyed without removing the dependency first. Default = false
    tags = {'Name': f'{stackname}-control-plane-sg', 'foo': 'bar'}, # dict - put in required tags
    vpc_id = None, # str - VPC in which to place the security group
)

cluster_sg_rule1 = aws.ec2.SecurityGroupRule(
    'resource_name', # str -The name of the resource.
    opts = pulumi.ResourceOptions(depends_on=[cluster_sg]), # https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    cidr_blocks = None, # list of str - List of CIDR blocks. Cannot be specified with source_security_group_id.
    description = None, # str - yo dawg... it's a description
    from_port = None, # float - The start port (or ICMP type number if protocol is “icmp” or “icmpv6”).
    ipv6_cidr_blocks = None, # list of str - List of IPv6 CIDR blocks.
    prefix_list_ids = None, # list of strs - prefix list IDs (for allowing access to VPC endpoints). Only valid with egress.
    protocol = None, # str - The protocol. If not icmp, icmpv6, tcp, udp, or all use the protocol number
    security_group_id = None, # str - The security group to apply this rule to.
    self = None, # bool - If true, the security group itself will be added as a source to this ingress rule. Cannot be specified with source_security_group_id.
    source_security_group_id = None, # str - The security group id to allow access to/from, depending on the type. Cannot be specified with cidr_blocks and self.
    to_port = None, # float - The end port (or ICMP code if protocol is “icmp”).
    type = None # str - The type of rule being created. Valid options are ingress (inbound) or egress (outbound).
)

ekscluster = aws.eks.Cluster(
    f'{stackname}-eks-cluster', # name of the resource
    opts = None, # https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    enabled_cluster_log_types = ['api', 'audit', 'authenticator', 'controlManager', 'scheduler'], # list - https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html 
    encryption_config = {'provider': {'key_arn': kms_key.arn}, 'resources': ['secrets']}, # dict - encrypt master nodes in cluster with KMS CMK shared to AWS account
    name = f'{stackname}-eks-cluster', # str - name of the cluster
    role_arn = None, # str - required, 
    tags = {'Name': f'{stackname}-eks-cluster', 'foo': 'bar'}, # dict - put in required tags
    version = None, # str - version of EKS to create, defaults to latest
    vpc_config = {
        'clusterSecurityGroupId': None, # str - The cluster security group that was created by Amazon EKS for the cluster. The cluster security group that was created by Amazon EKS for the cluster.
        'endpointPrivateAccess': None, # bool - Indicates whether or not the Amazon EKS private API server endpoint is enabled. Default is false.
        'endpointPublicAccess': None, # bool - Indicates whether or not the Amazon EKS public API server endpoint is enabled. Default is true.
        'publicAccessCidrs': None, # list of str - cidrs of addresses that may call the API server, requires endpointPublicAccess set to True
        'security_group_ids': None, # list of str - List of security group IDs for the cross-account elastic network interfaces that Amazon EKS creates to use to allow communication between your worker nodes and the Kubernetes control plane.
        'subnet_ids': None, # list of str - List of subnet IDs. Must be in at least two different availability zones. Amazon EKS creates cross-account elastic network interfaces in these subnets to allow communication between your worker nodes and the Kubernetes control plane.
        'vpc_id': None} # str - conflicts with subnet_ids
)

iam_role = aws.iam.Role(
    'resource_name', # str - The name of the resource
    opts = None, # https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    assume_role_policy = """{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "ec2.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }]
    }""", # str - The policy that grants an entity permission to assume the role.
    description = None, # str - yo dawg... it's a description
    force_detach_policies = None, # bool - Specifies to force detaching any policies the role has before destroying it. Defaults to false
    max_session_duration = None, # float - The maximum session duration (in seconds) that you want to set for the specified role. If you do not specify a value for this setting, the default maximum of one hour is applied. This setting can have a value from 1 hour to 12 hours.
    name = None, # str - The name of the role. If omitted, this provider will assign a random, unique name.
    name_prefix = None, # str - Creates a unique name beginning with the specified prefix. Conflicts with name
    path = None, # str - The path to the role. See https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html
    permissions_boundary = None, # str - The ARN of the policy that is used to set the permissions boundary for the role.
    tags = {'Name': f'{stackname}-eks-cluster', 'foo': 'bar'}, # dict - put in required tags
)

policy =  aws.iam.Policy(
    'resource_name', # str – The name of the resource.
    opts=None, # https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    description=None, # str - yo dawg... it's a description
    name=None, # str – The name of the policy. If omitted, this provider will assign a random, unique name.
    name_prefix=None, # str – Creates a unique name beginning with the specified prefix. Conflicts with name.
    path=None, # str – Path in which to create the policy. See IAM Identifiers for more information.
    policy=None, # dict – The policy document.
)

aws.iam.RolePolicyAttachment(
    'resource_name', # str - The name of the resource
    opts = None, # https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    policy_arn = 'arn:aws:iam::aws:policy/AmazonEKSClusterPolicy', # str – The ARN of the policy you want to apply
    role = iam_role.name, # str – The role the policy should be applied to
)

instance_profile = aws.iam.InstanceProfile(
    'resource_name', # str – The name of the resource.
    opts = None, # https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    name = None, # str – The profile’s name. If omitted, this provider will assign a random, unique name.
    name_prefix = None, # str – Creates a unique name beginning with the specified prefix. Conflicts with name.
    path = None, # str – Path in which to create the profile.
    role = None, # str – The role name to include in the profile.
    roles = None # list – A list of role names to include in the profile. The current default is 1. If you see an error message similar to Cannot exceed quota for InstanceSessionsPerInstanceProfile: 1, then you must contact AWS support and ask for a limit increase.
)

launch_template = aws.ec2.LaunchTemplate(
    'resource_name', # str – The name of the resource.
    opts = None, # https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    block_device_mappings = None, # list – Specify volumes to attach to the instance besides the volumes specified by the AMI. See Block Devices below for details.
    capacity_reservation_specification = None, # dict – Targeting for EC2 capacity reservations. See Capacity Reservation Specification below for more details.
    cpu_options = None, # dict – The CPU options for the instance. See CPU Options below for more details.
    credit_specification = None, # dict – Customize the credit specification of the instance. See Credit Specification below for more details.
    description = None, # str - yo dawg... it's a description
    disable_api_termination = None, # bool – If true, enables EC2 Instance Termination Protection
    ebs_optimized = None, # str – If true, the launched EC2 instance will be EBS-optimized.
    elastic_gpu_specifications = None, # list – The elastic GPU to attach to the instance. See Elastic GPU below for more details.
    elastic_inference_accelerator = None, # dict – Configuration block containing an Elastic Inference Accelerator to attach to the instance. See Elastic Inference Accelerator below for more details.
    iam_instance_profile = None, # dict – The IAM Instance Profile to launch the instance with. See Instance Profile below for more details.
    image_id = None, # str – The AMI from which to launch the instance.
    instance_initiated_shutdown_behavior = None, # [str – Shutdown behavior for the instance. Can be stop or terminate. (Default: stop).
    instance_market_options = None, # dict – The market (purchasing) option for the instance. See Market Options below for details.
    instance_type = None, # str – The type of the instance.
    kernel_id = None, # str – The kernel ID.
    key_name = None, # str – The key name to use for the instance.
    license_specifications = None, # list – A list of license specifications to associate with. See License Specification below for more details.
    monitoring = None, # dict – The monitoring option for the instance. See Monitoring below for more details.
    name = None, # str – The name of the launch template. If you leave this blank, this provider will auto-generate a unique name.
    name_prefix = None, # str – Creates a unique name beginning with the specified prefix. Conflicts with name.
    network_interfaces = [{
        'associate_public_ip_address': None, # bool - Associate a public ip address with the network interface. Boolean value.
        'delete_on_termination': None, # bool - Whether the network interface should be destroyed on instance termination.
        'description': None, # str - Description of the network interface.
        'device_index': None, # float - The integer index of the network interface attachment.
        'ipv6_addresses': None, # list of str - One or more specific IPv6 addresses from the IPv6 CIDR block range of your subnet. Conflicts with ipv6_address_count
        'ipv6_address_count': None, # float - The number of IPv6 addresses to assign to a network interface. Conflicts with ipv6_addresses
        'network_interface_id': None, # str - The ID of the network interface to attach.
        'private_ip_address': None, # str - The primary private IPv4 address.
        'ipv4_address_count': None, # float - The number of secondary private IPv4 addresses to assign to a network interface. Conflicts with ipv4_addresses
        'ipv4_addresses': None, # list of str - One or more private IPv4 addresses to associate. Conflicts with ipv4_address_count
        'security_groups': None, # list - A list of security group IDs to associate.
        'subnet_id': None # str - The VPC Subnet ID to associate.
    }], # list – Customize network interfaces to be attached at instance boot time. See Network Interfaces below for more details.
    placement = None, # dict – The placement of the instance. See Placement below for more details.
    ram_disk_id = None, # str – The ID of the RAM disk.
    security_group_names = None, # list – A list of security group names to associate with. If you are creating Instances in a VPC, use vpc_security_group_ids instead.
    tag_specifications = [{'resource_type': 'instance', 'tags': {'foo': 'bar'}}, {'resource_type': 'volume', 'tags': {'foo': 'bar'}}], # list – The tags to apply to the resources during launch. See Tag Specifications below for more details.
    tags = None, # dict – A mapping of tags to assign to the launch template.
    user_data = None, # str – The Base64-encoded user data to provide when launching the instance.
    vpc_security_group_ids = None, # list – A list of security group IDs to associate with. conflicts with network_interfaces.security_groups
)

ec2_instance = aws.ec2.Instance(  # https://www.pulumi.com/docs/reference/pkg/python/pulumi_aws/ec2/#pulumi_aws.ec2.Instance
    'resource_name', # str) – The name of the resource.
    opts=None, # https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    ami=None, # str - The AMI to use for the instance.
    associate_public_ip_address=None, # bool - Associate a public ip address with an instance in a VPC. Boolean value.
    availability_zone=None, # str - The AZ to start the instance in.
    cpu_core_count=None, # float - Sets the number of CPU cores for an instance. This option is only supported on creation of instance type that support CPU Options CPU Cores and Threads Per CPU Core Per Instance Type - specifying this option for unsupported instance types will return an error from the EC2 API.
    cpu_threads_per_core=None, # float - If set to to 1, hyperthreading is disabled on the launched instance. Defaults to 2 if not set. See Optimizing CPU Options for more information.
    credit_specification=None, # dict - Customize the credit specification of the instance. See Credit Specification below for more details.
    disable_api_termination=None, # bool - If true, enables EC2 Instance Termination Protection
    ebs_block_devices=None, # list - Additional EBS block devices to attach to the instance. Block device configurations only apply on resource creation. See Block Devices below for details on attributes and drift detection.
    ebs_optimized=None, # bool - If true, the launched EC2 instance will be EBS-optimized. Note that if this is not set on an instance type that is optimized by default then this will show as disabled but if the instance type is optimized by default then there is no need to set this and there is no effect to disabling it. See the EBS Optimized section of the AWS User Guide for more information.
    ephemeral_block_devices=None, # list - Customize Ephemeral (also known as “Instance Store”) volumes on the instance. See Block Devices below for details.
    get_password_data=None, # bool - If true, wait for password data to become available and retrieve it. Useful for getting the administrator password for instances running Microsoft Windows. The password data is exported to the password_data attribute. See GetPasswordData for more information.
    hibernation=None, # bool - If true, the launched EC2 instance will support hibernation.
    host_id=None, # str - The Id of a dedicated host that the instance will be assigned to. Use when an instance is to be launched on a specific dedicated host.
    iam_instance_profile=None, # dict - The IAM Instance Profile to launch the instance with. Specified as the name of the Instance Profile. Ensure your credentials have the correct permission to assign the instance profile according to the EC2 documentation, notably iam:PassRole.
    instance_initiated_shutdown_behavior=None, # str - Shutdown behavior for the instance. Amazon defaults this to stop for EBS-backed instances and terminate for instance-store instances. Cannot be set on instance-store instances. See Shutdown Behavior for more information.
    instance_type=None, # str - The type of instance to start. Updates to this field will trigger a stop/start of the EC2 instance.
    ipv6_address_count=None, # float - (Optional) A number of IPv6 addresses to associate with the primary network interface. Amazon EC2 chooses the IPv6 addresses from the range of your subnet.
    ipv6_addresses=None, # list - Specify one or more IPv6 addresses from the range of the subnet to associate with the primary network interface
    key_name=None, # str - The key name of the Key Pair to use for the instance; which can be managed using the ec2.KeyPair resource.
    monitoring=None, # bool - If true, the launched EC2 instance will have detailed monitoring enabled. (Available since v0.6.0)
    network_interfaces=None, # list - Customize network interfaces to be attached at instance boot time. See Network Interfaces below for more details.
    placement_group=None, # str - The Placement Group to start the instance in.
    private_ip=None, # str - Private IP address to associate with the instance in a VPC.
    root_block_device=None, # dict - Customize details about the root block device of the instance. See Block Devices below for details.
    security_groups=None, # list - A list of security group names (EC2-Classic) or IDs (default VPC) to associate with.
    source_dest_check=None, # bool - Controls if traffic is routed to the instance when the destination address does not match the instance. Used for NAT or VPNs. Defaults true.
    subnet_id=None, # str - The VPC Subnet ID to launch in.
    tags=None, # dict - A mapping of tags to assign to the resource.
    tenancy=None, # str - The tenancy of the instance (if the instance is running in a VPC). An instance with a tenancy of dedicated runs on single-tenant hardware. The host tenancy is not supported for the import-instance command.
    user_data=None, # str - The user data to provide when launching the instance. Do not pass gzip-compressed data via this argument; see user_data_base64 instead.
    user_data_base64=None, # str - Can be used instead of user_data to pass base64-encoded binary data directly. Use this instead of user_data whenever the value is not a valid UTF-8 string. For example, gzip-encoded user data must be base64-encoded and passed via this argument to avoid corruption.
    volume_tags=None, # dict - A mapping of tags to assign to the devices created by the instance at launch time.
    vpc_security_group_ids=None, # list - A list of security group IDs to associate with.
)

instance_profile = aws.iam.InstanceProfile(
    'resource_name', # str – The name of the resource.
    opts=None, # 
    name=None, # str - The profile’s name. If omitted, this provider will assign a random, unique name.
    name_prefix=None, # str - Creates a unique name beginning with the specified prefix. Conflicts with name.
    path=None, # str - Path in which to create the profile.
    role=None, # dict - The role name to include in the profile.
    roles=None # list - A list of role names to include in the profile. The current default is 1. If you see an error message similar to Cannot exceed quota for InstanceSessionsPerInstanceProfile: 1, then you must contact AWS support and ask for a limit increase.
)

autoscaling_group = aws.autoscaling.Group(
    'resource_name', # str – The name of the resource.
    opts = None, # https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    availability_zones = None, # list – A list of one or more availability zones for the group. This parameter should not be specified when using vpc_zone_identifier.
    default_cooldown = None, # float – The amount of time, in seconds, after a scaling activity completes before another scaling activity can start.
    desired_capacity = None, # float – The number of Amazon EC2 instances that should be running in the group. (See also Waiting for Capacity below.)
    enabled_metrics = None, # list – A list of metrics to collect. The allowed values are GroupDesiredCapacity, GroupInServiceCapacity, GroupPendingCapacity, GroupMinSize, GroupMaxSize, GroupInServiceInstances, GroupPendingInstances, GroupStandbyInstances, GroupStandbyCapacity, GroupTerminatingCapacity, GroupTerminatingInstances, GroupTotalCapacity, GroupTotalInstances.
    force_delete = None, # bool – Allows deleting the autoscaling group without waiting for all instances in the pool to terminate. You can force an autoscaling group to delete even if it’s in the process of scaling a resource. Normally, this provider drains all the instances before deleting the group. This bypasses that behavior and potentially leaves resources dangling.
    health_check_grace_period = None, # float – Time (in seconds) after instance comes into service before checking health.
    health_check_type = None, # str – “EC2” or “ELB”. Controls how health checking is done.
    initial_lifecycle_hooks = None, # list – One or more Lifecycle Hooks to attach to the autoscaling group before instances are launched. The syntax is exactly the same as the separate ``autoscaling.LifecycleHook` <https://www.terraform.io/docs/providers/aws/r/autoscaling_lifecycle_hook.html>`_ resource, without the autoscaling_group_name attribute. Please note that this will only work when creating a new autoscaling group. For all other use-cases, please use autoscaling.LifecycleHook resource.
    launch_configuration = None, # str – The name of the launch configuration to use.
    launch_template = None, # dict – Nested argument containing launch template settings along with the overrides to specify multiple instance types and weights. Defined below.
    load_balancers = None, # list – A list of elastic load balancer names to add to the autoscaling group names. Only valid for classic load balancers. For ALBs, use target_group_arns instead.
    max_instance_lifetime = None, # float – The maximum amount of time, in seconds, that an instance can be in service, values must be either equal to 0 or between 604800 and 31536000 seconds.
    max_size = None, # float – The maximum size of the auto scale group.
    metrics_granularity = None, # str – The granularity to associate with the metrics to collect. The only valid value is 1Minute. Default is 1Minute.
    min_elb_capacity = None, # float – Setting this causes this provider to wait for this number of instances from this autoscaling group to show up healthy in the ELB only on creation. Updates will not wait on ELB instance number changes. (See also Waiting for Capacity below.)
    min_size = None, # float – The minimum size of the auto scale group. (See also Waiting for Capacity below.)
    mixed_instances_policy = None, # dict – Configuration block containing settings to define launch targets for Auto Scaling groups. Defined below.
    name = None, # str – The name of the auto scaling group. By default generated by this provider.
    name_prefix = None, # str – Creates a unique name beginning with the specified prefix. Conflicts with name.
    placement_group = None, # str – The name of the placement group into which you’ll launch your instances, if any.
    protect_from_scale_in = None, # bool – Allows setting instance protection. The autoscaling group will not select instances with this setting for terminination during scale in events.
    service_linked_role_arn = None, # str – The ARN of the service-linked role that the ASG will use to call other AWS services
    suspended_processes = None, # list – A list of processes to suspend for the AutoScaling Group. The allowed values are Launch, Terminate, HealthCheck, ReplaceUnhealthy, AZRebalance, AlarmNotification, ScheduledActions, AddToLoadBalancer. Note that if you suspend either the Launch or Terminate process types, it can prevent your autoscaling group from functioning properly.
    tags = None, # list – A list of tag blocks. Tags documented below.
    tags_collection = None, # list – A list of tag blocks (maps). Tags documented below.
    target_group_arns = None, # list – A list of alb.TargetGroup ARNs, for use with Application or Network Load Balancing.
    termination_policies = None, # list – A list of policies to decide how the instances in the auto scale group should be terminated. The allowed values are OldestInstance, NewestInstance, OldestLaunchConfiguration, ClosestToNextInstanceHour, OldestLaunchTemplate, AllocationStrategy, Default.
    vpc_zone_identifiers = None, # list – A list of subnet IDs to launch resources in.
    wait_for_capacity_timeout = None, # float – Setting this will cause this provider to wait for exactly this number of healthy instances from this autoscaling group in all attached load balancers on both create and update operations. (Takes precedence over min_elb_capacity behavior.) (See also Waiting for Capacity below.)
    wait_for_elb_capacity = None # float – Setting this will cause this provider to wait for exactly this number of healthy instances from this autoscaling group in all attached load balancers on both create and update operations. (Takes precedence over min_elb_capacity behavior.) (See also Waiting for Capacity below.)
)

fargate_profile = aws.eks.FargateProfile(
    'resource_name', # str – The name of the resource. REQUIRED
    opts = None, # https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    cluster_name = None, # str – Name of the EKS Cluster. REQUIRED
    fargate_profile_name = None, # str – Name of the EKS Fargate Profile. REQUIRED
    pod_execution_role_arn = None, # str – Amazon Resource Name (ARN) of the IAM Role that provides permissions for the EKS Fargate Profile. REQUIRED
    selectors = [{'namespace': 'fargate', 'labels': {'fargate': 'true'}}], # list – Configuration block(s) for selecting Kubernetes Pods to execute with this EKS Fargate Profile. Detailed below. REQUIRED
    subnet_ids = None, # list – Identifiers of private EC2 Subnets to associate with the EKS Fargate Profile. These subnets must have the following resource tag: kubernetes.io/cluster/CLUSTER_NAME (where CLUSTER_NAME is replaced with the name of the EKS Cluster). REQUIRED
    tags = None # dict – Key-value mapping of resource tags.
)

node_group = aws.eks.NodeGroup(
    'resource_name', # str – The name of the resource.
    opts  =  None, # https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    ami_type = None, # str - Type of Amazon Machine Image (AMI) associated with the EKS Node Group. Defaults to AL2_x86_64. Valid values: AL2_x86_64, AL2_x86_64_GPU
    cluster_name = None, # str – Name of the EKS Cluster. REQUIRED
    disk_size = None, # float - Disk size in GiB for worker nodes. Defaults to 20. Will only perform drift detection if a configuration value is provided.
    instance_types = None, # str - Set of instance types associated with the EKS Node Group. Defaults to ["t3.medium"]. Will only perform drift detection if a configuration value is provided. Currently, the EKS API only accepts a single value in the set.
    labels = None, # dict – Key-value mapping of Kubernetes labels. Only labels that are applied with the EKS API are managed by this argument. Other Kubernetes labels applied to the EKS Node Group will not be managed.
    node_group_name = None, # str – Name of the EKS Node Group. REQUIRED
    node_role_arn = None, # str – Amazon Resource Name (ARN) of the IAM Role that provides permissions for the EKS Node Group. REQUIRED
    release_version = None, # str – AMI version of the EKS Node Group. Defaults to latest version for Kubernetes version.
    remote_access = {'ec2SshKey': 'foo', 'sourceSecurityGroupIds': ['bar', 'baz']}, # dict – Configuration block with remote access settings. Detailed below.
    scaling_config = {'desiredSize': 2, 'max_size': 3, 'min_size': 1}, # dict – Configuration block with scaling settings. Detailed below. REQUIRED
    subnet_ids = None, # list – Identifiers of EC2 Subnets to associate with the EKS Node Group. These subnets must have the following resource tag: kubernetes.io/cluster/CLUSTER_NAME (where CLUSTER_NAME is replaced with the name of the EKS Cluster). REQUIRED
    tags = None, # dict – Key-value mapping of resource tags.
    version = None # str - Kubernetes version. Defaults to EKS Cluster Kubernetes version. Will only perform drift detection if a configuration value is provided.
)

ami = aws.get_ami(
    most_recent="true", owners=["137112412989"],
    filters=[{"name":"name","values":["amzn2-ami-hvm-*"]}]
)

dns_record = aws.route53.Record(
    'resource_name', # str – The name of the resource.
    opts=None, # https://www.pulumi.com/docs/reference/pkg/python/pulumi/#pulumi.ResourceOptions
    aliases=None, # list – An alias block. Conflicts with ttl & records. Alias record documented below.
    allow_overwrite=None, # bool – Allow creation of this record to overwrite an existing record, if any. This does not affect the ability to update the record using this provider and does not prevent other resources within this provider or manual Route 53 changes outside this provider from overwriting this record. false by default. This configuration is not recommended for most environments.
    failover_routing_policies=None, # list – A block indicating the routing behavior when associated health check fails. Conflicts with any other routing policy. Documented below.
    geolocation_routing_policies=None, # list – A block indicating a routing policy based on the geolocation of the requestor. Conflicts with any other routing policy. Documented below.
    health_check_id=None, # str – The health check the record should be associated with.
    latency_routing_policies=None, # list – A block indicating a routing policy based on the latency between the requestor and an AWS region. Conflicts with any other routing policy. Documented below.
    multivalue_answer_routing_policy=None, # bool – Set to true to indicate a multivalue answer routing policy. Conflicts with any other routing policy.
    name=None, # str – DNS domain name for a CloudFront distribution, S3 bucket, ELB, or another resource record set in this hosted zone.
    records=None, # list – A string list of records. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add "" inside the configuration string (e.g. "first255characters""morecharacters").
    set_identifier=None, # str – Unique identifier to differentiate records with routing policies from one another. Required if using failover, geolocation, latency, or weighted routing policies documented below.
    ttl=None, # float – The TTL of the record.
    type=None, # dict – PRIMARY or SECONDARY. A PRIMARY record will be served if its healthcheck is passing, otherwise the SECONDARY will be served.
    weighted_routing_policies=None, # list – A block indicating a weighted routing policy. Conflicts with any other routing policy. Documented below.
    zone_id=None # str – Hosted zone ID for a CloudFront distribution, S3 bucket, ELB, or Route 53 hosted zone.
)

pulumi.export('ekscluster vpc_config', ekscluster.vpc_config['clusterSecurityGroupId']) # vpc_config is kinda a dict but you can't use typical python dict.get() on it cause it's actually a pulumi.output.Output type object