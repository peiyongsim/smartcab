file_to_read = '0101.txt'
fh = open(file_to_read)

i = 1
num_success = 0
num_aborted = 0
num_lines = 0

for line in fh.readlines():
	if i % 2 == 0:
		output = line.strip()
		num_lines += 1
		if "aborted" in output:
			num_aborted += 1
		else:
			num_success += 1
	i += 1

alpha = 0.1
gamma = 0.1
epsilon = 0.05
print("alpha: " + str(alpha))
print("gamma: " + str(gamma))
print("epsilon: " + str(epsilon))
a = num_aborted/num_lines
print("abortion rate: %.2f" % a)
s = num_success/num_lines
print("success rate: %.2f" % s)
print(num_success+num_aborted == num_lines)