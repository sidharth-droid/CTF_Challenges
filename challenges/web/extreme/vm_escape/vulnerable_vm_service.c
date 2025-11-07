#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>

#define BUFFER_SIZE 1024

char flag[] = "CTF{HyP3rV1s0r_3sc4p3_Thr0ugh_T1m3}";
char hypervisor_memory[4096];

// Simulated vulnerable hypervisor interface
void vulnerable_hypercall(unsigned long arg1, unsigned long arg2) {
    // This simulates the vulnerable hypercall interface
    printf("[DEBUG] Hypercall received: 0x%lx, 0x%lx\n", arg1, arg2);
    
    // Vulnerable: doesn't properly validate nested VM state
    if (arg1 == 0xDEADBEEF && arg2 == 0xCAFEBABE) {
        printf("[!] Triggering triple fault path...\n");
        printf("[!] VM Escape Successful! Accessing hypervisor memory...\n");
        printf("[FLAG] %s\n", flag);
        exit(0);
    }
    else if (arg1 == 0x1337 && arg2 == 0xCAFE) {
        // Hidden debug backdoor
        printf("[DEBUG] Hypervisor memory dump:\n");
        for (int i = 0; i < 64; i++) {
            printf("%02x ", hypervisor_memory[i]);
            if ((i + 1) % 16 == 0) printf("\n");
        }
    }
}

void handle_connection() {
    char buffer[BUFFER_SIZE];
    unsigned long arg1, arg2;
    
    // Initialize "hypervisor memory" with some data
    memset(hypervisor_memory, 0, sizeof(hypervisor_memory));
    strcpy(hypervisor_memory + 256, flag);
    
    printf("=== Nested VM Debug Interface ===\n");
    printf("Available commands:\n");
    printf("HYPERCALL <arg1> <arg2> - Execute hypercall\n");
    printf("READ <addr> - Read from memory\n");
    printf("EXIT - Close connection\n");
    printf("=================================\n");
    
    while (1) {
        printf("VM> ");
        fflush(stdout);
        
        if (!fgets(buffer, BUFFER_SIZE, stdin)) break;
        
        if (strncmp(buffer, "HYPERCALL", 9) == 0) {
            if (sscanf(buffer + 9, "%lx %lx", &arg1, &arg2) == 2) {
                vulnerable_hypercall(arg1, arg2);
            } else {
                printf("Usage: HYPERCALL <hex_arg1> <hex_arg2>\n");
            }
        }
        else if (strncmp(buffer, "READ", 4) == 0) {
            printf("Memory read disabled in secure mode\n");
        }
        else if (strncmp(buffer, "EXIT", 4) == 0) {
            printf("Closing connection...\n");
            break;
        }
        else if (strncmp(buffer, "HELP", 4) == 0) {
            printf("Available commands:\n");
            printf("HYPERCALL <arg1> <arg2> - Execute hypercall\n");
            printf("READ <addr> - Read from memory\n");
            printf("EXIT - Close connection\n");
        }
        else {
            printf("Unknown command. Type HELP for available commands.\n");
        }
    }
}

int main() {
    printf("Starting Vulnerable VM Service...\n");
    printf("Listening for connections...\n");
    
    // For CTF, we'll handle one connection at a time via socat
    handle_connection();
    
    return 0;
}
