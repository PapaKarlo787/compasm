import re
import argparse
import sys
import os
import nums_to_bytes as ntb
import args
from functions import *

commands = {"add": add, "sub": sub, "mul": mul, "div": div, "mov": mov,
			"and": and_, "or": or_, "xor": xor, "cmp": cmp_, "int": int_,
			"jmp": jmp, "loop": loop, "push": push, "pop": pop,
			"mod": mod, "fprint": print_, "delay": delay, "send": send,
			"gkey": gkey, "scur": setc, "binclude": binclude,
			"call": call, "ret": ret, "rnd": rnd, "print": print_int,
			"dd": dd, "movb": movb, "pow": pow_, "point": point,
			"circle": circle, "line": line, "rect": rect, "cls": cls,
			"bmp": bmp, "scond": scond, "lprint": lprint, "fmov": fmov,
			"fpush": fpush, "fpop": fpop, "shr": shr, "shl": shl,
			"fadd": fadd, "fsub": fsub, "fmul": fmul, "fdiv": fdiv,
			"fcmp": fcmp_, "fpow": fpow_, "play": play, "nplay": nplay,
			"db": db, "df": df, "icvtf": icvtf, "fcvti": fcvti, "dw": dw,
			"movw": movw, "pushai": pushai, "popai": popai, "popaf": popaf,
			"pushaf": pushaf, "rpix": rpix, "nop": nop, "mzer": mzer,
			"test": test, "ftest": ftest, "gtm": get_time, "stm": set_time,
			"mls": millis, "mcs": micros, "gmice": gmice, "gjoy": gjoy,
			"gir": gir, "btest": btest, "ldr": ldr, "str": str_, "mcp": mcp,
			"rb": rb, "rw": rw, "rd": rd, "lea": lea, "rcond": rcond,
			"krd": krd, "kwt": kwt, "rev": rev}


pattern = re.compile(r"\".*\"|\[|\]|\+|\*|-?[\w\.]+|,|:|;.*|-|\$")


def manage_line(data):
	global data_base, addr
	if data and data[-1][0] == ";":
		data.pop()
	if not data:
		return
	if data[0] in commands:
		data_base += commands[data[0]](data[1:], len(data_base))
	elif len(data) == 2 and data[1] == ":":
		data[0] = args.get_norm_lable(data[0], True)
		if data[0] in lables:
			raise Exception("Label '{}' already presents".format(data[0]))
		lables[data[0]] = len(data_base)
	elif re.match("jn?(e?g?l?i?a?b?z?I?)*$", data[0]):
		data_base += jc(data[1:], data[0][1:], len(data_base))
	elif len(data) == 2 and data[0] == "include" and "\"\"" == data[1][0]+data[1][-1]:
		nl = args.nl
		try:
			start(data[1][1:-1])
			args.nl = nl+1
		except Exception as e:
			args.nl = nl
			raise e
	elif data[0] == "times":
		data_base += times(data[1:], len(data_base), commands)
	else:
		raise Exception


def start(fn, visited=[]):
	args.nl = 1
	fn = os.path.abspath(fn)
	if fn in visited:
		raise Exception("file {} already included".format(fn))
	visited.append(fn)
	with open(fn) as f:
		for l in f:
			try:
				manage_line(pattern.findall(l))
				args.nl += 1
			except Exception as e:
				msg = str(e) if str(e) else "Wrong line"
				raise Exception("{}: {} (line {})".format(fn, msg, args.nl))


def add_lables(org):
	global nl, data_base
	for d in to_rebuild:
		if d[-1] == -1:
			set_value(d[0], d[1])
			continue
		if d[0][d[-1]][0] == "$":
			d[0][d[-1]] = str(int(d[0][d[-1]][1:]) + org)
		else:
			if d[0][d[-1]] not in lables:
				raise Exception("No such lable - {} (line {})".format(d[0][d[-1]], d[2]))
			d[0][d[-1]] = str(lables[d[0][d[-1]]] + org)
			d[-1] = -1


def set_value(val, n):
	global data_base
	val = ntb.int_to_bytes(eval("".join(val)))
	data_base = data_base[:n] + val + data_base[n+4:]


def save(fn):
	with open(fn, 'wb') as f:
		f.write(data_base)
		f.flush()


if __name__ == "__main__":
	try:
		parser = argparse.ArgumentParser(description='OzComp Compiler')
		parser.add_argument("inf", help="input file")
		parser.add_argument("outf", help="output file")
		parser.add_argument("org", type=int, default=0x40000000,
							help="open file", nargs='?')
		cmd = parser.parse_args()
		start(cmd.inf)
		add_lables(cmd.org)
		save(cmd.outf)
	except Exception as e:
		print(e)
		sys.exit(1)
