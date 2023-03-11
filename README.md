# Date App
<!-- ABOUT THE PROJECT -->
## About The Project
### This is a fullstack application for our IT490 Project
###### Three-Tier Architecture VPC Logical Model - (Scripts have a sequential order to be run, VPC script goes first, and then RDS script.)
Three Tier Architecture has become a staple practice for many Web Application solutions when it comes to deploying a highly available and scalable application. This three-tier-architecture deploys a VPC with 2 Availability Zones, 6 subnets, 2 public and 4 private, along with 2 NAT gateways, an Internet Gateway, public and private route tables, an S3 bucket for any packages or files, and deploying 2 database instances in the database-tier one on each AZ.
CloudFormation is a service by AWS that is used to provision AWS resources using code. When you create a stack, AWS will automatically go through your code and deploy the resources you defined automatically which makes provisioning infrastructure very easy and neat! CloudFormation scripts can be written in YAML or JSON but in this lab, I chose to write it in YAML because it is very easy to read and define all the resources you need when writing the script. 

Why CloudFormation?
* It is an AWS native solution for Infrastructure as a Code and does the job of automatically provisioning resources well. 
* Terraform can be a good alternative.
* Writing the code is very easy since AWS supplies a lot of documentation for problems or templates you might need.

Still in progress, so what is next?
* Writing new scripts that deploy needed components into the subnets. (Bastion Host, ELB, ALB, Auto-Scaling Group, Client Server, Web Server)

### Built With
* ![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

<!-- CONTACT -->
## Contact
* [![LinkedIn][linkedin-shield]][linkedin-url] (Lap)
* [![LinkedIn][linkedin-shield]][linkedin-url-brian] (Brian)

<!-- MARKDOWN LINKS & IMAGES -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/lap-le-cloud/
[linkedin-url-brian]: https://www.linkedin.com/in/brian-gomez-devops-engineer/
