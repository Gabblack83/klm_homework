FROM registry.access.redhat.com/ubi9/python-311

USER root
RUN yum install -y gcc gcc-c++ make npm
RUN cd /home && mkdir klm_homework
ENV WORKING_DIR /home/klm_homework
WORKDIR ${WORKING_DIR}
RUN mkdir logs
COPY requirements.txt ${WORKING_DIR}
RUN pip install -r ./requirements.txt
COPY ./vue ./vue
RUN cd vue && npm i
COPY ./build_vue ./build_vue
COPY ./common ./common
COPY app.py ${WORKING_DIR}
ENV PYTHONPATH ${PATHONPATH}:${WORKING_DIR}
RUN python3 ./build_vue/build.py

RUN useradd -g 0 notrootuser
USER notrootuser


EXPOSE 9442
ENTRYPOINT ["python3", "app.py"]