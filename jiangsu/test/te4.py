import json
import time
from urllib import parse

from jiangsu.send.sendkafka import get_or_save_mq

mq = get_or_save_mq("javapython")


def start(id):
    mq.send_data(json.dumps({"taskid": id, "method": "start"}))
    print("发送启动命令")


def stop(id):
    mq.send_data(json.dumps({"taskid": id, "method": "stop"}))
    print("发送停止命令")


def split_url(url):
    url = str(url)
    if url.startswith(":"):
        urls = url.split(":")
        result_urls = [parse.quote(one) for one in urls]
        result = ":".join(result_urls)
        return result
    else:
        return parse.quote(url)


if __name__ == "__main__":
    # start(26)
    stop(26)
