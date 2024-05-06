# Password Hacking

How safe is your password?
What is a strong password?

This repository is a simple python repository to demonstrate how to:
a. Generate a strong(ish) password in python
b. Crack bad passwords using 2 obvious techniques.

There are two main python exercises, and one more general activity to crack an actual application behind a password.
As such, for this repository we assume python3 is installed and a bash cli is used.
It can of course be amended to use windows powershell, online python compilers, etc to run it.

Further details are outlined below.

## Task 1
Create a python function to generate a password of 8 characters.
It must have:
* A lowercase letter
* An uppercase letter
* A number
* A special character `£$%&:@;_-+=[]{}?`


Write your [function](task1/task1.py).
When ready to test it run
```sh
python3 test1.py
```

If you get stuck see the [help information for task1](docs/Task1Help.md)

A solution, if you must, can be found [here](docs/SolutionTask1.py).
It is not the only solution, or even the best. Just one that works and is fairly simple.

## Task2
The aim of this task is to use two techniques used to crack passwords, more information is online for example [from nord](https://nordvpn.com/blog/password-cracking/).

There are two functions to [implement](task2/task2.py).
The first is to crack a pin number, 4 characters long, pure brute force.
The second is a targeted brute force attack using common prefix/suffix patterns.

When ready run
```sh
python3 test2.py
```

If you get stuck see the [hints](docs/Task2Help.md).

If you must, there is a [solution](docs/SolutionTask2.py).
It is not the only solution, or even the best. Just one that works and is fairly simple.

## Hints
See the docs folder

## Unit tests
Run all unit tests with
```sh
python3 -m unittest
```

## Activity
Navigate [here](activity/README.md) and follow the instructions.
Unfortunately, you will have to host the flask app yourself currently.
