#!/bin/bash
echo "Compiling vulnerable VM service..."
gcc -o vulnerable_service vulnerable_vm_service.c -fno-stack-protector -z execstack -no-pie -static
echo "Compilation complete!"
ls -la vulnerable_service
