import numpy as np 
import tensorflow as tf
from tensorflow.python.platform import gfile
from nested_lstm import NestedLSTM

sample = np.array( [[
                    [0, 1, 0, 0],
                    [ 0, 1, 0, 0],
                    [0, 1, 0, 0]
                    ]] )

with tf.compat.v1.Session() as sess:	    
	with gfile.FastGFile('../models/model.pb', 'rb') as f:	        
		graph_def = tf.compat.v1.GraphDef()	        
		graph_def.ParseFromString(f.read())	        
		sess.graph.as_default()	        
		g_in = tf.compat.v1.import_graph_def(graph_def)	        
		tensor_input = sess.graph.get_tensor_by_name('import/input_layer:0')	        
		tensor_output = sess.graph.get_tensor_by_name('import/output_layer/BiasAdd:0')	        
		predictions = sess.run(tensor_output, {tensor_input:sample})	        
		print(predictions)	        


from keras.models import load_model
commands = open("initialize.py").read()
exec(commands)
 
model = load_model('../models/model.h5', 
	  custom_objects={'NestedLSTM':NestedLSTM})
<<<<<<< HEAD
print(model.predict(sample))
=======

output = model.predict(sample)
print(output)
#print(tf.gradient(output, sample))
>>>>>>> ffc647349d466eea01eb25c825a8c0f3e1fd9083
