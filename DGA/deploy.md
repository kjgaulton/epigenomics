## Initial set-up and deploy in single server mode

Run these commands create the initial site and database, which then can later be deployed as a cluster for a full production site if desired in the next section.  

Important:  You should fork your own repository with the code base, as setting up your own site will require systematic changes (such as your S3 bucket names, other customized aspects of your site such as the homepage etc.).  Your repository is also cloned into the AWS instance as part of installation and therefore needs to have these changes reflected in the repository in GitHub directly for proper deployment.  

**DGA repo:**  
```
git clone https://github.com/T2DREAM/t2dream-portal.git
```

**Deploy test server to local machine:**
Follow instructions in README.rst

**Deploy to AWS instance:**  
Pick a name for the instance, e.g.:  x1  
(Make sure your AWS credentials are in order on your local machine to ensure you can log in to instances once deployed)

Create buckets on S3 via the AWS console which are uniquely named for your site – for DGA the buckets all start with the tag ‘t2depi’.  For example, if you used the tag ‘mysite’, the buckets you need to create would be:mysite, mysite-blobs, mysite-blobs-dev, mysite-conf-prod, mysite-files, mysite-files-dev, mysite-backups  
(Make sure to modify the entire code base to point to the buckets created for your site and not t2depi or encode buckets)

In AWS console, create the following IAMs: encoded-files-upload, encoded-instance, production

**For production:**  
```
./bin/deploy --name x1 --test --instance-type m4.xlarge --profile-name production
```
Can change instance type based on the size of production site needed

Go to your AWS console, look at EC2 running instances

Select the public DNS for the instance just deployed, 
e.g.: ec2-xx-xxx-xxx-xxx.us-west-2.compute.amazonaws.com (each time will be different DNS)

**Login to instance to check status of installation:**  
```
ssh ubuntu@ec2-34-210-240-153.us-west-2.compute.amazonaws.com
```

**View progress:**  
```
tail -f /var/log/cloud-init-output.log
```

Server should automatically reboot after installation is complete

Visit the URL http://ec2-xx-xxx-xxx-xxx.us-west-2.compute.amazonaws.com - should return the homepage, although without the initial splash page

To load ‘test’ data (in my experience was needed for the site to start working properly and to ‘prime’ the database to enable adding real data – but may not be necessary for others), login to instance:  
```
cd /srv/encoded/
sudo -u encoded /bin/dev-servers production.ini --app-name app --load --init
```  
[might require some editing of dev-servers to work properly]

**Set up postgres backup (WAL):**  

add to postgres.conf:  
```
archive_command = '/opt/wal-e/bin/envfile --config /home/ubuntu/.aws/credentials --section default --upper -- /opt/wal-e/bin/wal-e --s3-prefix="$(cat /etc/postgresql/9.3/main/wale_s3_prefix)" wal-push "%p"'
```

Restart postgres

**Create base backup:**  
```
sudo -i -u postgres /opt/wal-e/bin/envfile --config /home/ubuntu/.aws/credentials --section default --upper -- /opt/wal-e/bin/wal-e --s3-prefix="$(cat /etc/postgresql/9.3/main/wale_s3_prefix)" backup-push /var/lib/postgresql/9.3/main
```

**Cron for scheduled backups (1 AM PST):**  
```
sudo crontab -e

00 7 * * * sudo -i -u postgres /opt/wal-e/bin/envfile --config ~postgres/.aws/credentials --section default --upper -- /opt/wal-e/bin/wal-e --s3-prefix="$(cat /etc/postgresql/9.3/main/wale_s3_prefix)" backup-push /var/lib/postgresql/9.3/main
```

Create an admin user account by creating a user for yourself based on the ‘user.json’ schema (see example provided at end of document), and load it into the database.  Make sure you are in group ‘admin’ so that you have administrator privileges.  You can post JSON to the database using the script ‘loadxl.py’.  Using this account will allow you to then authenticate with your email address once Auth0 is setup and log in to the site and start adding additional information from the web.  

To load commonly used ‘core’ meta-data from ENCODE (such as antibodies, organisms, software, etc.), perform bulk download of JSON for each category and load into site using ‘ENCODE_import_data.py’ script in repository  

Establish an Elastic IP on AWS so that the site will always be associated with the same IP, and so that this IP can be referenced in other necessary contexts such as for authentication.

**For SSL - Instructions on how to add SSL certificate are here:**  
https://certbot.eff.org/#ubuntutrusty-apache
(Requires reboot after installation, renewal every ~90 days)

**Authentication:**  
Create account and login to https://auth0.com/ for authentication and login for authenticated users

