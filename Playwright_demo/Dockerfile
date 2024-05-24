FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ &&  \
    playwright install &&  \
    playwright install-deps && \
    ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&  \
    echo Asia/Shanghai > /etc/timezone
CMD ["python", "main.py"]
