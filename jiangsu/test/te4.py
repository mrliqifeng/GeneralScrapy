import json

from jiangsu.send.sendkafka import get_or_save_mq

mq = get_or_save_mq("javapython")


def start():
    mq.send_data(json.dumps({"taskid": 1, "method": "start"}))
    print("发送启动命令")


def stop():
    mq.send_data(json.dumps({"taskid": 1, "method": "stop"}))
    print("发送停止命令")


if __name__ == "__main__":
    # start()
    stop()
