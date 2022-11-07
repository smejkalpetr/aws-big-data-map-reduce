# this is the script that runs on a VM after its startup (this needs to install Hadoop and Spark)


#Install Java 8 (other versions just don't work)
sudo apt install curl -y
sudo apt-get install unzip
sudo apt-get install zip

curl -s "https://get.sdkman.io"	| bash
source ~/.sdkman/bin/sdkman-init.sh\"

sdk install java 8.0.265-open

##Install Hadoop##
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz
#unpack
sudo tar -xvf hadoop-3.3.4.tar.gz -C /opt/
#remove the archive file and go to the right directory
rm hadoop-3.3.4.tar.gz && cd /opt
#rename
sudo mv hadoop-3.3.4 hadoop
echo "export HADOOP_HOME=/opt/hadoop" >> ~/.bashrc
echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin" >> ~/.bashrc

#No permission for this line, so yet to figure out
echo "export JAVA_HOME=/.sdkman/candidates/java/8.0.265.open" >> /opt/hadoop/etc/hadoop/hadoop-env.sh

##installing Spark##
wget https://dlcdn.apache.org/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz	
#unpack
sudo tar -xvf spark-3.3.1-bin-hadoop3.tgz -C /opt/
#remove the archive and go the opt file
rm spark-3.3.1-bin-hadoop3.tgz && cd /opt
#rename to spark
sudo mv spark-3.3.1-bin-hadoop3 spark
#define the SPARK_HOME environment variable
echo "export SPARK_HOME=/opt/spark" >> ~/.bashrc
echo "export PATH=\$PATH:\$SPARK_HOME/bin" >> ~/.bashrc
source ~/.bashrc 
