import torch
import torch.nn as nn
import struct

def solve_challenge():
    # Step 1: Load and analyze the state_dict
    state_dict = torch.load('obfuscated_model.pth', map_location='cpu', weights_only=True)
    
    print("=== Analyzing Model Weights ===")
    for key, tensor in state_dict.items():
        print(f"{key}: {tensor.shape}")
    
    # Step 2: Deduce model architecture from weight shapes
    # layer1.weight: [256, 128] -> in_features=128, out_features=256
    # layer2.weight: [128, 256] -> in_features=256, out_features=128  
    # layer3.weight: [64, 128]  -> in_features=128, out_features=64
    
    class ReconstructedModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.layer1 = nn.Linear(128, 256)
            self.layer2 = nn.Linear(256, 128)
            self.layer3 = nn.Linear(128, 64)
    
    # Step 3: Load weights into reconstructed model
    model = ReconstructedModel()
    model.load_state_dict(state_dict)
    model.eval()
    
    print("\n=== Extracting Flag ===")
    
    flag_chars = []
    
    # Method 1: Extract from layer1 bias (first 16 characters)
    print("Extracting from layer1.bias...")
    bias_data = model.layer1.bias.data
    for i in range(16):
        if i < len(bias_data):
            # Reverse: char = value * 1000
            encoded_value = bias_data[i].item()
            char_code = int(round(encoded_value * 1000))
            if 32 <= char_code <= 126:  # Printable ASCII range
                char = chr(char_code)
                flag_chars.append(char)
                print(f"  Position {i}: {encoded_value:.6f} -> {char_code} -> '{char}'")
    
    # Method 2: Extract from layer2 weight diagonal (next 16 characters)  
    print("\nExtracting from layer2.weight diagonal...")
    weight_data = model.layer2.weight.data
    for i in range(16):
        if i < min(weight_data.size(0), weight_data.size(1)):
            # Reverse: char = value * 10000
            encoded_value = weight_data[i, i].item()
            char_code = int(round(encoded_value * 10000))
            if 32 <= char_code <= 126:
                char = chr(char_code)
                flag_chars.append(char)
                print(f"  Position {i}: {encoded_value:.6f} -> {char_code} -> '{char}'")
    
    # Method 3: Extract from layer3 weights as floats (remaining characters)
    print("\nExtracting from layer3.weight as floats...")
    weight_flat = model.layer3.weight.data.view(-1)
    chars_extracted = 0
    max_chars_needed = 10  # We need about 8 more characters
    
    for i in range(len(weight_flat)):
        if chars_extracted >= max_chars_needed:
            break
            
        encoded_value = weight_flat[i].item()
        if abs(encoded_value) > 1e-10:  # Only check non-zero values
            # Reverse: original_float = value * 100
            original_float = encoded_value * 100
            try:
                # Convert float back to bytes and extract character
                float_bytes = struct.pack('f', original_float)
                # The character is stored in the first byte (repeated 4 times)
                char = chr(float_bytes[0])
                if 32 <= ord(char) <= 126 and char.isprintable():
                    flag_chars.append(char)
                    chars_extracted += 1
                    print(f"  Position {i}: {encoded_value:.10f} -> float -> '{char}'")
            except (struct.error, ValueError):
                continue
    
    # Step 4: Assemble the flag
    flag = ''.join(flag_chars)
    
    print(f"\n=== Reconstructed Flag ===")
    print(f"Raw extracted: {flag}")
    print(f"Length: {len(flag)}")
    
    # The flag should be exactly 40 characters
    if len(flag) >= 40:
        final_flag = flag[:40]
        print(f"\nFinal Flag: {final_flag}")
        return final_flag
    else:
        print("Could not extract complete flag")
        return None

def alternative_solution():
    """Alternative approach without reconstructing full model"""
    print("\n" + "="*50)
    print("ALTERNATIVE SOLUTION APPROACH")
    print("="*50)
    
    state_dict = torch.load('obfuscated_model.pth', map_location='cpu', weights_only=True)
    
    flag_chars = []
    
    # Direct extraction from state_dict
    # Layer1 bias extraction
    bias_data = state_dict['layer1.bias']
    for i in range(16):
        char_code = int(round(bias_data[i].item() * 1000))
        if 32 <= char_code <= 126:
            flag_chars.append(chr(char_code))
    
    # Layer2 diagonal extraction  
    weight_data = state_dict['layer2.weight']
    for i in range(16):
        char_code = int(round(weight_data[i, i].item() * 10000))
        if 32 <= char_code <= 126:
            flag_chars.append(chr(char_code))
    
    # Layer3 float extraction
    weight_flat = state_dict['layer3.weight'].view(-1)
    for i in range(10):
        try:
            original_float = weight_flat[i].item() * 100
            float_bytes = struct.pack('f', original_float)
            char = chr(float_bytes[0])
            if char.isprintable():
                flag_chars.append(char)
        except:
            pass
    
    flag = ''.join(flag_chars)
    print(f"Alternative method flag: {flag}")
    return flag

if __name__ == "__main__":
    print("CTF Challenge 2: Neural Network Obfuscation")
    print("Solution Script\n")
    
    # Main solution
    flag1 = solve_challenge()
    
    # Alternative solution
    flag2 = alternative_solution()
    
    # Verify with validator
    if flag1 and flag1 == flag2:
        print(f"\nVERIFIED: CTF{{{flag1}}}")
        
        # Test with validator
        import subprocess
        import sys
        result = subprocess.run([sys.executable, 'validator.py', flag1], 
                              capture_output=True, text=True)
        print(f"Validator output: {result.stdout}")
    else:
        print("\nExtraction methods produced different results")
        print(f"Method 1: {flag1}")
        print(f"Method 2: {flag2}")
