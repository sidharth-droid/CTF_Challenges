#!/usr/bin/env python3
import sys

def validate_flag(submitted_flag):
    expected_flag = "CTF{L4tt1c3_St3g0_1s_Qu4ntum_S4f3}"
    if submitted_flag.strip() == expected_flag:
        return True
    else:
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validator.py <flag>")
        sys.exit(1)
    
    if validate_flag(sys.argv[1]):
        print("Correct! Flag verified.")
    else:
        print("Invalid flag.")
