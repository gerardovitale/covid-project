ARG JAVA_IMAGE_VARIANT=slim
ARG OPENJDK_VERSION=8
ARG PY_IMAGE_VARIANT=slim
ARG PYTHON_VERSION=3.9.5

FROM openjdk:${OPENJDK_VERSION}-${JAVA_IMAGE_VARIANT} AS JAVA8

FROM python:${PYTHON_VERSION}-${PY_IMAGE_VARIANT}

ENV JAVA_HOME=/usr/local/openjdk-8
COPY --from=JAVA8 ${JAVA_HOME} ${JAVA_HOME}

MAINTAINER Gerardo Vitale

LABEL name="PySparkApp" \
      license="MIT License"

ENV PYTHONUNBUFFERED 1

ARG CONTAINER_BASE_DIR="/app"
ARG LOCAL_PROJECT_MODULE="/app"
ARG JUPYTER_PORT=8888

ARG APACHE_MIRROR="https://downloads.apache.org"
ARG SPARK_VERSION="3.1.2"
ARG HADOOP_VERSION="3.2"
ARG MONGO_HADOOP_VERSION="1.5.2"
ARG MONGO_HADOOP_COMMIT="r1.5.2"
ARG MONGO_JAVA_DRIVER_VERSION="3.4.0"

ENV CONTAINER_BASE_DIR=${CONTAINER_BASE_DIR}
ENV LOCAL_PROJECT_MODULE=${LOCAL_PROJECT_MODULE}
ENV JUPYTER_PORT=${JUPYTER_PORT}
ENV PATH_TO_SPARK_DIR=/usr/local
ENV MONGO_HADOOP_SPARK_HOME=/usr/local/mongo-hadoop

ENV JAVA_HOME=${JAVA_HOME}
ENV SPARK_DIR_NAME=spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
ENV SPARK_HOME=${PATH_TO_SPARK_DIR}/${SPARK_DIR_NAME}
ENV SPARK_URL=${APACHE_MIRROR}/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

ENV MONGO_HADOOP_URL=https://github.com/mongodb/mongo-hadoop/archive/${MONGO_HADOOP_COMMIT}.tar.gz
ENV MONGO_HADOOP_LIB_PATH=${MONGO_HADOOP_SPARK_HOME}/build/libs
ENV MONGO_HADOOP_JAR=${MONGO_HADOOP_LIB_PATH}/mongo-hadoop-${MONGO_HADOOP_VERSION}.jar
ENV MONGO_HADOOP_SPARK_PATH=${MONGO_HADOOP_SPARK_HOME}/spark
ENV MONGO_HADOOP_SPARK_JAR=${MONGO_HADOOP_SPARK_PATH}/build/libs/mongo-hadoop-spark-${MONGO_HADOOP_VERSION}.jar
ENV MONGO_JAVA_DRIVER_URL=https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/${MONGO_JAVA_DRIVER_VERSION}/mongo-java-driver-${MONGO_JAVA_DRIVER_VERSION}.jar

ENV PYTHONPATH=${MONGO_HADOOP_SPARK_PATH}/src/main/python:${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-0.9-src.zip:/usr/local/lib
ENV SPARK_DRIVER_EXTRA_CLASSPATH=${MONGO_HADOOP_JAR}:${MONGO_HADOOP_SPARK_JAR}
ENV CLASSPATH=${SPARK_DRIVER_EXTRA_CLASSPATH}
ENV JARS=${MONGO_HADOOP_JAR},${MONGO_HADOOP_SPARK_JAR}
ENV PYSPARK_DRIVER_PYTHON=/usr/bin/ipython
ENV PATH=${PATH}:${SPARK_HOME}/bin
ENV NB_USER=spark
ENV NB_UID=1000

RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

RUN wget -qO - ${SPARK_URL} | tar -xz -C ${PATH_TO_SPARK_DIR}/

RUN mkdir -p ${PATH_TO_SPARK_DIR}/bin/before-notebook.d && \
    ln -s "${SPARK_HOME}/sbin/spark-config.sh" ${PATH_TO_SPARK_DIR}/bin/before-notebook.d/spark-config.sh

RUN useradd -m -s /bin/bash -N -u ${NB_UID} ${NB_USER}

COPY ./requirements.txt ${CONTAINER_BASE_DIR}/requirements.txt

ENV LD_LIBRARY_PATH=/lib:/usr/lib:/usr/local/lib

RUN pip install --user --upgrade pip && \
    pip install --user --no-cache-dir -r ${CONTAINER_BASE_DIR}/requirements.txt && \
    rm -f ${CONTAINER_BASE_DIR}/requirements.txt && \
    pip install jupyter

COPY . ${CONTAINER_BASE_DIR}/
WORKDIR ${CONTAINER_BASE_DIR}/
EXPOSE ${JUPYTER_PORT}

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini

RUN chmod +x /usr/bin/tini && \
    chmod +x ./run_app.sh

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["bash", "./run_app.sh"]
