#!/bin/bash

echo "Setup starting..."

# update apt
echo "Updating apt."
sudo apt update

# install java 8, python3  and pip3
echo "Installing Java, Python3, pip3."
sudo apt install -y openjdk-8-jre-headless
sudo apt install -y python3
sudo apt install -y python3-pip

# set PATH for Java
echo "Setting up PATH for Java."
echo '
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH="$JAVA_HOME/bin:$PATH"
' >> ~/.profile

# install spark
echo "Installing PySpark."
pip install pyspark

# download hadoop, unpack it and copy to /usr/local
echo "Downloading Hadoop."
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz

echo "Unzipping an copying Hadoop."
sudo tar -xf hadoop-3.3.1.tar.gz -C /usr/local/

echo "Deleting the Hadoop installation tar file."
rm hadoop-3.3.1.tar.gz

# update PATH for Hadoop
echo "Setting up PATH for Hadoop."
echo '
export HADOOP_HOME=/usr/local/hadoop-3.3.1
export PATH="$HADOOP_HOME/bin:$PATH"
' >> ~/.profile

# update hadoop env variables (java & HADOOP_HOME)
echo "Setting up Hadoop variables."
echo '
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop-3.3.1
' >> /usr/local/hadoop-3.3.1/etc/hadoop/hadoop-env.sh

echo "Reloading profile."

# load .profile to current environment
source ~/.profile

echo "Environment setup done."
echo "Starting Hadoop setup..."

echo '<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
' > $HADOOP_HOME/etc/hadoop/hdfs-site.xml

echo '<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/var/lib/hadoop</value>
    </property>
</configuration>
' > $HADOOP_HOME/etc/hadoop/core-site.xml

sudo mkdir /var/lib/hadoop
sudo chmod 777 /var/lib/hadoop
hdfs namenode -format

ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

echo "Hadoop setup done."
