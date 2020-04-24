# Introduction

The purpose of this document is to detail out the functionality of the Chatbot Project using Azure LUIS the assumptions to ensure that the Project team and the various Stakeholders have a common understanding to ensure the success of the project.

# Background
Ineuron AI team conducted Chatbot project challenge for its students to motivate the potentials to deliver a project end to end.

# Key Objectives

Build a covid-19 Chatbot, which will be able to tell us a number of cases available in any of the locality by providing Pin-code, city name, country etc., as input to the Chatbot and it will give all the instruction and preventive measures.

Chatbot Requirements

* 	Chatbot should welcome the user
* 	Request the user’s name, email ID, mobile number and city name. Store the details in any cloud database
* 	Validations to be done while collecting the data
* 	Chatbot should give show details of Total active, Recovered and Cases for the city or country provided by the user.
* 	Send email to the user about the preventive measures to be taken for Covidh-19 Corona Virus
* 	Bot should provide the option to show map wise COVID cases in case a user is asking for a worldwide case of covid-19

# Application Architecture

Application Architecture is to detail about how the application works, technologies used and how all the components communicate with each other with a pictorial representation.

![](https://github.com/auromirapps/CovidhBot/blob/master/ApplicatioinArchitecture.JPG)

## Cloud Platform (Azure Portal)

Chatbot project is built and deployed in Microsoft azure cloud platform with an Azure subscription (free options). 
 
## Azure Services

Microsoft cloud platform provides multiple services for different kind of projects based on the usage. For this Chatbot project we have used below services
Language Understanding (LUIS)

A machine learning-based service to build natural language into apps, bots, and IoT devices. It is designed to identify valuable information in conversations, LUIS interprets user goals (intents) and distills valuable information from sentences (entities), for a high quality, nuanced language model. LUIS integrates seamlessly with the Azure Bot Service, making it easy to create a sophisticated bot.

## Azure Web App

This service is used create and deploy web applications in different platforms like Windows and Linus. Continuous deployment can be done using GitHub, DevOps etc. For this project we have used GitHub to deploy the website in Azure Web App using KUDU which is used as Service Control manager for Azure web sites. 
### Development Platform and Tools
Website is developed using Flask web framework and Python as programming language. Microsoft Bot framework used as the primary component to integrate with LUIS and retrieve and record user conversations. Visual Studio Community edition is used as the IDE for development.
## Azure Cosmos DB

Data provided by user through Chatbot is stored in Azure Cosmos DB. Azure Cosmos DB is Microsoft's globally distributed, multi-model database service which provides the options to store data using SQL, MongoDB, Cassandra, Tables. For this project we have used DB Table storage. It provides the simplest and fastest way to retrieve and store data.
Data Source for Web App
Live website which provided the data related Corona virus across the world is used as the data source Chatbot service integrating with LUIS. 
Website Link  https://www.trackcorona.live

 
## Bot Channels Registration

Azure Bot Channels registration services is used to integrate the Web App service with different communication channels to provide requested by user. A Channel is the communication between the bot and communication Apps. For this project we have used Azure Web App service as the communication platform. Channels used for this project are 
1.	Web Chat
2.	Microsoft Teams
3.	Telegram

