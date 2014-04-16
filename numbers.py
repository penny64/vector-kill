def interp(n_1, n_2, t):
	return n_1 + (n_2-n_1) * t

def interp_velocity(velocity_1, velocity_2, interp_by):
	return [interp(velocity_1[0], velocity_2[0], interp_by),
	        interp(velocity_1[1], velocity_2[1], interp_by)]

def clip(number, start, end):
	return max(start, min(number, end))

def distance(pos_1, pos_2, old=False):
	if old:
		return abs(pos_1[0]-pos_2[0])+abs(pos_1[1]-pos_2[1])

	x_dist = abs(pos_1[0]-pos_2[0])
	y_dist = abs(pos_1[1]-pos_2[1])

	if x_dist > y_dist:
		return y_dist + (x_dist-y_dist)
	else:
		return x_dist + (y_dist-x_dist)
