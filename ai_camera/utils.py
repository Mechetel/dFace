from tensorflow.keras.layers import Conv2D, Dense, ZeroPadding2D, BatchNormalization, Activation
import tensorflow as tf


def LRN2D(x):
    return tf.nn.lrn(x, alpha=1e-4, beta=0.75)

def conv2d_bn(x,
        layer=None,
        cv1_out=None,
        cv1_filter=(1, 1),
        cv1_strides=(1, 1),
        cv2_out=None,
        cv2_filter=(3, 3),
        cv2_strides=(1, 1),
        padding=None,
    ):
    num = '' if cv2_out == None else '1'
    tensor = Conv2D(cv1_out, cv1_filter, strides=cv1_strides, name=layer+'_conv'+num)(x)
    tensor = BatchNormalization(axis=3, epsilon=0.00001, name=layer+'_bn'+num)(tensor)
    tensor = Activation('relu')(tensor)
    if padding == None:
        return tensor
    tensor = ZeroPadding2D(padding=padding)(tensor)
    if cv2_out == None:
        return tensor
    tensor = Conv2D(cv2_out, cv2_filter, strides=cv2_strides, name=layer+'_conv'+'2')(tensor)
    return tensor
