# rfm-flask-CI-CD-AWS

DevOps CI/CD Pipeline to AWS


## Pre-requisites:
Points to Jot Down
1. IAM user Access Key + IAM User Secret Key: 
Create one IAM user with following privileges:
•	Full Access S3
•	Full Access EBS

2. Name of the S3 bucket:Create S3 bucket that will store Deployment Packages. The code and other related files will be pushed to S3 
as a zip folder from GitHub.

3. Application Name + Environment Names + Region: rfm + rfm-dev +rfm-prod	Create a sample application and two environments (dev and prod) in a particular region on AWS.

## Workflow:

![cicd](https://user-images.githubusercontent.com/54689111/79947615-3dedf600-8440-11ea-8155-8d28b7545c38.JPG)


## Implementation:
1.	Push the code from local repository to a GitHub repository on Master Branch.
2.	Create two more branches: Dev and Prod.
3.	Go to Actions and create a CI/CD pipeline for Development Continuous Integration and Continuous Deployment.
4.	Store the AWS IAM user credentials: AWS Access key and AWS Access Secret Key in Secret Tab in GitHub.
5.	This pipeline is created from dev.yml file that stores the variables in env: Bucket name, Application name, Environment name, Package name, AWS Region Name.
6.	It will have a job: Built that will be triggered when something is pushed to Dev Branch. It will have steps to clone the repository and push it to AWS S3 in form of zip file using the credentials stored as Secret in Github.
7.	Similarly, another job will be: Deploy that will be triggered after the completion of the first job (Built). It will include steps to configure credentials, create a new environment for the application with the source code on S3 and then deploy the application on dev environment.
8.	Similarly, create another pipeline for CI/CD Production Environment. In this case, create a prod.yml file in which jobs will be triggered when the code/changes are pushed to the Production environment. 



 

