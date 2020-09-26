# Forex Web Application

This is a full stack web application where users could search for exchange rates.

## Technologies used: 
  1) Client-Side : ReactJs, HTML, CSS
  2) Server-Side :  Python-Flask
  3) Database: Cassandra in docker

## Description
  Users today are keen on looking out for foreign currency rates. Users are interested to know how their country is doing by comparing it with other currencies.
  This application provides a platform to check exchange rates between countries. It's an easy-to-use lightweight applicaton. 
  
## Architecture

  ![Architecture Diagram](https://github.com/ViswanathanAR96/forex-app/blob/master/Architecture%20diagram.jpg)

## Features:
  1) API based Architecture
  2) HTTP services: GET, POST
  3) use of an external API to get forex rates
  4) cassandra database to store and retrieve data
  
## Installation Instructions:
  Run the following commands to setup docker with cassandra. 
  1) docker pull cassandra                                          ---- To download the docker image of cassandra into your local system
  2) docker run -d --name cassandra-dev -p 9042:9042 cassandra      ---- To create a container within the cassandra image called cassandra-dev and setting the container on port 9042
  3) docker exec -it cassandra-dev bash                             ---- Execute the cassandra container. Now you are all set to perform database operations
  

  
