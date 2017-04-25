# Relational Databases and Mem-cache on Amazon Web Services

Name : Aastha Gupta <br>
Email : aastha.gupta@mavs.uta.edu <br>
Affiliation : University of Texas at Arlington <br>
Website URL :  <br>

## Project Description : <br>

Developed a web application in python which could store, query data and retrieve results from database or from Mem-cache (if record exists). Also, the application records time to retrieve records. <br>

1. Configure EC2 as the webserver that host the python flask application. <br>
    Follow the following link to configure EC2 instance : "http://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/" <br>
2. Load the data into a Relational DB. <br>
3. Write SQL code to do 5 thousand random queries. Log the time from request to response.<br>
4. Repeat using queries of 5 thousand specific (limited by parameter) queries. Log the time from request
   to response. <br>
5. Repeat previous two steps using “Elastic” Cache (Memcache, Redis, etc.) <br>

#### Run the app on AWS apache server using 'sudo apachectl restart' on Ubuntu Commandline Terminal. <br>

[Install Python]: https://www.python.org/downloads/