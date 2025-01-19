# Cron Expression Parser Service

This service parses cron strings and expands each field to provide customers with insights into when a task or job will run.

## Prerequisites

In order to run this locally, please ensure the following are installed on your system:

1. **Python3**: Confirm that Python 3 is installed by running the following:

    ```
    python3 --version
    ```

    If Python 3 is not installed, you can download it from [python.org](https://www.python.org).

2. **pip**: Confirm that Python's package manager is installed by running:

    ```
    pip3 --version
    ```

## Set Up a Virtual Environment (Recommended)

Setting up a virtual environment allows you to manage dependencies in an isolated environment, enabling you to run different services independently. Follow the steps below:

> You can technically ignore this, and install dependencies globally, but this may intefere with other things you're working on. Using virtual environment ensures your dependencies are isolated.

1. **Create your virtual environment**:

    ```
    python3 -m venv env
    ```

2. **Activate your virtual environment**:

    - **MacOS/Linux**:
      ```
      source env/bin/activate
      ```

    - **Windows**:
      ```
      .\env\Scripts\activate
      ```

## Install Dependencies

With the virtual environment set up and activated, you can now install all the required dependencies:

```
pip install -r requirements.txt
```

## Run the Service

To run the service, navigate to the root directory of the project and use the following command:

```
python3 main.py "<cron_expression>"
```

This will parse and expand the cron expression and display the expanded fields with insights into the execution times.

## Examples

Here’s an example of how to use the service:

If you want to parse and validate the cron expression `30 2 * * * backup.sh`, which runs at 2:30 AM every day, run the following command:

```
python3 main.py "30 2 * * * backup.sh"
```

This will display the expanded cron expression with all the possible execution times.

---

**Note**: This is a local script and is not deployed anywhere. It is designed to run directly from the command line in your local development environment.

