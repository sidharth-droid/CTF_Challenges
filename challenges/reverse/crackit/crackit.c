#include <stdio.h>
#include <string.h>

void check_password(char *input) {
    char correct[] = {0x46, 0x4C, 0x41, 0x47, 0x7B, 0x52, 0x45, 0x76, 0x5F, 0x30, 0x62, 0x66, 0x75, 0x73, 0x63, 0x61, 0x74, 0x65, 0x7D, 0x00}; 
    if (strcmp(input, correct) == 0) {
        printf("Correct! Here is your flag: %s\n", correct);
    } else {
        printf("Wrong password! Try again.\n");
    }
}

int main() {
    char input[20];
    printf("Enter password: ");
    scanf("%19s", input);
    check_password(input);
    return 0;
}
