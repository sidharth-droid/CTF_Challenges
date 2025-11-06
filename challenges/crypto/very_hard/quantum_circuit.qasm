OPENQASM 2.0;
include "qelib1.inc";

qreg q[6];
creg c[6];

// Simon's Algorithm variant with deliberate noise
h q[0];
h q[1];
h q[2];
h q[3];

// Oracle for secret period s = 101101
cx q[0], q[4];
cx q[1], q[4];
cx q[0], q[5];
cx q[2], q[5];
cx q[3], q[4];
cx q[3], q[5];

// Deliberate flaw: controlled noise injection
// This creates interference patterns that leak the period
rz(pi/8) q[0];
rz(pi/8) q[1];
rz(pi/8) q[2];
rz(pi/8) q[3];

h q[0];
h q[1];
h q[2];
h q[3];

// Measurements create probability distribution with period info
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
measure q[4] -> c[4];
measure q[5] -> c[5];
