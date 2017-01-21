FROM ubuntu:latest
MAINTAINER Rahul Somasunderam <rahul.som@gmail.com>

RUN apt-get update && \
        apt-get install -y python swig python-numpy git openjdk-8-jdk-headless curl

RUN echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list && \
        curl https://bazel.build/bazel-release.pub.gpg | apt-key add - && \
        apt-get update && apt-get install -y bazel

RUN git clone https://github.com/tensorflow/tensorflow.git && \
        cd tensorflow && \
        yes "" | ./configure && \
        bazel build -c opt //tensorflow/java:tensorflow //tensorflow/java:libtensorflow_jni
