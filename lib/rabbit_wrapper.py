import pika
import pickle
import logging
import traceback
import sys

logger = logging.getLogger(__name__)
res = {"status":1,"msg":"success"}
msg = {"deploy_form_id": 1,  "deploy_id": 2, "deploy_type": 3}
# deploy_type: 1/3/4/5 1:upgrade 3:restart  4:downgrade  5:cancel
queue_dict = {'worker':'worker_queue', 'error':'error_queue'}

class RabbitWrpper():


    def __init__(self):
        print("RabbitWrpper init")

    def fastInitProcuder(self):
        self.openConnection()
        self.openChannel()
        self.openQueue(queue_dict['worker'])
        return res

    def fastInitErrorProcuder(self):
        self.openConnection()
        self.openChannel()
        self.openQueue(queue_dict['error'])
        return res

    def fastInitConsumer(self, callback_func):
        self.openConnection()
        self.openChannel()
        self.openQueue(queue_dict['worker'])
        self.addCallbackFunc(callback_func)
        return res

    def fastInitErrorConsumer(self, callback_func):
        self.openConnection()
        self.openChannel()
        self.openQueue(queue_dict['error'])
        self.addCallbackFunc(callback_func)
        return res

    def openConnection(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    def openChannel(self):
        self.channel = self.connection.channel()

    def openQueue(self, queue_name):
        self.queue_name = queue_name
        self.routing_key = queue_name
        self.channel.queue_declare(self.queue_name)

    # Every queue is automatically bound to the defaultexchange
    # with a routing key which is the same as the queue name.
    def sendMsg(self, msg):
        data = pickle.dumps(msg)
        self.channel.basic_publish(exchange='',
                              routing_key=self.routing_key,
                              body=data)

    def addCallbackFunc(self, callback_func):
        self.channel.basic_consume(callback_func,
                          queue=self.queue_name,
                          no_ack=True)

    def recvMsg(self):
        try:
            self.channel.start_consuming()
        except Exception as e:
            self.view_traceback()
        finally:
            self.closeConnection()
            raise Exception("recvMsg corrupt on queue %s" % self.queue_name)

    def closeConnection(self):
        self.connection.close()

    def view_traceback(self):
        ex_type, ex, tb = sys.exc_info()
        traceback.print_tb(tb)
        del tb


