from datascience import *
import ast

step_table = Table(['trial', 'inputs', 'waypoint', 'action'])
trial_table = Table(['trial', 'final_deadline', 'net_reward', 'success'])

fh = open('0101.txt')
for line in fh.readlines():
	if "Simulator" in line:
		trial = [int(s) for s in line.split() if s.isdigit()][0]
		continue

	if "Step data" in line:
		d = ast.literal_eval(line[line.find("{"):])
		step_table.with_row([trial, d['inputs'], d['waypoint'], d['action']])
	elif "Trial data" in line:
		d = ast.literal_eval(line[line.find("{")+1:])
		trial_table.with_row([trial, d['final_deadline'], d['net_reward'], d['success']])


step_table.show()
trial_table.show()