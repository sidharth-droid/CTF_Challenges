# custom_ops/__init__.py
import torch
import torch.nn as nn
import torch.nn.functional as F
import struct

class CustomLinear(nn.Module):
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = nn.Parameter(torch.Tensor(out_features, in_features))
        if bias:
            self.bias = nn.Parameter(torch.Tensor(out_features))
        else:
            self.register_parameter('bias', None)
        nn.init.kaiming_uniform_(self.weight, a=5.0)
        if bias:
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / (fan_in ** 0.5) if fan_in > 0 else 0
            nn.init.uniform_(self.bias, -bound, bound)
    
    def forward(self, input):
        return F.linear(input, self.weight, self.bias)

class WeightObfuscator(nn.Module):
    def __init__(self):
        super().__init__()
    
    def forward(self, x):
        return x

class DynamicGraphLayer(nn.Module):
    def __init__(self):
        super().__init__()
        self.control_param = nn.Parameter(torch.tensor(1.0))
    
    def forward(self, x):
        return x * self.control_param
