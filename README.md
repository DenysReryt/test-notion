# Notion Task Scheduler #

This project implements task scheduling in Notion based on specified dates and periodicity. It uses the Notion API to retrieve and update data in the Notion database.

## Start 
First of all, you need to clone the project from Github locally to your computer:

```commandline
git clone https://github.com/DenysReryt/etcetera-agency-test-assignment.git
```

Before starting, create .env file and configurated environment variables like in .env.example

To start the script, navigate to the project directory in your terminal and run the following command:

```commandline
cd <repository_name>
docker build -t <image_name> .
docker run -it -d -p 8000:8000 <image_name>
```

You run the script, and after clicking on url http://127.0.0.1:8000 in your web browser you make it work with Notion database.