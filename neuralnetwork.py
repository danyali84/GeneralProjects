import numpy as np

#stochastic gradient descent
class SGDOptimizer:
    def __init__(self,lr : float):
        self.lr = lr
    def apply(self,vector,dvector):
        return vector * dvector * self.lr


class DenseLayer():
    def __init__(self,input_nodes : int, output_nodes : int):
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes
        #creates matrix output (lines) by input (columns)
        self.weight = np.random.randn(self.output_nodes * self.input_nodes).reshape((self.output_nodes,self.input_nodes))
        #randomly initialize parameters and adapt them with gradient descent so becomes most optimal
        self.bias = np.random.randn(self.output_nodes)
        self.gradient_weight = None
        self.gradient_bias = None
        self.input = None
    def forward(self,X : np.ndarray) -> np.ndarray:
        self.input = X
        return self.weight @ X + self.bias #matric mutiplication with bias
    def backward(self,delta):
        self.gradient_weight = delta.reshape((self.output_nodes,1)) @ self.input.reshape((1,self.input_nodes))
        self.gradient_bias = delta
        dX = self.weight.T @ delta
        return dX
    def apply(self, opt):
        self.weight = opt.apply(self.weight,self.gradient_weight)
        self.bias = opt.apply(self.bias, self.gradient_bias)


sample_input = np.array([0.5,0.5])
dense_layer = DenseLayer(2,4)

# print(dense_layer.forward(sample_input))
# print(np.random.randn(4).reshape((4,1)) @ np.random.randn(2).reshape((1,2)))

class ReluActivation:
    def __init__(self):
        self.input = None
        self.gradient = None
    # 0 if smaller than 0 and itself if bigger
    def forward(self,X):
        self.input = X
        return np.maximum(X,0) 
    def backward(self,delta):
        #delta is the incoming gradient
        drelu = np.zeros_like(self.input)
        drelu[self.input > 0]= 1
        #hadamard product (elementary prod between relu activation gradients with incoming gradients from outer side)
        return drelu * delta

# sigmoid_activation = ReluActivation()
# print(sigmoid_activation.forward(np.array([-0.5,2,0])))
# print(sigmoid_activation.backward(np.array([0.3,0.2,0.1])))

class SigmoidActivation:
    def __init__(self):
        # self.input = None
        self.gradient = None
        #easier, more efficient to use output to calculate gradient instead of input
        self.output = None
    def forward(self,X):
        # self.input = X
        self.output = 1 / (1 + np.exp(-X))
        return self.output
    def backward (self,delta):
        dsigmoid = self.output * (1 - self.output)
        return dsigmoid * delta
    
# sigmoid_activation = SigmoidActivation()
# print(sigmoid_activation.forward(np.array([10000,-10000,0])))
# print(sigmoid_activation.forward(np.array([-0.5,2,0])))
# print(sigmoid_activation.backward(np.array([0.3,0.2,0.1])))

# relu_activation = ReluActivation()
# print(relu_activation.forward(np.array([-25,0,125])))

class MSELoss:
    def forward(self,y_true,y_pred):
        return 0.5 * np.mean((y_true - y_pred)**2)
    def backward(self,y_true,y_pred):
        return y_pred - y_true

    
# mse = MSELoss()
# print(mse.forward(np.array([1,2]), np.array([1,1])))

class NeuralNetwork:
    def __init__(self,layers,loss):
        self.layers = layers
        self.loss = loss
    def forward(self,X):
        current_input = X
        for layer in self.layers:
            current_input = layer.forward(current_input)
        return current_input
    
