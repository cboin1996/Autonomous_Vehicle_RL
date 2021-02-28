import tensorflow as tf
from tensorflow.keras import layers

def get_actor(num_states, num_actions, high_bound, weight_init=True, seed_int=None, hidd_mult=1):
    """Get an actor network

    Args:
        num_states (int): number of states from the environment
        upper_bound ([type]): used for scaling the actions
        weight_init (bool): whether to initialize the weights of the network randomly or not
        seed_int (int): a seed for the random number generator

    Returns:
        model: the tensorflow model
    """
    if weight_init == True:
        # Initialize weights between -3e-3 and 3-e3
        last_init = tf.random_uniform_initializer(minval=-0.003, maxval=0.003, seed=seed_int)

    inputs = layers.Input(shape=(num_states))
    out = layers.Dense(int(300 * hidd_mult), activation="relu")(inputs)
    out = layers.BatchNormalization()(out)
    out = layers.Dense(int(600 * hidd_mult), activation="relu")(out)
    out = layers.BatchNormalization()(out)
    if weight_init == True:
        outputs = layers.Dense(num_actions, activation="tanh", kernel_initializer=last_init)(out)
    else:
        outputs = layers.Dense(num_actions, activation="tanh")(out)

    outputs = outputs * high_bound
    model = tf.keras.Model(inputs, outputs)
    return model


def get_critic(num_states, num_actions, hidd_mult=1):
    """get the critic network

    Args:
        num_states (int): the number of states from the environment
        num_actions (int): the number of actions from the environment

    Returns:
        model: the critic model
    """
    # State as input
    state_input = layers.Input(shape=(num_states))
    state_out = layers.Dense(int(300 * hidd_mult), activation="relu")(state_input)
    state_out = layers.BatchNormalization()(state_out)

    # Action as input
    action_input = layers.Input(shape=(num_actions))
    action_out = layers.Dense(int(600 * hidd_mult), activation="relu")(action_input)
    action_out = layers.BatchNormalization()(action_out)

    # Both are passed through seperate layer before concatenating
    concat = layers.Concatenate()([state_out, action_out])

    out = layers.Dense(int(600 * hidd_mult), activation="relu")(concat)
    out = layers.BatchNormalization()(out)

    outputs = layers.Dense(num_actions)(out)

    # Outputs single value for give state-action
    model = tf.keras.Model([state_input, action_input], outputs)

    return model