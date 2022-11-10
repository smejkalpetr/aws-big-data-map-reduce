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

    ##----------% UTILITY METHODS: %----------##
    def setup_vm_with_script(self, vm_public_ip):
        os.chmod(self.constants.KEY_PAIR_PATH, 0o400)
        subprocess.check_call([self.constants.SSH_SETUP_SCRIPT_PATH, vm_public_ip])

    ##----------------------------------------##
    ##---------% INITIALIZE METHODS: %--------##
    def check_default_vpc(self):
        self.constants.VPC_ID = self.utilities.get_vpc()
    def check_key_pair(self):
        self.utilities.print_info("Resolving Key Pair...")

        if self.constants.KEY_PAIR_PATH is None:
            self.utilities.print_error("There is no Key Pair path specified. Specify one and then try again.")
            return

        if not os.path.exists(self.constants.KEY_PAIR_PATH):
            self.utilities.print_info("Creating new Key Pair.")
            self.utilities.create_key_pair()
            self.utilities.print_info("The new private key has been saved to ./keys directory.")

    def check_security_group(self):
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
        self.utilities.print_info("Initializing...")

        self.check_default_vpc()
        self.check_key_pair()
        self.check_security_group()

        self.utilities.print_info("Initialization done.")

    ##----------------------------------------##
    ##----------% SHUTDOWN METHODS: %---------##
    def auto_shutdown(self):
        self.terminate_ec2_instances()

        if self.constants.SECURITY_GROUP_ID is not None:
            self.delete_security_group()

        self.delete_key_pair()

    def terminate_ec2_instances(self):
        self.utilities.terminate_ec2_instances(self.instance_id)

        # self.utilities.print_info("Waiting for " + self.instance_id + " instance to terminate...")
        self.utilities.wait_for_instances(self.instance_id, 'instance_terminated')

    def delete_security_group(self):
        self.utilities.delete_security_group(self.constants.SECURITY_GROUP_ID, silent=True)
        self.utilities.print_info("Security Group " + self.constants.SECURITY_GROUP_NAME + " has been deleted.")

    def delete_key_pair(self):
        self.utilities.delete_key_pair(self.constants.KEY_PAIR_NAME, silent=True)

        cctp1_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        keys_path = os.path.abspath(os.path.join(cctp1_path, 'keys'))
        os.remove(os.path.join(keys_path, self.constants.KEY_PAIR_NAME + '.pem'))

        self.utilities.print_info("Key Pair " + self.constants.KEY_PAIR_NAME + " has been deleted.")

    ##----------------------------------------##
    ##------------% SETUP METHODS: %----------##
    def auto_setup(self):
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
        self.setup_vm_with_script(self.instance_public_ip)
        self.utilities.print_info("Hadoop and Spark are now ready.")

    ##----------------------------------------##
    ##-------% CONTROLLER MAIN METHOD: %------##
    def run(self):
        self.initialize_env()
        self.auto_setup()
        # self.auto_shutdown()

    ##----------------------------------------##