Create auth0 application (react, application type: single page).  Add your site URL(s) to allowed callback urls, allowed web origins and CORS 

Enable AWS add on.  Configure and enable connections for Gmail, Facebook, Twitter etc. so that user can login using these accounts https://auth0.com/docs/dashboard/guides/connections/set-up-connections-social

Check if you can login to your admin user account authenticated using social media via the web site.

## Deploy in cluster mode  

This will launch the elastic search and indexing in cluster mode which is necessary to accommodate large datasets and meet computational demands for a full production site. The cluster node runs elasticsearch (for indexing & searching) and the master node runs the main python codebase.

Once the initial site and database is created, that instance can be spun down and the site can be deployed in cluster mode and the database can then be re-loaded into the new site from the backup.  Similarly, when changes are made to the code and a new production server needs to be deployed to reflect these changes, a new cluster can be spun up and the database can be re-loaded into the site from the backup.   

**Deploy AWS instances:**  
Checkout the code on local machine  
```
git clone https://github.com/T2DREAM/t2dream-portal.git
```

**For production:**  
Navigate to t2dream-portal directory and launch master node  
```
bin/deploy --cluster-name vX-cluster --profile-name production --candidate --n vX-master --instance-type c5.9xlarge
```

**Launch cluster nodes**   
```
bin/deploy --elasticsearch yes --cluster-name vX-cluster --cluster-size 3 --profile-name production --name vX-cluster --instance-type c5.xlarge
```

Note: X is the instance version
Ensure the --cluster-name for launching cluster nodes and master node is same

Go to AWS console, check that the cluster nodes and master nodes are running
Important: Open security groups elasticsearch-https (for elasticsearch cluster mode), ssh-http-https for master and all the cluster nodes individually via AWS console.

Select public DNS for the master node just deployed, e.g.: ec2-xx-xxx-xxx-xxx.us-west-2.compute.amazonaws.com (each time will be different DNS)

***Login to master instance to check status of installation:**   
```
ssh ubuntu@ec2-xx-xxx-xxx-xxx.us-west-2.compute.amazonaws.com
```

**View progress:**
```
tail -f /var/log/cloud-init-output.log
```

Usually runs without any errors, errors typically encountered only when modules/dependencies are deprecated
The master server should automatically reboot after installation is complete.  

Visiting the URL of the master node http://ec2-xx-xxx-xxx-xxx.us-west-2.compute.amazonaws.com should return the homepage of the site

Login to master node instance to add elasticsearch replicas: ssh ubuntu@ec2-xx-xxx-xxx-xxx.us-west-2.compute.amazonaws.com
(https://www.elastic.co/guide/en/elasticsearch/guide/current/distributed-cluster.html)

**Add Replicas**  
```
curl -XPUT 'localhost:9200/_all/_settings' -d '{"index": {"number_of_replicas": 2}}'
```

**View cluster health on master**
```
curl localhost:9200/_cluster/health?pretty
{
  "cluster_name" : "v6-cluster",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 5,
  "number_of_data_nodes" : 4,
  "active_primary_shards" : 102,
  "active_shards" : 204,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0
}
```

**Retrieve the latest WAL backup of postgres (during installation process) - required for production:**
Stop PostgreSQL server and remove data directory  
```
sudo service postgresql stop  
sudo rm -rf /var/lib/postgresql/9.3/main
```

**Fetch latest WAL-E backup**   
```
sudo -i -u postgres /opt/wal-e/bin/envfile --config /home/ubuntu/.aws/credentials --section default --upper -- /opt/wal-e/bin/wal-e --s3-prefix="$(cat /etc/postgresql/9.3/main/wale_s3_prefix)" backup-fetch /var/lib/postgresql/9.3/main LATEST
```

**Change postgres recovery.conf to include command that runs during recovering**
`sudo -u postgres vim /var/lib/postgresql/9.3/main/recovery.conf` 

Add to recovery.conf:  
```
restore_command = '/opt/wal-e/bin/wal-e --aws-instance-profile --s3-prefix="$(cat /etc/postgresql/9.3/main/wale_s3_prefix)" wal-fetch "%f" "%p"'
```

**Start PostgreSQL and Reboot the server (master and cluster nodes) via. aws console!**
`sudo service postgresql start`

Once WAL backups are retrieved indexing to ES datastore initiates



## Additional info

Example ‘user.json’:
```
{
    "email": "kgaulton@gmail.com",
    "first_name": "Kyle",
    "groups": [
        "admin"
    ],
    "job_title": "PI",
    "last_name": "Gaulton",
    "schema_version": "5",
    "status": "current",
    "submits_for": [],
    "timezone": "US/Pacific"
}
``` 


