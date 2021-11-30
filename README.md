# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

With the help of https://azure.microsoft.com/en-us/pricing/calculator/:

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database* |  [Single Server]( https://azure.microsoft.com/en-us/pricing/details/postgresql/server/), Pay as you go  |     =$127.90 Average per month         |
| *Azure Service Bus*   |    Basic,Standard     |   =0 - $9.81  Free in case of Basic!!!         |
| *Storage Account*                   |  Pay as you go      |     =$20.80 Average per month         |
| *App Service Plan*                   |  Premiun V2    |     =$83.95  |
| *Azure Function*                   |  Consumption   |    In most cases free, but be aware that you may be charged $0.20 per million executions |

## Architecture Explanation

Azure WebApps are a a good choice under business context in which there is a need of lightweight applications and services. That was the case of this choice context. They provided us the following *advantageous* featues:
- Continuous deployment with Git, Team Foundation Server, GitHub, and DevOps
- Built-in autoscale and load balancing
- Supports WordPress, Umbraco, Joomla!, and Drupal
- Support of multiple languages, such as .NET, .NET Core, Java, Ruby, Node.js, PHP, or Python
- High availability with auto-patching
- Vertical or Horizontal scaling.
- Supports Windows and Linux platforms
Even if they have some resource limitations, it is a great resource to be evaluated, specially for focusing in core business needs as well as cost savings. 

 Having used the zure Functions within the selected has their own *benefits*:
 -They provide all the continually updated infrastructure and resources needed to run your applications. 
 - Again,you are able to focus on your core business and functionality
 - They provide **serverless** compute for Azure.
 - They may share the same app service plan which would reduce the cost for multiple service plans.

The main *drawbacks* of this architecture is that there is a limitation on scalibility and high performance demanding context. For the azure function app it has been used the app service service plan. According to the documentation, timeout is difference depending on which hosting method / pricing tier is used to host an Azure Function App. While in the Consumption plan, the default timeout is 5 minutes, there is a different default and maximum timeout for the App Service Plan and Premium Plan pricing (being 5 vs 30 min in comsumption and App Service Plan). This may be a drawback adopting this architecture. However, there are some is some best practices/chitectural patterns to able to deal with it like Function Chaining, among others. Itis a method of breaking up a long running task into multiple shorter running tasks and then linking them together so that each one call the next in the workflow once it completes.


Overall, both provides us a way to not only carry out a cost saving plan but also to delegate some of the infraestructure management making your solutions easier to deploy and more important to continuously delivery and monitor your (micro) services.
 




