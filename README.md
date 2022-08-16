<h1 align="center"> Wallet APP API </h1> <br>

<h3 align="center">
  An Wallet Backend for Personal Finance Manager. Built with Python/Django Rest Framework.
</h3>

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation Process](#installation-process)

## Introduction

DRF Wallet API provides API endpoints for personal finance manager. Built with Python/Django.

## Features

A few of futher on this app:

- Customized user authentication
- Use phone number to register and login
- Ability to charge, withdraw and transfer money
- Balance calculation at the database level
- Save user transactions
- Document project with swagger
- Dockerized project

## Installation Process

**Installation Process (Linux)**

1. Install docker engine `https://docs.docker.com/engine/install/`
2. Install docker compose `https://docs.docker.com/compose/install/`
3. Clone This Project `git clone git@github.com:amirzre/wallet-app-api.git`
4. Go To Project Directory `cd wallet-app-api`
5. Build docker images `sudo docker compose build`
6. Do make migrations `sudo docker compose run --rm app sh -c "python manage.py makemigrations"`
7. Run the project `sudo docker compose run`
