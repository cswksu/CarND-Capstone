from styx_msgs.msg import TrafficLight
#import tensorflow as tf
#from tensorflow.contrib.layers import *
import numpy as np
from PIL import Image
#import os

class TLClassifier(object):
    def __init__(self):
        pass



    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #image=Image.open(infile)
        #im=np.asarray(image)
        greenSum=0
        redSum=0
        yellowSum=0
        #imShape=im.shape
        #xDim=imShape[0]
        #yDim=imShape[1]
        PILimage=Image.fromarray(image)
        imShape=image.shape
        xDim=imShape[0]
        yDim=imShape[1]
        PILimage=PILimage.resize((xDim/4,yDim/4))
        im=np.asarray(PILimage)
        imShape=im.shape
        xDim=imShape[0]
        yDim=imShape[1]
        ans=4
        for x in range(xDim):
            for y in range(yDim):
                blue=im[x, y, 0]
                green=im[x, y, 1]
                red=im[x, y, 2]
                if (blue<55) and (blue>25) and (green>235) and (red>235):
                    yellowSum=yellowSum+1
                elif (red>200) and (blue<100) and (green<100):
                    redSum=redSum+1
                elif (green>225) and (blue<75) and (red<75):
                    greenSum=greenSum+1
        maxSum=max([yellowSum, redSum, greenSum])
        if maxSum>=5:
            if (greenSum>redSum) and (greenSum>yellowSum):
                ans=2
            elif (redSum>yellowSum):
                ans=0
            else:
                ans=1
        return ans
        #image1=Image.fromarray(image)
        #image1=image1.resize((72,72))
        #im=np.float32(np.asarray(image1))
        #im=np.true_divide(im,128.0)
        #im=np.subtract(im,1.0)
        #imArr=np.array([im])
        #ans=-1
        #sess1=self.sess
        #ans=int(sess1.run(self.prediction, feed_dict = {self.x1: imArr[0:1]})[0])
        #print(ans)
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

        #if ans==3:
        #    ans=4
        #TODO implement light color prediction
        #return ans
