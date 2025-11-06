import torch
import torch.nn as nn
import torch.nn.functional as F
import struct
import numpy as np

# Define the classes directly in the script
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
        self.reset_parameters()
    
    def reset_parameters(self):
        nn.init.kaiming_uniform_(self.weight, a=5.0)
        if self.bias is not None:
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / (fan_in ** 0.5) if fan_in > 0 else 0
            nn.init.uniform_(self.bias, -bound, bound)
    
    def forward(self, input):
        return F.linear(input, self.weight, self.bias)

class ObfuscatedNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        
        # Main layers
        self.layer1 = CustomLinear(128, 256)
        self.layer2 = CustomLinear(256, 128)
        self.layer3 = CustomLinear(128, 64)
        
        # Flag hidden in multiple weight matrices
        self._hide_flag_in_weights()
    
    def _hide_flag_in_weights(self):
        flag = "CTF{N3ur4l_0bfU5c4t10n_1s_Fut1l3}"
        
        # Method 1: Direct ASCII in specific weights
        with torch.no_grad():
            # Hide in layer1 bias (first 16 chars)
            for i, char in enumerate(flag[:16]):
                if i < len(self.layer1.bias):
                    self.layer1.bias.data[i] = ord(char) * 1e-3
            
            # Hide in layer2 weight matrix diagonal (next 16 chars)
            for i, char in enumerate(flag[16:32]):
                if i < min(self.layer2.weight.size(0), self.layer2.weight.size(1)):
                    self.layer2.weight.data[i, i] = ord(char) * 1e-4
            
            # Hide remaining characters in layer3 weights as IEEE754 floats
            remaining = flag[32:]
            weight_flat = self.layer3.weight.data.view(-1)
            for i, char in enumerate(remaining):
                if i < len(weight_flat):
                    # Convert char to special float representation
                    try:
                        as_float = struct.unpack('f', char.encode() * 4)[0]
                        weight_flat[i] = as_float * 1e-2
                    except:
                        pass
    
    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = torch.sigmoid(self.layer2(x))
        x = self.layer3(x)
        return x

def create_and_save_model():
    model = ObfuscatedNetwork()
    
    # Save ONLY the state_dict for security
    torch.save(model.state_dict(), 'obfuscated_model.pth')
    
    # Also save model architecture separately if needed
    torch.save({
        'state_dict': model.state_dict(),
        'model_config': {
            'layer1': {'in_features': 128, 'out_features': 256},
            'layer2': {'in_features': 256, 'out_features': 128},
            'layer3': {'in_features': 128, 'out_features': 64}
        }
    }, 'obfuscated_model_safe.pth')
    
    print("Model created and saved!")

if __name__ == "__main__":
    create_and_save_model()
