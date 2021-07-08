#!/bin/sh
cp -p "${SPARK_HOME}/conf/spark-defaults.conf.template" \
    "${SPARK_HOME}/conf/spark-defaults.conf"

cp -p "${SPARK_HOME}/conf/log4j.properties.template" \
    "${SPARK_HOME}/conf/log4j.properties"

echo "spark.driver.extraJavaOptions -Dio.netty.tryReflectionSetAccessible=true" \
    >> "${SPARK_HOME}/conf/spark-defaults.conf" && \
    echo "spark.executor.extraJavaOptions -Dio.netty.tryReflectionSetAccessible=true" \
    >> "${SPARK_HOME}/conf/spark-defaults.conf" && \
    echo "spark.driver.extraClassPath ${CLASSPATH}" >> "${SPARK_HOME}/conf/spark-defaults.conf"

echo "spark.jars /usr/local/mongo-hadoop/mongo-hadoop-spark-2.0.0-rc0.jar,\
    /usr/local/mongo-hadoop/mongo-java-driver-3.2.2.jar,\
    /usr/local/mongo-hadoop/mongo-hadoop-2.0.0-rc0.jar" \
    >> "${SPARK_HOME}/conf/spark-defaults.conf"
