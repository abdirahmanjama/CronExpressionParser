# Cron Expression Parser Service

This service parses cron strings, and expands each field to provide customers with insights into when a command will run.

## Prerequisites

1. Please ensure you the following installed:

    - **Python3**: Ensure you have this installed by running:

    ```
    python3 --version
    ```

    If Python 3 is not installed, you can download it from python.org.

    - **pip**: verify you have python's package manager installed by running:

    ```
    pip3 --version
    ```


## Set Up a Virtual Environment

Setting up a virtual environment allows you to manage your dependencies in an isolated environment, enabling you to run different services at scale. 

1. Create your virtual environment:

```
python3 -m venv env
```

2. Activate your virtual environment:

  - MacOS/Linux
    ```
    source env/bin/activate
    ```

- Windows
    ```
    .\env\Scripts\activate

    ```



## Install Dependencies

With the virtual environment set up, and activated. You can now install all the dependencies in an isolated environment: 

```
pip install -r requirements.txt
```



## Run the service

Run the service in your command line,running this in rpoject root: 

`python3 main.py <cron expression>`

## Examples

If you want to parse and validate the cron expression and it's associated command, like `30 2 * * * example_script.sh`(which runs at 2:30 AM every day), you would run:

`python3 main.py "30 2 * * * backup.sh"`
