
# TP2: Advanced Concepts of Cloud Computing

## Description of the Work



## Instructions to Run the Code

1. Configure AWS Credentials on your computer:

    * Open the file with AWS credentials:
  
        ``code ~/.aws/credentials``
        
    * Navigate to your AWS Academy account, then to AWS Details and copy your AWS CLI information. 
        
    * Paste the AWS CLI information to the opened credentials file and save and close the file.
    
    * If there's an error saying that you haven't configured your location, create a file called ``config`` in the ``~/.aws`` folder and put this in it:
    
    ```text
   [default]
   region = us-east-1
   output = json 
   ```
   
   * Now you can test if you're connected to the AWS by running the following command:
   
   ``aws ec2 describe-key-pairs``
   
   This shouldn't throw any exception (note that you need to have installed the aws-cli tool in order to run this command).

 2. Clone the GitHub repository to your desired location:
  
    ``git clone https://github.com/smejkalpetr/cc-tp2.git``
  
3. Proceed to the project's directory:
  
    ``cd cc-tp2``
  
4. Run the automated application:
  
    ``. ./setup.sh``
    
5. See output in the log files
  
    ``./logs/wordcount*.log`` and ``./logs/social_network_problem.log``
