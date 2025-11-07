#!/bin/bash
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:./vulnerable_service,stderr
