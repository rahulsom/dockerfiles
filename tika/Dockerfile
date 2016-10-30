FROM java:8-jdk
MAINTAINER Rahul Somasunderam <rahul.som@gmail.com>

WORKDIR /opt
RUN wget http://www-eu.apache.org/dist/tika/tika-app-1.13.jar

WORKDIR /local
CMD java -jar /opt/tika-app-1.13.jar
