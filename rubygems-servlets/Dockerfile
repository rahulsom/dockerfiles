FROM maven:3.5.2-jdk-8
MAINTAINER Rahul Somasunderam

WORKDIR /
RUN git clone https://github.com/torquebox/rubygems-servlets

WORKDIR /rubygems-servlets
RUN mvn package
EXPOSE 8989
CMD mvn jetty:run
