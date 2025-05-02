#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

// XOR Decryption function
void decrypt_flag(char *enc, int key) {
    for (int i = 0; i < strlen(enc); i++) {
        enc[i] ^= key;
    }
}

// Function to detect if a debugger is present (basic)
int is_debugger_present() {
    FILE *status = fopen("/proc/self/status", "r");
    char line[256];
    
    if (status) {
        while (fgets(line, sizeof(line), status)) {
            if (strstr(line, "TracerPid")) {
                int tracer = atoi(line + 10);
                fclose(status);
                return tracer != 0;  // If TracerPid != 0, debugger detected
            }
        }
        fclose(status);
    }
    return 0;
}

int main() {
    if (is_debugger_present()) {
        printf("Debugger detected! Exiting...\n");
        return 1;
    }

    // Encrypted flag (FLAG{Super_Hard_Rev_CTF})
    char encrypted_flag[] = { 0x35, 0x3F, 0x32, 0x34, 0x08, 0x20, 0x06, 0x03, 0x16, 0x01, 0x2C, 0x3B, 0x12, 0x01, 0x17, 0x2C, 0x21, 0x16, 0x05, 0x2C, 0x30, 0x27, 0x35, 0x0E };

    // Hardcoded XOR key (0x73) instead of random generation
    int xor_key = 0x73; // Key is now fixed

    printf("Enter the secret key: ");
    int user_input;
    scanf("%d", &user_input);

    if (user_input == xor_key) {
        decrypt_flag(encrypted_flag, xor_key);
        printf("Correct! Here is your flag: %s\n", encrypted_flag);
    } else {
        printf("Wrong key! Try again.\n");
    }

    return 0;
}