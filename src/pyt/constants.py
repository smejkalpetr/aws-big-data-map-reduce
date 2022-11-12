
class Constants:
    KEY_PAIR_NAME = "log8145-key-pair"
    KEY_PAIR_PATH = "./keys/log8145-key-pair.pem"

    SECURITY_GROUP_NAME = "log8145-security-group"
    SECURITY_GROUP_ID = None

    VPC_ID = None

    AMI_ID = "ami-0149b2da6ceec4bb0"

    M4_LARGE = "m4.large"

    SCRIPT_EXECUTE_ON_REMOTE = "./src/bash/ssh_execute_local_script_on_remote.sh"

    URLS_DATASETS_PATH = "./src/wc/urls.txt"

    SCRIPT_VM_SETUP = "./src/bash/vm_setup.sh"
    LOG_VM_SETUP = "./logs/vm_setup.log"

    SCRIPT_DOWNLOAD_DATASETS = './src/bash/wordcount_download_dataset.sh'
    LOG_DOWNLOAD_DATASETS = './logs/download_dataset'

    SCRIPT_WORDCOUNT_LINUX = './src/bash/wordcount_linux.sh'
    LOG_WORDCOUNT_LINUX = './logs/wordcount_linux.log'

    SCRIPT_WORDCOUNT_HADOOP = './src/bash/wordcount_hadoop.sh'
    LOG_WORDCOUNT_HADOOP = './logs/wordcount_hadoop.log'

    SCRIPT_WORDCOUNT_SPARK = './src/bash/wordcount_spark.sh'
    LOG_WORDCOUNT_SPARK = './logs/wordcount_spark.log'