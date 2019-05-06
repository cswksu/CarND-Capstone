from styx_msgs.msg import TrafficLight
import tensorflow as tf
from tensorflow.contrib.layers import *
import numpy as np
from PIL import Image
import os

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        self.cwd = os.getcwd()
        self.sess=tf.Session()
        saver = tf.train.import_meta_graph(self.cwd+'/light_classification/lenet.meta')
        graph = tf.get_default_graph()
        saver.restore(self.sess, tf.train.latest_checkpoint(self.cwd+'/light_classification/'))
        self.x1 = graph.get_tensor_by_name("x1:0")
        self.prediction = graph.get_tensor_by_name("predict:0")
        #logits = LeNet(X_train)
        #cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_train, logits=logits)
        #loss_operation = tf.reduce_mean(cross_entropy)
        #optimizer = tf.train.AdamOptimizer(learning_rate = rate)
        #training_operation = optimizer.minimize(loss_operation)
        #correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(y_train, 1))
        #accuracy_operation = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))



    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        image1=Image.fromarray(image)
        image1=image1.resize((72,72))
        im=np.float32(np.asarray(image1))
        im=np.true_divide(im,128.0)
        im=np.subtract(im,1.0)
        imArr=np.array([im])
        ans=-1
        sess1=self.sess
        ans=int(sess1.run(self.prediction, feed_dict = {self.x1: imArr[0:1]})[0])
        print(ans)
        #sess=self.sess
        #feed_dict = {x1: im}
        #answer=sess.run(tf.nn.softmax(self.logits), feed_dict = {self.x1: im})
        #ans=int(np.argmax(answer[0,:]))
        #with tf.Session() as sess:
            #saver = tf.train.import_meta_graph(self.cwd+'/light_classification/lenet.meta')
            #graph = tf.get_default_graph()
            #saver.restore(sess, tf.train.latest_checkpoint(self.cwd+'/light_classification/'))
            #sess.run(tf.global_variables_initializer())
            #x1 = graph.get_tensor_by_name("x1:0")
            #logits = graph.get_tensor_by_name("logits1:0")
            #feed_dict = {x1: im}
            #answer=sess.run(tf.nn.softmax(logits))
            #ans=int(np.argmax(answer[0,:]))

        if ans==3:
            ans=4
        #TODO implement light color prediction
        return ans
