FROM python:3.6.9-stretch

# ---------------------------------------------------------------------------------------------------------------------
# Install Java
RUN apt-get update && apt-get install openjdk-8-jdk -y && apt-get clean

# ---------------------------------------------------------------------------------------------------------------------
# Fiji installation
# Install virtual X server
RUN apt-get update && apt-get install -y unzip xvfb libx11-dev libxtst-dev libxrender-dev

# Install Fiji.
RUN wget https://downloads.imagej.net/fiji/Life-Line/fiji-linux64-20170530.zip
RUN unzip fiji-linux64-20170530.zip
RUN mv Fiji.app/ fiji

# create a sym-link with the name jars/ij.jar that is pointing to the current version jars/ij-1.nm.jar
RUN cd /fiji/jars && ln -s $(ls ij-1.*.jar) ij.jar

# Add fiji to the PATH
ENV PATH $PATH:/fiji
RUN mkdir -p /fiji/data

# Clean up
RUN rm fiji-linux64-20170530.zip

# ---------------------------------------------------------------------------------------------------------------------
# Install Fiji plugins
RUN cd /fiji/plugins && wget -O imagescience.jar https://imagescience.org/meijering/software/download/imagescience.jar
RUN cd /fiji/plugins && wget -O FeatureJ_.jar https://imagescience.org/meijering/software/download/FeatureJ_.jar

# ---------------------------------------------------------------------------------------------------------------------
# Install Macro
ADD macro.ijm /fiji/macros/macro.ijm
ADD wrapper.py /app/wrapper.py

# for running the wrapper locally
ADD descriptor.json /app/descriptor.json

ENTRYPOINT ["python", "/app/wrapper.py"]
