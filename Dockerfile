FROM python:3
COPY /lc_bot /lc_bot
RUN git clone -b test https://github.com/jpal91/leetcode.git leetcode
WORKDIR /lc_bot
RUN pip install selenium; pip install python-dotenv