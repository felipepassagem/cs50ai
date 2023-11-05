\# Model Testing and Conclusions

In the course of my experiments with different model architectures, I have drawn several key conclusions. It is important to note that these observations may not be universally applicable and could be specific to the problem at hand.

\## Key Conclusions

1. \*\*Increasing Convolutional Layers:\*\* Simply increasing the number of convolutional layers does not necessarily lead to a proportional improvement in model accuracy.

1. \*\*Kernel Overload:\*\* Overloading a layer with an excessive number of kernels may not enhance accuracy and, in fact, can significantly slow down both model training and inference.

1. \*\*Pooling Layer Requirement:\*\* At least one pooling layer is essential, as the absence of pooling can lead to significantly longer model execution times.

1. \*\*Dropout Recommendation:\*\* To mitigate the risk of overfitting, it is recommended to incorporate dropout layers in the model architecture.

\## Experiment Details

\### Test 1

model = tf.keras.Sequential([

tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input\_shape=(IMG\_WIDTH, IMG\_HEIGHT, 3)),

tf.keras.layers.MaxPooling2D((2, 2)),

tf.keras.layers.Flatten(),

tf.keras.layers.Dense(NUM\_CATEGORIES, activation='softmax'),

])


Key Aspects:

One Conv2D layer

One pooling layer

No dropout layer

Performance: The model performed well with an accuracy of approximately 96%, but it lacked measures to prevent overfitting.

\### Test 2

model = tf.keras.Sequential([

tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input\_shape=(IMG\_WIDTH, IMG\_HEIGHT, 3)),

tf.keras.layers.MaxPooling2D((2, 2)),

tf.keras.layers.Flatten(),

tf.keras.layers.Dense(NUM\_CATEGORIES, activation='softmax'),

tf.keras.layers.Dropout(0.4),

])

Key Aspects:

One Conv2D layer

One pooling layer

Dropout layer (0.4)

Performance: The model's performance was slightly worse after adding dropout. The next experiment introduced more layers and pooling

\### Test 3

model = tf.keras.Sequential([

tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input\_shape=(IMG\_WIDTH, IMG\_HEIGHT, 3)),

tf.keras.layers.MaxPooling2D((4, 4)),

tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input\_shape=(IMG\_WIDTH, IMG\_HEIGHT, 3)),

tf.keras.layers.MaxPooling2D((2, 2)),

tf.keras.layers.Flatten(),

tf.keras.layers.Dense(NUM\_CATEGORIES, activation='softmax'),

tf.keras.layers.Dropout(0.4),

])

Key Aspects:

One Conv2D layer

Two pooling layers

Dropout layer (0.4)

Performance: Results varied between 0.4 and 0.8. The first pooling layer changed to (4, 4), and reverting it to (2, 2) significantly improved results.

\### Test 4

model = tf.keras.Sequential([

tf.keras.layers.Conv2D(N, (3, 3), activation='relu', input\_shape=(IMG\_WIDTH, IMG\_HEIGHT, 3)),

tf.keras.layers.MaxPooling2D((2, 2)),

tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input\_shape=(IMG\_WIDTH, IMG\_HEIGHT, 3)),

tf.keras.layers.MaxPooling2D((2, 2)),

tf.keras.layers.Conv2D(N, (3, 3), activation='relu', input\_shape=(IMG\_WIDTH, IMG\_HEIGHT, 3)),

tf.keras.layers.MaxPooling2D((2, 2)),

tf.keras.layers.Flatten(),

tf.keras.layers.Dropout(0.4),

tf.keras.layers.Dense(NUM\_CATEGORIES, activation='softmax'),

])

Key Aspects:

Number of filters in the layers significantly affected results.

N set to 32 resulted in poor performance, whereas N set to 64 provided more consistent results (~0.9).

Experimenting with two 128 layers led to slower execution with marginal improvement in results.

\### Test 5

model = tf.keras.Sequential([

tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input\_shape=(IMG\_WIDTH, IMG\_HEIGHT, 3)),

tf.keras.layers.MaxPooling2D((2, 2)),

tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input\_shape=(IMG\_WIDTH, IMG\_HEIGHT, 3)),

tf.keras.layers.Flatten(),

tf.keras.layers.Dropout(0.3),

tf.keras.layers.Dense(NUM\_CATEGORIES, activation='softmax'),

])

Key Aspects:

Two convolutional layers (32, 64)

One pooling layer (2, 2)

Dropout layer (0.3)

Aparently, 2 layers first 32, second 64 and one pooling (2,2) with .3 dropout bring very satisfying results(~=.95), while keeping the model light and simple.
