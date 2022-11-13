import pyt.constants
import pyt.utilities
import os.path
import os
import subprocess

# this class directs the flow of the whole program
class Controller:
    constants = pyt.constants.Constants
    utilities = pyt.utilities
    instances = None
    instance_id = None
    instance_public_ip = None

    def run_script_on_local(self, script_path, arg, log_path):
        """ Runs bash script specified in the script_path and sends additional arguments to the script
            to store the logs of the running script. """
        os.chmod(script_path, 0o777)
        subprocess.check_call([script_path, arg, log_path])

    def run_script_on_vm(self, vm_public_ip, script_path, log_path, arg1="", arg2=""):
        """ Runs bash script specified in the script_path on an AWS instance specified by vm_public_ip
         and sends additional arguments to the script to store the logs of the running script. """
        os.chmod(self.constants.KEY_PAIR_PATH, 0o400)
        subprocess.check_call([self.constants.SCRIPT_EXECUTE_ON_REMOTE, vm_public_ip, script_path, log_path, arg1, arg2])

    def check_default_vpc(self):
        """ Checks and sets the VPC from AWS."""
        self.constants.VPC_ID = self.utilities.get_vpc()

    def check_key_pair(self):
        """ Creates a new key pair in AWS. """
        self.utilities.print_info("Resolving Key Pair...")

        if self.constants.KEY_PAIR_PATH is None:
            self.utilities.print_error("There is no Key Pair path specified. Specify one and then try again.")
            return

        if not os.path.exists(self.constants.KEY_PAIR_PATH):
            self.utilities.print_info("Creating new Key Pair.")
            self.utilities.create_key_pair()
            self.utilities.print_info("The new private key has been saved to ./keys directory.")

    def check_security_group(self):
        """ Checks if security group exists and if not, creates one."""
        self.utilities.print_info("Resolving Security Group...")

        if self.constants.SECURITY_GROUP_NAME is None:
            self.utilities.print_info("Creating new Security Group...")
            self.constants.SECURITY_GROUP_ID = self.utilities.create_security_group(self.constants.VPC_ID, silent=True)['GroupId']
            self.utilities.print_info("New Security Group with ID" + self.constants.SECURITY_GROUP_ID + " has been created.")

        if self.constants.SECURITY_GROUP_NAME is not None:
            response = self.utilities.describe_security_group_id_by_name(self.constants.SECURITY_GROUP_NAME, silent=True)
            if response is not None:
                self.constants.SECURITY_GROUP_ID = response['SecurityGroups'][0]['GroupId']
            else:
                self.utilities.print_info("Creating new Security Group...")
                self.constants.SECURITY_GROUP_ID = (self.utilities.create_security_group(self.constants.VPC_ID, silent=True))['GroupId']
                self.utilities.print_info("New Security Group " + self.constants.SECURITY_GROUP_NAME + " has been created.")

    def initialize_env(self):
        """ Initialises the AWS by getting the VPC and setting the security group and key pair."""
        self.utilities.print_info("Initializing...")

        self.check_default_vpc()
        self.check_key_pair()
        self.check_security_group()

        self.utilities.print_info("Initialization done.")


    def download_datasets(self):
        """ Downloads WordCount datasets on a running VM. """
        os.chmod(self.constants.SCRIPT_DOWNLOAD_DATASETS, 0o777)

        with open(self.constants.URLS_DATASETS_PATH) as file:
            cnt = 0
            for line in file:
                self.run_script_on_vm(
                    self.instance_public_ip,
                    self.constants.SCRIPT_DOWNLOAD_DATASETS,
                    f"{self.constants.LOG_DOWNLOAD_DATASETS}_{cnt}.log",
                    line.rstrip(),
                    f'input_file{cnt}.txt'
                )
                cnt = cnt + 1

    def wordcount_linux_run(self):
        """ Runs the WordCount algorithm using Linux on VM. """
        self.run_script_on_vm(
            self.instance_public_ip,
            self.constants.SCRIPT_WORDCOUNT_LINUX,
            self.constants.LOG_WORDCOUNT_LINUX
        )

    def wordcount_hadoop_run(self):
        """ Runs the WordCount algorithm using Hadoop on VM. """
        self.run_script_on_vm(
            self.instance_public_ip,
            self.constants.SCRIPT_WORDCOUNT_HADOOP,
            self.constants.LOG_WORDCOUNT_HADOOP
        )

    def wordcount_spark_prepare(self):
        """ Prepares"""
        self.run_script_on_local(
            self.constants.SCRIPT_WORDCOUNT_SPARK_PREPARE,
            self.instance_public_ip,
            self.constants.LOG_WORDCOUNT_SPARK_PREPARE
        )

    def wordcount_spark_run(self):
        """ Runs the WordCount algorithm using Spark on VM. """
        self.run_script_on_vm(
            self.instance_public_ip,
            self.constants.SCRIPT_WORDCOUNT_SPARK,
            self.constants.LOG_WORDCOUNT_SPARK
        )

    def social_network_problem_prepare(self):
        """ Prepares the VM environment for executing the Social Network Problem. """
        self.run_script_on_local(
            self.constants.SCRIPT_SOCIAL_NETWORK_PROBLEM_PREPARE,
            self.instance_public_ip,
            self.constants.LOG_SOCIAL_NETWORK_PROBLEM_PREPARE
        )

    def social_network_problem_run(self):
        """ Runs the Social Network Problem algorithm on VM. """
        self.run_script_on_vm(
            self.instance_public_ip,
            self.constants.SCRIPT_SOCIAL_NETWORK_PROBLEM,
            self.constants.LOG_SOCIAL_NETWORK_PROBLEM
        )

    def auto_shutdown(self):
        """ Shuts down the application by terminating the created instance,
            deleting security group and key pair on AWS. """
        self.terminate_ec2_instances()

        if self.constants.SECURITY_GROUP_ID is not None:
            self.delete_security_group()

        self.delete_key_pair()

    def terminate_ec2_instances(self):
        """ Terminates specified instance and waits for it to be terminates until proceeding with the program. """
        self.utilities.print_info("Waiting for " + self.instance_id + " instance to terminate...")
        self.utilities.terminate_ec2_instances([self.instance_id], silent=True)

        self.utilities.wait_for_instances([self.instance_id], 'instance_terminated', silent=True)
        self.utilities.print_info("The instance has been terminated.")

    def delete_security_group(self):
        """ Deletes the security group in AWS. """
        self.utilities.delete_security_group(self.constants.SECURITY_GROUP_ID, silent=True)
        self.utilities.print_info("Security Group " + self.constants.SECURITY_GROUP_NAME + " has been deleted.")

    def delete_key_pair(self):
        """ Deletes the key pair group in AWS. """
        self.utilities.delete_key_pair(self.constants.KEY_PAIR_NAME, silent=True)

        cctp1_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        keys_path = os.path.abspath(os.path.join(cctp1_path, 'keys'))
        os.remove(os.path.join(keys_path, self.constants.KEY_PAIR_NAME + '.pem'))

        self.utilities.print_info("Key Pair " + self.constants.KEY_PAIR_NAME + " has been deleted.")

    def auto_setup(self):
        """ Runs the automated implementation of the wordcount problem and the social network problem
            on a newly created AWS instance."""
        self.utilities.print_info("Creating M4.large instance...")

        response = self.utilities.create_ec2_instances(
            self.constants.SECURITY_GROUP_ID,
            self.constants.KEY_PAIR_NAME,
            self.constants.M4_LARGE
        )

        self.instance_id = response['Instances'][0]['InstanceId']
        self.utilities.print_info(f"Created instance with ID: {self.instance_id}.")

        self.utilities.print_info("Waiting for the instance to start running...")
        self.utilities.wait_for_instances([self.instance_id], 'instance_running')
        self.utilities.wait_for_instances([self.instance_id], 'instance_status_ok')
        self.utilities.wait_for_instances([self.instance_id], 'system_status_ok')
        self.utilities.print_info("The instance is now running.")

        self.instance_public_ip = self.utilities.describe_instance_by_id(self.instance_id)['Reservations'][0]['Instances'][0]['PublicIpAddress']

        self.utilities.print_info(f"Installing Hadoop and Spark on the instance with public IP: {self.instance_public_ip} (see logs/vm_setup.log for more details)...")
        self.run_script_on_vm(self.instance_public_ip, self.constants.SCRIPT_VM_SETUP, self.constants.LOG_VM_SETUP)
        self.utilities.print_info("Hadoop and Spark are now ready.")

        self.utilities.print_info("Downloading datasets for WordCount...")
        self.download_datasets()
        self.utilities.print_info("Done downloading datasets.")

        self.utilities.print_info("Running WordCount problem on Linux...")
        self.wordcount_linux_run()
        self.utilities.print_info("WordCount on Linux done (see ./logs/wordcount_linux.log for details).")

        self.utilities.print_info("Running WordCount problem on Hadoop...")
        self.wordcount_hadoop_run()
        self.utilities.print_info("WordCount on Hadoop done (see ./logs/wordcount_hadoop.log for details).")

        self.utilities.print_info("Running WordCount problem on Spark...")
        self.wordcount_spark_run()
        self.utilities.print_info("WordCount on Spark done (see ./logs/wordcount_spark.log for details).")

        self.utilities.print_info("Preparing the Social Network Problem's files...")
        self.social_network_problem_prepare()
        self.utilities.print_info("Social Network Problem's preparation done (see ./logs/social_network_problem_prepare.log for details).")

        self.utilities.print_info("Solving the Social Network Problem using map reduce...")
        self.social_network_problem_run()
        self.utilities.print_info("Social Network Problem solving done (see ./logs/social_network_problem.log for results and details).")

    def run(self):
        """ Runs the whole application implementation. """
        self.initialize_env()
        self.auto_setup()
        self.auto_shutdown()
