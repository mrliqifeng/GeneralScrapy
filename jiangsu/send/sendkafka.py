import pika
from kafka import KafkaProducer

MQ_DICT = {}


def get_or_save_mq(queue_name):
    mq = MQ_DICT.get(queue_name)
    if mq:
        return mq
    else:
        mq = InitMq(queue_name)
        MQ_DICT[queue_name] = mq
        return mq


class InitMq:
    def __init__(self, uuid):
        queue = uuid
        print("***********初始化MQ驱动*************")
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=queue)
        self.routing_key = queue

    def send_data(self, body):
        self.channel.basic_publish(exchange='', routing_key=self.routing_key, body=body.encode('utf-8'))


class InitKafka:
    def __init__(self, topic):
        self.producer = KafkaProducer(bootstrap_servers=["localhost:9092"])
        self.topic = topic

    def send_data(self, data):
        self.producer.send(self.topic, data.encode("utf-8"))

    def close(self):
        self.producer.close()


if __name__ == "__main__":
    inint = InitKafka("world")
    inint.send_data("dsaw")
    inint.close()
