# Plug & Play Authenticator

A simple user authentication system built with Python 3's Standard Library.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have python 3.6+ installed

```
python --version
```
You should get some output like 3.6.2. If you do not have Python, please install the latest 3.x version from python.org or refer to the Installing Python section of The Hitchhiker’s Guide to Python.

### Installing & Running

If you have Python 3 you are ready to go
```
git clone https://github.com/miniatureweasle/simple_authenticator.git
cd simple_authenticator
python3 client.py signup
```
This will execute the client to prompt for your user credentials. Once entered, wait for the server's response
and then check your email's inbox for a verification link (don't shut down the server while doing this).
Once you are registered you can login.
```
python3 client.py login
```
You can also login before signup, login with an incorrect
email or password and login before your email has been verified
to test functionality.

## Running the tests

I've included some rudimentary unit tests.

```
python3 test.py
```
## Contact

Please contact jacobfionngoldberg@gmail.com if there are any issues