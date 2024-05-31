import numpy as np

class DenseLayer():
    def __init__(self,input_nodes : int, output_nodes : int):
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes
        #creates matrix output (lines) by input (columns)
        self.weight = np.random.randn(self.output_nodes * self.input_nodes).reshape((self.output_nodes,self.input_nodes))
        #randomly initialize parameters and adapt them with gradient descent so becomes most optimal
        self.bias = np.random.randn(self.output_nodes)
        self.gradient = None
        self.input = None
    def forward(self,X : np.ndarray) -> np.ndarray:
        self.input = X
        return self.weight @ X + self.bias #matric mutiplication with bias
    def backward(self,delta):
        pass


# sample_input = np.array([0.5,0.5])
# dense_layer = DenseLayer(2,4)

# # print(dense_layer.forward(sample_input))

class ReluActivation:
    # 0 if smaller than 0 and itself if bigger
    def forward(self,X):
        return np.maximum(X,0) 
        

class SigmoidActivation:
    def forward(self,X):
        return 1 / (1 + np.exp(-X))
    
# sigmoid_activation = SigmoidActivation()
# # print(sigmoid_activation.forward(np.array([10000,-10000,0])))

# relu_activation = ReluActivation()
# print(relu_activation.forward(np.array([-25,0,125])))

class MSELoss:
    def forward(self,y_true,y_pred):
        return np.mean((y_true - y_pred)**2)
    
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