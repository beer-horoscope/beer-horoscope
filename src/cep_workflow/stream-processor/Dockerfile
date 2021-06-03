FROM fedora:33

RUN dnf -y install java-11-openjdk-headless openssl && dnf -y clean all

# Set JAVA_HOME env var
ENV JAVA_HOME /usr/lib/jvm/java

ARG version=latest
ENV VERSION ${version}

COPY ./scripts/ /bin
COPY ./src/main/resources/log4j2.properties /bin/log4j2.properties

RUN chmod 777 /bin/run.sh

ADD target/stream-processor-1.0-SNAPSHOT.jar /

CMD ["/bin/run.sh", "/stream-processor-1.0-SNAPSHOT.jar"]