#docker build -t jobs:02 .
#docker run  -it /bin/bash -v /var/www/lk_2_0:/var/www/lk_2_0/ jobs:01
#docker run  -d -v /var/www/lk_2_0:/var/www/lk_2_0/ jobs:02

FROM debian
RUN apt update && apt install -y ssh python3 python3-pip nano

RUN mkdir -p /root/.ssh/
COPY known_hosts /root/.ssh/

RUN mkdir -p /var/www/jobs_2.0/
RUN mkdir -p /var/www/share/

WORKDIR /var/www/jobs_2.0/
COPY . /var/www/jobs_2.0/

RUN pip3 install --no-cache-dir -r requirements.txt

#CMD ["python3", "run_jobs.py" ,"/var/www/api_2_0/"]