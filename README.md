# Social platform

Project was separated from other repository which contains too many projects.<br>
That's why is only few commits here. Please don't think i copy or steal it.

This app is a simple example of a web shop, built in Python/Django.
Main functionalities in the project:


## How to run

1. Using a GIT write the command.
    ``` bash
    git clone https://github.com/Marcin-Chudzik/django-social-platform.git
    ```

2. Create a new virtual environment.<br>
   Open a repository in the code editor (I'm using Pycharm).<br>
   Open a terminal and being in the "django-webshop" directory type a command:
    ``` python
    python.exe -m venv venv
    ```

3. Activate a new venv, change directory on "myshop" and use command.
    ``` python
    pip install -r requirements.txt
    ```

4. Make a migrations and apply them into database, by typing followed commands into the terminal:
    ``` python
    python.exe .\manage.py makemigrations
    ```
    then
    ``` python
    python.exe .\manage.py migrate
    ```

5. Create a new superuser. Type command and follow the displayed instructions:
    ``` python
    python.exe .\manage.py createsuperuser
    ```
