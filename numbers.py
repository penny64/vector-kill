def interp(n1, n2, t):
	return n1 + (n2-n1) * t

def clip(number, start, end):
	return max(start, min(number, end))