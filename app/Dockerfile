ARG IMAGE_VARIANT=slim
ARG OPENJDK_VERSION=8
ARG PYTHON_VERSION=3.9.5

FROM python:${PYTHON_VERSION}-${IMAGE_VARIANT} AS py3
FROM openjdk:${OPENJDK_VERSION}-${IMAGE_VARIANT}
COPY --from=py3 / /

ENV SPARK_VERSION 3.1.2
ENV HADOOP_VERSION 3.2
ENV MONGO_HADOOP_VERSION 1.5.2
ENV MONGO_HADOOP_COMMIT r1.5.2
ENV MONGO_JAVA_DRIVER_VERSION 3.4.0

ENV SPARK_DIR spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
ENV SPARK_HOME /usr/local/${SPARK_DIR}
ENV APACHE_MIRROR https://downloads.apache.org
ENV SPARK_URL ${APACHE_MIRROR}/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

ENV MONGO_HADOOP_URL https://github.com/mongodb/mongo-hadoop/archive/${MONGO_HADOOP_COMMIT}.tar.gz

ENV MONGO_HADOOP_LIB_PATH /usr/local/mongo-hadoop/build/libs
ENV MONGO_HADOOP_JAR  ${MONGO_HADOOP_LIB_PATH}/mongo-hadoop-${MONGO_HADOOP_VERSION}.jar

ENV MONGO_HADOOP_SPARK_PATH /usr/local/mongo-hadoop/spark
ENV MONGO_HADOOP_SPARK_JAR ${MONGO_HADOOP_SPARK_PATH}/build/libs/mongo-hadoop-spark-${MONGO_HADOOP_VERSION}.jar
ENV PYTHONPATH  ${MONGO_HADOOP_SPARK_PATH}/src/main/python:$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.9-src.zip:/usr/local/lib

ENV MONGO_JAVA_DRIVER_URL https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/${MONGO_JAVA_DRIVER_VERSION}/mongo-java-driver-${MONGO_JAVA_DRIVER_VERSION}.jar

ENV SPARK_DRIVER_EXTRA_CLASSPATH ${MONGO_HADOOP_JAR}:${MONGO_HADOOP_SPARK_JAR}
ENV CLASSPATH ${SPARK_DRIVER_EXTRA_CLASSPATH}
ENV JARS ${MONGO_HADOOP_JAR},${MONGO_HADOOP_SPARK_JAR}

ENV PYSPARK_DRIVER_PYTHON /usr/bin/ipython
ENV PATH $PATH:$SPARK_HOME/bin

ENV NB_USER spark
ENV NB_UID 1000

RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

# Download  Spark -> /usr/local/spark-3.1.2-bin-hadoop3.2
RUN wget -qO - ${SPARK_URL} | tar -xz -C /usr/local/

RUN mkdir -p /usr/local/bin/before-notebook.d && \
    ln -s "${SPARK_HOME}/sbin/spark-config.sh" /usr/local/bin/before-notebook.d/spark-config.sh

RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER

COPY ./requirements.txt /requirements.txt
WORKDIR /app

RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r /requirements.txt && \
    pip install jupyter

COPY . /app/

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]