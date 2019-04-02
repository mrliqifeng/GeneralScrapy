import json
import subprocess
import threading
from jiangsu.sql.tasksql import *
from jiangsu.send.sendkafka import *

TASKINFO = None
TASKSTATUS = None


def go(mq):
    if TASKSTATUS.status == 1:
        print("此爬虫正在运行")
        mq.send_data("此爬虫正在运行")
    else:
        print("*********程序启动*************")
        p = subprocess.Popen('scrapy crawl mySpider',
                             shell=True)  # -s JOBDIR=remain/%s' % name , stdout=subprocess.PIPE
        update_status_pid(p.pid, 1, TASKINFO.id)
        mq.send_data("爬虫启动成功")

def ki(mq):
    status = TASKSTATUS.status
    if status == 1:
        print("********************正在杀死******************")
        subprocess.Popen('taskkill /pid %s -t -f' % TASKSTATUS.pid, stdout=subprocess.PIPE, shell=True) #
        update_status(0, TASKINFO.id)
        mq.send_data("爬虫停止成功")
        print("爬虫停止成功")
    elif status == 0:
        mq.send_data("此爬虫已为停止状态")
        print("此爬虫已为停止状态")
    else:
        mq.send_data("此爬虫为初始状态")


def callback(ch, method, properties, body):  # 定义一个回调函数，用来接收生产者发送的消息
    global TASKINFO, TASKSTATUS
    body = body.decode('utf-8')
    js = json.loads(body)
    taskid = js.get("taskid")
    TASKINFO = get_taskinfo(taskid)
    TASKSTATUS = get_taskstatus(taskid)
    mq = get_or_save_mq("pythonjava")
    if js.get("method") == 'start':
        writeconf(taskid)
        t1 = threading.Thread(target=go, args=(mq,))
        t1.start()
    if js.get("method") == 'stop':
        t2 = threading.Thread(target=ki, args=(mq,))
        t2.start()


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='javapython')

channel.basic_consume(callback,
                      queue='javapython',
                      no_ack=True)
print('[消费者] waiting for msg .')
channel.start_consuming()  # 开始循环取消息
