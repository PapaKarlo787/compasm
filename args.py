import re
import nums_to_bytes as ntb


reg_re = "r(\d|1[0-5])$"
int_re = "(0|-?[1-9][0-9]*|0x[0-9a-f]+)$"
float_re = "-?(0\.\d+|[1-9][0-9]*\.\d+)|" + int_re
lable_re = "(([a-z]\w*)*\.*[a-z]\w*)|(\$[0-9]+)$"
nl = 1
last_lables = []


def is_three(data):
	return data[1] == "," and "," not in data[2:]


def is_reg(d):
	return re.match(reg_re, d)


def to_int(n):
	return int(n, 16 if "x" in n else 10)


def get_const(data, l, to_rebuild, k):
	for i in range(len(data)):
		if re.match(lable_re, data[i]):
			data[i] = get_norm_lable(data[i])
			to_rebuild.append([data, l+k, nl, i])
		if data[i] == "$":
			data[i] += str(l)
			to_rebuild.append([data, l+k, nl, i])
	to_rebuild.append([data, l+k, nl, -1])
	return bytes([0]*4)


def rc(data, l, to_rebuild, f):
	if is_three(data) and re.match(reg_re, data[0]):
		r = bytes([int(data[0][1:])])
		if f and (re.match(float_re, data[2]) or re.match(int_re, data[2])):
			return r + ntb.float_to_bytes(float(data[2]))
		return r + get_const(data[2:], l, to_rebuild, 2)
	raise Exception


def rcb(data):
	if is_three(data):
		return r(data[:1])+c(data[2:])
	raise Exception


def cbr(data):
	return rcb(data[::-1])[::-1]


def rr(data):
	if is_three(data) and re.match(reg_re, data[0]) and re.match(reg_re, data[2]):
		return bytes([int(data[2][1:]) * 16 + int(data[0][1:])])
	raise Exception


def cc(data):
	if is_three(data):
		x = c(data[:1]) + c(data[2:])
		if len(x) == 2:
			return x
	raise Exception


def r(data):
	if len(data) == 1 and re.match(reg_re, data[0]):
		return bytes([int(data[0][1:])])
	raise Exception


def c(data):
	if len(data) == 1 and re.match(int_re, data[0]):
		return bytes([to_int(data[0])])
	raise Exception


def jump(c, data, l, to_rebuild):
	return bytes([c]) + get_const(data, l, to_rebuild, 1)


def get_mor(data, l, k1, k2, to_rebuild):
	data = data[1:-1]
	res = [0]
	updated = False
	for i in range(len(data)):
		if re.match(reg_re, data[i]):
			if updated:
				raise Exception("Two registers is not prohibited")
			res[0] = int(data[i][1:]) * 16
			updated = True
			data[i] = "0"
	res += get_const(data, l, to_rebuild, 2)
	return [k2 if updated else k1] + res


def _db(e, l, to_rebuild):
	e = "".join(e)
	if re.match(int_re, e):
		return bytes([to_int(e)])
	if len(e) > 1 and e[0] == '"' and e[-1] == '"':
		return e[1:-1].encode()
	raise Exception


def _df(e, l, to_rebuild):
	e = "".join(e)
	if re.match(float_re, e):
		return ntb.float_to_bytes(float(e))
	raise Exception


def _dw(e, l, to_rebuild):
	e = "".join(e)
	if re.match(int_re, e):
		return ntb.int_to_bytes(to_int(e), 2)
	raise Exception


def _dd(e, l, to_rebuild):
	return get_const(e, l, to_rebuild, 0)


def get_norm_lable(lable, is_set=False):
	global last_lables
	lable = lable.split(".")
	fixed = False
	for i in range(len(lable)):
		if not lable[i] and len(last_lables) > i and not fixed:
			lable[i] = last_lables[i]
		elif fixed and (not lable[i] or is_set):
			raise Exception("Wrong name of label")
		elif is_set:
			last_lables = last_lables[:i]
			last_lables.append(lable[i])
			fixed = True
	return ".".join(lable)
