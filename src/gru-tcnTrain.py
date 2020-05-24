from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Input, Dropout, Flatten, GRU, Bidirectional
from keras.models import  Model, Sequential
from keras.layers.normalization import BatchNormalization
from mytcn import TCN
from numpy.random import seed
from tensorflow import set_random_seed 
from keras_radam import RAdam
from keras_self_attention import SeqSelfAttention

seed(1)
set_random_seed(2)

commands = open("timeSeries.py").read()
exec(commands)
model_path    = '../models/model-gru-tcn.h5'

X = []
Y = []
for i in range(1,37,2):
    indices = data['testid'].isin([i])
    for x in InputToTimeSeries(data_scaled[indices][:,time_series_feature_columns], np.array(data.loc[indices,'converged'])):
        X.append(x)
    for y in InputToTimeSeries(data_scaled[indices][:,target_columns], np.array(data.loc[indices,'converged'])):
        Y.append(y[-1])
X = np.array(X)
Y = np.array(Y)

X_val = []
Y_val = []
for i in range(2,38,2):
    indices = data_noiter['testid'].isin([i])
    for x in InputToTimeSeries(data_scaled_noiter[indices][:, time_series_feature_columns]):
        X_val.append(x)
    for y in  InputToTimeSeries(data_scaled_noiter[indices][:, target_columns]):
        Y_val.append(y[-1])
X_val = np.array(X_val)
Y_val = np.array(Y_val)

i = Input(shape=(time_series_steps, len(time_series_feature_columns)), name='input_layer')
o = GRU(128, return_sequences=True, input_shape=(time_series_steps, len(time_series_feature_columns)), name='gru_layer1') (i)
o = Dropout(0.2)(o)
o = TCN(nb_filters=8, kernel_size=4, dilations=[1,2,4], activation='wavenet', name='tcn_layer1')(o)
o = Flatten()(o)
o = Dense(2, name='output_layer') (o)

model = Model(inputs = [i], outputs=[o])
model.compile(loss=huber_loss(), optimizer=RAdam())
print(model.summary())
history = model.fit(X, Y, epochs = 20000, batch_size = 1024, validation_data = (X_val, Y_val),
					callbacks = [ModelCheckpoint(model_path, monitor = 'val_loss', save_best_only = True)])
pd.DataFrame(history.history).to_csv("../results/train-grutcn.csv")

