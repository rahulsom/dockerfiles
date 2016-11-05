FROM openjdk:8-alpine
MAINTAINER Rahul Somasunderam <rahul.som@gmail.com>

RUN apk update && apk add git && apk add bash

WORKDIR /opt
RUN git clone https://github.com/bazelbuild/bazel.git

WORKDIR /opt/bazel
RUN ./compile.sh
