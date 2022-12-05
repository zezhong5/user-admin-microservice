import logging
import boto3
import json
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

topicArns = {
    "RegConfirmTopic": 'arn:aws:sns:us-east-2:148730754678:RegConfirmTopic',
}

class SnsWrapper:

    @staticmethod
    def PublishRegConfirmTopic(link):
        topicArn=topicArns['RegConfirmTopic']
        try:
            snsClient = boto3.client(
                'sns',
                aws_access_key_id='AKIASFIILGZ3O7F7NTW3',
                aws_secret_access_key='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',
                region_name='us-east-2'
            )
            response=snsClient.publish(
                TopicArn=topicArn,
                Message=link
            )
            message_id = response['MessageId']
            logger.info(
                logger.info("Publish message to topic %s.", topicArn)
            )
        except ClientError:
            logger.info(
                logger.exception("Couldn't publish message to topic %s", topicArn)
            )
        else:
            return message_id



    # def __init__(self, sns_resource):
    #     self.sns_resource = sns_resource

#     def list_topics(self):
#         try:
#             topics_iter = self.sns_resource.topics.all()
#             logger.info("Got Topics.")
#         except ClientError:
#             logger.exception("Couldn't get topics.")
#             raise
#         else:
#             return topics_iter

#     @staticmethod
#     def publish_message(topic, message, attributes):
#         """
#         Publishes a message, with attributes, to a topic. Subscriptions can be filtered
#         based on message attributes so that a subscription receives messages only
#         when specified attributes are present.
#         :param topic: The topic to publish to.
#         :param message: The message to publish.
#         :param attributes: The key-value attributes to attach to the message. Values
#                            must be either `str` or `bytes`.
#         :return: The ID of the message.
#         """
#         try:
#             att_dict = {}
#             for key, value in attributes.items():
#                 if isinstance(value, str):
#                     att_dict[key] = {'DataType': 'String', 'StringValue': value}
#                 elif isinstance(value, bytes):
#                     att_dict[key] = {'DataType': 'Binary', 'StringValue': value}

#             response = topic.publish(Message=message, MessageAttributes=att_dict)
#             message_id = response['MessageId']
#             logger.info(
#                 logger.info("Publish message with attributes %s to topic %s.", attributes, topic.arn)
#             )
#         except ClientError:
#             logger.info(
#                 logger.exception("Couldn't publish message to topic %s", topic.arn)
#             )
#             raise
#         else:
#             return message_id

# def usage_demo():
#     print('-' * 88)
#     print("Welcome to the Amazon Simple Notification Service (Amazon SNS) demo!")
#     print('-' * 88)

#     logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

#     sns_wrapper = SnsWrapper(boto3.resource('sns'))
#     topics = sns_wrapper.list_topics()
#     for topic in topics:
#         print(topic)

# if __name__=='__main__':
#     usage_demo()