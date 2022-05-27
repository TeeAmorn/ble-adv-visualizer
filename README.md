# Setting up the MySQL Database 
## MySQL installation
If you're on Mac, install with Homebrew:
```console
$ brew install mysql
```
This may take a while (like 10 minutes).

Once installed, follow the directions to set up a password for your root user. Then, login as the root user to access the CLI:
```console
$ mysql -u root -p
Enter password: 
```
Enter your password (we just made it `password` for now). 
## Creating the database
I wasn't able to create the database with the Python scripts Tee provided (please edit if I'm wrong), so I created the `demo` DB through the MySQL CLI. Now that you're in the CLI, you can create the `demo` database:
```
mysql> CREATE DATABASE demo;
```
You can verify that the database was created:
```
mysql> SHOW DATABASES;
```
# Python project setup
## Setting up the environment
Open a new terminal and cd into the `python-and-db` folder. Set up virtual environment and install the dependencies with the following:
```console
$ cd python-and-db
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```
## Creating the tables
To create the table (named `two`), run:
```console
(venv) $ python setup.py
```
See `python-and-db/setup.py` for more information on the setup of the table.

# C# project setup
## Setting up the environment
Not sure if we need to do this for Unity (probably not?), but for this demo I had to create a `dotnet` project. First, download the `dotnet` SDK [here](https://dotnet.microsoft.com/en-us/download).

Then, create and cd into the project folder (`csharp_mysql` in this case) and run the following command:
```console
$ cd csharp_mysql
$ dotnet new console --framework net6.0
```
## Installing dependencies
To install the MySql.Data package, run:
```console
$ dotnet add package MySql.Data 
```
## Running the project
To run the project, enter:
```console
$ dotnet run
```

