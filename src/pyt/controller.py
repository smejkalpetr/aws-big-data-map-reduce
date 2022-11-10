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
    
    def check_sg_and_kp(self):
        if self.constants.KEY_PAIR_PATH is None:
            self.utilities.print_error("There is no Key Pair path specified. Specify one and then try again.")
            return

        if self.constants.SECURITY_GROUP_NAME is None:
            self.constants.SECURITY_GROUP_ID = (self.utilities.create_security_group(self.constants.VPC_ID, silent=True))['GroupId']

        if self.constants.SECURITY_GROUP_ID is None:
            response = self.utilities.describe_security_group_id_by_name(self.constants.SECURITY_GROUP_NAME, silent=True)
            if response is None:
                self.utilities.print_info("Creating new Security Group...")
                self.constants.SECURITY_GROUP_ID = (self.utilities.create_security_group(self.constants.VPC_ID, silent=True))['GroupId']
                self.utilities.print_info("New Security Group " + self.constants.SECURITY_GROUP_NAME + " has been created.")

            else:
                self.constants.SECURITY_GROUP_ID = response_sg_id

    def initialize_env(self):
        self.utilities.print_info("Initializing...")

        self.constants.VPC_ID = self.utilities.get_vpc()

        if not os.path.exists(self.constants.KEY_PAIR_PATH):
            self.utilities.create_key_pair()

        if self.constants.SECURITY_GROUP_NAME is not None:
            response = self.utilities.describe_security_group_id_by_name(self.constants.SECURITY_GROUP_NAME, silent=True)
            if response is not None:
                self.constants.SECURITY_GROUP_ID = response['SecurityGroups'][0]['GroupId']
        
        self.check_sg_and_kp()
        self.utilities.print_info("Initialization done.")

    def auto_setup(self):
        self.initialize_env()

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
        
        self.utilities.print_info(f"Installing Hadoop and Spark on the instance with public IP: {self.instance_public_ip}...")
        self.setup_VM_with_script(self.instance_public_ip)
        self.utilities.print_info("Hadoop and Spark are now ready.")

    def delete_security_group(self):
        self.utilities.delete_security_group(self.constants.SECURITY_GROUP_ID, silent=True)
        self.utilities.print_info("Security Group " + self.constants.SECURITY_GROUP_NAME + " has been deleted.")

    def delete_key_pair(self):
        self.utilities.delete_key_pair(self.constants.KEY_PAIR_NAME, silent=True)

        cctp1_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        keys_path = os.path.abspath(os.path.join(cctp1_path, 'keys'))
        os.remove(os.path.join(keys_path, self.constants.KEY_PAIR_NAME +'.pem'))

        self.utilities.print_info("Key Pair "+ self.constants.KEY_PAIR_NAME + " has been deleted.")

    def terminate_ec2_instances(self):
        self.utilities.terminate_ec2_instances(self.instance_id)

        # self.utilities.print_info("Waiting for " + self.instance_id + " instance to terminate...")
        self.utilities.wait_for_instances(self.instance_id, 'instance_terminated')

    def setup_VM_with_script(self, vm_public_ip):
        os.chmod(self.constants.KEY_PAIR_PATH, 0o400)
        subprocess.check_call([self.constants.SSH_SETUP_SCRIPT_PATH, vm_public_ip])

    def auto_shutdown(self):
        self.terminate_ec2_instances()

        if self.constants.SECURITY_GROUP_ID is not None:
            self.delete_security_group()

        self.delete_key_pair()

    def print_menu(self):
        print("<<------------------------>>")
        print("APPLICATION MENU: ")
        print("  [a] AUTO SETUP")
        print("  [m] LIST MENU")
        print("  [x] QUIT")
        print("<<------------------------>>")

    def run(self):
        self.initialize_env()

        self.print_menu()

        while True:
            cmd_input_line = input("-> ").split()

            if len(cmd_input_line) < 1:
                print("Choose a command and try again!")
                continue

            cmd_input = cmd_input_line[0]

            if cmd_input == 'a':
                self.auto_setup()
            elif cmd_input == 'm':
                self.print_menu()
            elif cmd_input == 'x':
                self.auto_shutdown()
                print("Goodbye! :)")
                break
            else:
                print("Wrong option, try again!")
                continue

