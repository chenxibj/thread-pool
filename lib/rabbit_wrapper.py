import pika, pickle, logging, sys, traceback
from time import sleep
from django.conf import settings

logger = logging.getLogger(__name__)
res = {"status":1,"msg":"success"}
template = {"deploy_form_id": 1,  "deploy_id": 2, "deploy_type": "UPGRADE", "conn": 5,
            "product": "iaas", "system":"jcloud"}

class RabbitWrapperError(Exception):
    pass

class RabbitWrapper():

    RETRY_TIME = 3
    RETRY_INTERVAL = 1

    def __init__(self):
        print("RabbitWrapper init")
        self.retry_func = None
        self.retry_args = None
        self.retry_time = 0

    def createQueue(self, queue_name, exchange, exchange_type, callback_func=None):
        print("createQueue")
        self.queue_name = queue_name
        self.exchange = exchange if exchange else ''
        self.routing_key = queue_name if queue_name else ''
        self.exchange_type = exchange_type

        ret = self.openConnection()

        if queue_name == "worker_queue":
            print("worker queue")
            self.openQueue()
        elif queue_name == "error_sender":
            self.openExchange()
        else:
            print("error queue")
            self.openQueueExchange()

        if callback_func:
            print("register callback_func for consumer")
            self.basicConsume(callback_func)

    def createWorkerProducer(self):
        self.retry_func = self.createWorkerProducer
        self.retry_args = None
        self.createQueue('worker_queue', None, 'direct')
        return res

    def createWorkerConsumer(self, callback_func):
        self.retry_func = self.createWorkerConsumer
        self.retry_args = callback_func
        self.createQueue('worker_queue', None, 'direct', callback_func)
        return res

    def createErrorProducer(self):
        self.retry_func = self.createErrorProducer
        self.retry_args = None
        self.createQueue("error_sender", 'error', 'fanout')
        return res

    def createErrorConsumer(self, callback_func):
        self.retry_func = self.createErrorConsumer
        self.retry_args = callback_func
        self.createQueue(None, 'error', 'fanout', callback_func)
        return res

    def openConnection(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT))
            # self.connection = pika.BlockingConnection(
            #     pika.ConnectionParameters('localhost'))
            self.channel = self.connection.channel()
        except pika.exceptions.ConnectionClosed as e:
            self.retry_time += 1
            if self.retry_time > self.RETRY_TIME:
                self.retry_time = 0
                raise RabbitWrapperError("fail to openConnection")
            print("openConnection retry time %s , let us sleep a few seconds" % self.retry_time)
            sleep(self.RETRY_INTERVAL*self.retry_time)
            self.openConnection()

    def openExchange(self):
        self.channel.exchange_declare(exchange=self.exchange,
                                      exchange_type=self.exchange_type)

    def openQueueExchange(self):
        print("openQueueExchange")
        result = self.channel.queue_declare(exclusive = True)
        self.queue_name = result.method.queue
        print(result.method.queue)
        self.channel.exchange_declare(exchange=self.exchange,
                                 exchange_type=self.exchange_type)
        self.channel.queue_bind(exchange=self.exchange,
                           queue=self.queue_name)

    def openQueue(self):
        self.channel.queue_declare(self.queue_name, durable=True)

    def basicConsume(self, callback_func):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(callback_func,
                          queue=self.queue_name,
                          no_ack=False)

    def closeConnection(self):
        self.connection.close()

    # Every queue is automatically bound to the defaultexchange
    # with a routing key which is the same as the queue name.
    def sendMsg(self, msg):
        print(self.exchange)
        print(self.routing_key)
        data = pickle.dumps(msg)
        try:
            self.channel.basic_publish(exchange=self.exchange,
                                        routing_key=self.routing_key,
                                        body=data,
                                        properties=pika.BasicProperties(
                                        delivery_mode=2,
                                        ))
        except pika.exceptions.ConnectionClosed as e:
            self.retry_time += 1
            if self.retry_time > self.RETRY_TIME:
                self.retry_time = 0
                raise RabbitWrapperError("fail to sendMsg as connection is closed")
            print("sendMsg retry time %s , let us sleep a few seconds" % self.retry_time)
            sleep(self.RETRY_INTERVAL * self.retry_time)
            if self.retry_args:
                self.retry_func(self.retry_args)
            else:
                self.retry_func()
            self.sendMsg(msg)

    def recvMsg(self):
        try:
            self.channel.start_consuming()
        except pika.exceptions.ConnectionClosed as e:
            self.retry_time += 1
            if self.retry_time > self.RETRY_TIME:
                self.retry_time = 0
                raise RabbitWrapperError("fail to recvMsg as connection is closed")
            print("recvMsg retry time %s , let us sleep a few seconds" % self.retry_time)
            sleep(self.RETRY_INTERVAL * self.retry_time)
            if self.retry_args:
                self.retry_func(self.retry_args)
            else:
                self.retry_func()
            self.recvMsg()

    def parseMsg(self, msg):
        d = pickle.loads(msg)
        for key in template:
            if not d.has_key(key):
                print("parse_msg fail: %s" % d)
                return -1
        return d

    def view_traceback(self):
        ex_type, ex, tb = sys.exc_info()
        traceback.print_tb(tb)
        del tb


