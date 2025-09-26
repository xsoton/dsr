import pyvisa

rm = pyvisa.ResourceManager('@py')


k = rm.open_resource('GPIB0::25::INSTR')
k.timeout = 25000

k.write("output1 off")
k.write("output2 off")
k.write("system:azero on")
k.write("sense1:current:range:auto on")
k.write("sense1:current:nplcycles 10")
k.write("sense1:average off")
k.write("sense1:average:count 10")
k.write("sense1:average:tcontrol repeat")
k.write("source1:gconnect 0")
k.write("source1:voltage:mode fixed")
k.write("source1:voltage 0")
k.write("system:azero on")
k.write("sense2:current:range:auto on")
k.write("sense2:current:nplcycles 10")
k.write("sense2:average off")
k.write("sense2:average:count 10")
k.write("sense2:average:tcontrol repeat")
k.write("source2:gconnect 0")
k.write("source2:voltage:mode fixed")
k.write("source2:voltage 0")

# k.write("output1 on")
# k.write("output2 on")

while True:
	k.write("read?")
	print(k.read().encode())
