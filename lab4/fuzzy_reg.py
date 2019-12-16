# 1.
import math

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class FuzzyController(object):
	def __init__(self):
		self.max_angle = 25.0 / 180 * math.pi
		inp_discr = 1.0 / 180 * math.pi
		inp_mean = 20.0 / 180 * math.pi
		inp_sigma = 20.0 / 180 * math.pi

		inp_values = np.linspace(-self.max_angle, self.max_angle, int(2 * self.max_angle / inp_discr) + 1)
		input = ctrl.Antecedent(inp_values, 'input')
		input['low'] = fuzz.gaussmf(input.universe, -inp_mean, inp_sigma)
		input['high'] = fuzz.gaussmf(input.universe, inp_mean, inp_sigma)

		self.max_output = 1
		output_discr = 0.1
		outp_mean1 = 0.4
		outp_mean2 = 1
		outp_hbreadth = 0.2

		outp_values = np.linspace(-self.max_output, self.max_output, int(2 * self.max_output / output_discr) + 1)
		output = ctrl.Consequent(outp_values, 'output')
		output['too low'] = fuzz.trimf(output.universe, [-outp_mean2 - outp_hbreadth, -outp_mean2, -outp_mean2 + outp_hbreadth])
		output['low'] = fuzz.trimf(output.universe, [-outp_mean1 - outp_hbreadth, -outp_mean1, -outp_mean1 + outp_hbreadth])
		output['high'] = fuzz.trimf(output.universe, [outp_mean1 - outp_hbreadth, outp_mean1, outp_mean1 + outp_hbreadth])
		output['too high'] = fuzz.trimf(output.universe, [outp_mean2 - outp_hbreadth, outp_mean2, outp_mean2 + outp_hbreadth])

		rule1 = ctrl.Rule(input['low'] , output['high'])
		rule2 = ctrl.Rule(input['high'] , output['low'])
		rule3 = ctrl.Rule(input['high'] , output['too low'])
		rule4 = ctrl.Rule(input['low'] , output['too high'])

		control_system =  ctrl.ControlSystem([rule1, rule2, rule3, rule4])
		self.simulation = ctrl.ControlSystemSimulation(control_system)

	def calc(self, inp_value):
		self.simulation.input['input'] = inp_value
		self.simulation.compute()
		return self.simulation.output['output']
	
	def plot(self, num_points = 100):
		inp = np.linspace(-1.5*self.max_angle, 1.5*self.max_angle, num_points)
		outp = np.zeros(num_points)
		for i in range(num_points):
			outp[i] = self.calc(inp[i])
		plt.plot(inp, outp)
		plt.show()
		
