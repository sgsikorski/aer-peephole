OPENQASM 2.0;
include "qelib1.inc";
qreg q[28];
h q[0];
h q[1];
cp(427*pi) q[0],q[1];
h q[2];
cp(505*pi) q[1],q[2];
h q[3];
cp(1063.4291) q[0],q[3];
cp(1044.5796) q[1],q[3];
cp(1163.9601) q[2],q[3];
