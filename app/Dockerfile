ARG JAVA_IMAGE_VARIANT=slim
ARG OPENJDK_VERSION=8
ARG PY_IMAGE_VARIANT=slim
ARG PYTHON_VERSION=3.9.5


FROM openjdk:${OPENJDK_VERSION}-${JAVA_IMAGE_VARIANT} AS JAVA8

RUN apt-get update && \
    apt-get install -y wget

ARG PATH_TO_SPARK_DIR=/usr/local
ARG SPARK_VERSION="3.1.2"
ARG HADOOP_VERSION="3.2"
ARG APACHE_MIRROR="https://downloads.apache.org"
ENV SPARK_URL=${APACHE_MIRROR}/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    SPARK_HOME=${PATH_TO_SPARK_DIR}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}

RUN wget -qO - ${SPARK_URL} | tar -xz -C ${PATH_TO_SPARK_DIR}/
RUN mkdir -p ${PATH_TO_SPARK_DIR}/bin/before-notebook.d && \
    ln -s ${SPARK_HOME}/sbin/spark-config.sh ${PATH_TO_SPARK_DIR}/bin/before-notebook.d/spark-config.sh


FROM python:${PYTHON_VERSION}-${PY_IMAGE_VARIANT} AS PY3

RUN apt-get update && \
    python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt ${CONTAINER_BASE_DIR}/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r ${CONTAINER_BASE_DIR}/requirements.txt && \
    pip install jupyter


FROM python:${PYTHON_VERSION}-${PY_IMAGE_VARIANT} AS build-image

MAINTAINER Gerardo Vitale
LABEL name="PySparkApp" \
      license="MIT License"

ENV PYTHONUNBUFFERED 1

ARG CONTAINER_BASE_DIR="/app"
ARG LOCAL_PROJECT_MODULE="/app"
ARG JUPYTER_PORT=8888

ARG SPARK_VERSION="3.1.2"
ARG HADOOP_VERSION="3.2"
ARG MONGO_HADOOP_VERSION="1.5.2"
ARG MONGO_HADOOP_COMMIT="r1.5.2"
ARG MONGO_JAVA_DRIVER_VERSION="3.4.0"
ARG TINI_VERSION=v0.6.0

ARG APACHE_MIRROR="https://downloads.apache.org"
ARG PATH_TO_SPARK_DIR=/usr/local
ARG MONGO_HADOOP_HOME=/usr/local/mongo-hadoop

ENV CONTAINER_BASE_DIR=${CONTAINER_BASE_DIR} \
    LD_LIBRARY_PATH=/lib:/usr/lib:/usr/local/lib \
    PYSPARK_DRIVER_PYTHON=/usr/bin/ipython \
    LOCAL_PROJECT_MODULE=${LOCAL_PROJECT_MODULE} \
    JUPYTER_PORT=${JUPYTER_PORT} \
    MONGO_HADOOP_URL=https://github.com/mongodb/mongo-hadoop/archive/${MONGO_HADOOP_COMMIT}.tar.gz \
    MONGO_HADOOP_LIB_PATH=${MONGO_HADOOP_HOME}/build/libs \
    MONGO_JAVA_DRIVER_URL=https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/${MONGO_JAVA_DRIVER_VERSION}/mongo-java-driver-${MONGO_JAVA_DRIVER_VERSION}.jar \
    MONGO_HADOOP_SPARK_PATH=${MONGO_HADOOP_HOME}/spark \
    NB_USER=spark \
    NB_UID=1000 \
    JAVA_HOME=/usr/local/openjdk-8 \
    SPARK_HOME=${PATH_TO_SPARK_DIR}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}

ENV MONGO_HADOOP_JAR=${MONGO_HADOOP_LIB_PATH}/mongo-hadoop-${MONGO_HADOOP_VERSION}.jar \
    MONGO_HADOOP_SPARK_JAR=${MONGO_HADOOP_SPARK_PATH}/build/libs/mongo-hadoop-spark-${MONGO_HADOOP_VERSION}.jar

ENV PYTHONPATH=${MONGO_HADOOP_SPARK_PATH}/src/main/python:${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-0.9-src.zip:/usr/local/lib \
    SPARK_DRIVER_EXTRA_CLASSPATH=${MONGO_HADOOP_JAR}:${MONGO_HADOOP_SPARK_JAR} \
    JARS=${MONGO_HADOOP_JAR},${MONGO_HADOOP_SPARK_JAR} \
    PATH=${PATH}:${SPARK_HOME}/bin \
    PATH=/opt/venv/bin:$PATH

COPY --from=JAVA8 ${JAVA_HOME} ${JAVA_HOME}
COPY --from=JAVA8 ${SPARK_HOME} ${SPARK_HOME}
COPY --from=PY3 /opt/venv /opt/venv

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini

RUN useradd -m -s /bin/bash -N -u ${NB_UID} ${NB_USER}

ENV CLASSPATH=${SPARK_DRIVER_EXTRA_CLASSPATH}

COPY ./src ${CONTAINER_BASE_DIR}/
COPY ./run_app.sh ${CONTAINER_BASE_DIR}/run_app.sh

WORKDIR ${CONTAINER_BASE_DIR}/
EXPOSE ${JUPYTER_PORT}

RUN chmod +x /usr/bin/tini && \
    chmod +x ./run_app.sh

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["bash", "./run_app.sh"]
