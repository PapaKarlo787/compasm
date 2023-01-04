import nums_to_bytes as ntb
import args
import re
import copy


lables = {}
to_rebuild = []
data_base = b''


def ariphmetics(data, l, k1, k2, f=False):
	try:
		return bytes([k1]) + args.rr(data)
	except Exception:
		return bytes([k2]) + args.rc(data, l, to_rebuild, f)


def add(data, l):
	return ariphmetics(data, l, 0, 1)


def fadd(data, l):
	return ariphmetics(data, l, 67, 68, True)


def sub(data, l):
	return ariphmetics(data, l, 2, 3)


def fsub(data, l):
	return ariphmetics(data, l, 69, 70, True)


def mul(data, l):
	return ariphmetics(data, l, 4, 5)


def fmul(data, l):
	return ariphmetics(data, l, 71, 72, True)


def div(data, l):
	return ariphmetics(data, l, 6, 7)


def fdiv(data, l):
	return ariphmetics(data, l, 73, 74, True)


def pow_(data, l):
	return ariphmetics(data, l, 48, 49)


def fpow_(data, l):
	return ariphmetics(data, l, 75, 76, True)


def and_(data, l):
	return ariphmetics(data, l, 14, 15)


def btest(data, l):
	return ariphmetics(data, l, 124, 125)


def or_(data, l):
	return ariphmetics(data, l, 16, 17)


def xor(data, l):
	return ariphmetics(data, l, 18, 19)


def shr(data, l, k1=79, k2=80):
	try:
		return bytes([k1]) + args.rr(data)
	except Exception:
		return bytes([k2]) + args.rcb(data)


def shl(data, l):
	return shr(data, l, 81, 82)


def cmp_(data, l):
	return ariphmetics(data, l, 20, 21)


def fcmp_(data, l):
	return ariphmetics(data, l, 77, 78, True)


def mod(data, l):
	return ariphmetics(data, l, 27, 28)


def jmp(data, l, k1=22, k2=95):
	try:
		return bytes([k2]) + args.r(data)
	except Exception:
		return args.jump(k1, data, l, to_rebuild)


def loop(data, l):
	return jmp(data, l, 24, 97)


def call(data, l):
	return jmp(data, l, 40, 98)


def play(data, l):
	return args.jump(91, data, l, to_rebuild)


def nplay(data, l):
	return bytes([92])


def ret(data, l):
	return bytes([41])


def rnd(data, l):
	return bytes([42])


def pushai(data, l):
	return bytes([105])


def popai(data, l):
	return bytes([106])


def pushaf(data, l):
	return bytes([107])


def popaf(data, l):
	return bytes([108]) 


def gkey(data, l):
	return bytes([36])


def gmice(data, l):
	return bytes([121])


def gjoy(data, l):
	return bytes([122])


def gir(data, l):
	return bytes([123])


def cls(data, l):
	return bytes([58])


def millis(data, l):
	return bytes([117])


def micros(data, l):
	return bytes([118])


def rev(data, l):
	return bytes([39])


def nop(data, l):
	return bytes([255])


def mcp(data, l):
	return bytes([128]) + args.rr(data)


def push(data, l, k1=25, k2=104):
	try:
		return bytes([k1]) + args.r(data)
	except Exception:
		return bytes([k2]) + args.get_const(data, l+1, to_rebuild, 0)


def pop(data, l):
	return push(data, l, 26)


def fpush(data, l):
	return push(data, l, 89)


def fpop(data, l):
	return push(data, l, 90)


def print_int(data, l):
	return print_(data, l, 43)


def scond(data, l):
	return bytes([66]) + args.c(data)


def rcond(data, l):
	return bytes([13]) + args.c(data)


def krd(data, l):
	return bytes([87]) + args.r(data)


def kwt(data, l):
	return bytes([88]) + args.r(data)


def get_time(data, l):
	return bytes([116]) + args.r(data)


def set_time(data, l):
	return bytes([115]) + args.r(data)


def point(data, l):
	return setc(data, l, (50, 51))


def ldr(data, l):
	if len(data) == 3 and data[1] == ",":
		res = args.r(data[:1])[0] + (args.sr(data[2:]) << 4)
		return bytes([126, res])
	raise Exception


def str_(data, l):
	if len(data) == 3 and data[1] == ",":
		res = args.sr(data[:1]) + (args.r(data[2:])[0] << 4)
		return bytes([126, res])
	raise Exception


def mov(data, l, n=4, k1=8, k2=9, k3=10, k4=11, to_addr=True):
	if data[2]+data[-1] != "[]" and data[0]+data[-3] != "[]":
		return ariphmetics(data, l, k3, k4, k1 != 8)
	if args.is_reg(data[-1]) and data[-2] == ",":
		result = args.get_ea(data[:-2], l, to_rebuild, n, k2)
		result[1] += int(data[-1][1:])
		return bytes(result)
	return lea(data, l, k1, n)


def icvtf(data, l):
	return bytes([93]) + args.rr(data)


def fcvti(data, l):
	return bytes([94]) + args.rr(data)


def mzer(data, l):
	try:
		return bytes([111]) + args.rc(data, l, to_rebuild, False)
	except Exception:
		data = dd(data, l)
		if len(data) == 8:
			return bytes([112]) + data
	raise Exception


def fmov(data, l):
	return mov(data, l, 4, 83, 84, 85, 86)


def movw(data, l):
	return mov(data, l, 2)


def movb(data, l):
	return mov(data, l, 1)


def lea(data, l, k=12, n=4):
	if args.is_reg(data[0]) and data[1] == ",":
		result = args.get_ea(data[2:], l, to_rebuild, n, k)
		result[1] += int(data[0][1:])
		return bytes(result)
	else:
		raise Exception


def jc(data, cond, l):
	bit = 0 if 'n' in cond[0] else 1
	byte = 0
	for i in "Iabzigle":
		byte *= 2
		byte += bit if i in cond else (bit + 1) % 2
	result = list(jmp(data, l + 1, 23, 96))
	result.insert(1, byte)
	return bytes(result)


def print_(data, l, n=29):
	return bytes([n]) + args.r(data)


def lprint(data, l):
	return jmp(data, l, 30, 103)


def delay(data, l, k1=31, k2=32):
	try:
		return bytes([k1]) + args.r(data)
	except Exception:
		if len(data) == 1 and int(data[0]) >= 0:
			return bytes([k2]) + ntb.int_to_bytes(int(data[0]))


def send(data, l):
	return delay(data, l, 33, 34)


def circle(data, l):
	if len(data) == 5 and data[1] == ',':
		if args.is_reg(data[0]):
			return bytes([52]) + args.r(data[:1]) + args.rr(data[2:])
		else:
			res = args.c(data[:1])
			try:
				return bytes([54]) + res + args.rr(data[2:])
			except Exception:
				return bytes([53]) + res + args.cc(data[2:])


def line(data, l, k=(55,56,57)):
	if len(data) == 7 and data[3] == ",":
		res1 = setc(data[:3], l, k[:2])
		res2 = setc(data[-3:], l, k[:2])
		if res1[0] < res2[0]:
			res2 = bytes([k[2]]) + res2[1:]
		return res2+res1[1:]
	raise Exception


def rect(data, l):
	return line(data, l, (59, 60, 61))


def bmp(data, l):
	for f in [(args.rcb, 62), (args.cbr, 63), (args.rr, 64), (args.cc, 65)]:
		try:
			res = bytes([f[1]]) + f[0](data[:3])
			break
		except Exception:
			pass
	else:
		raise Exception
	return res + args.jump(0, data[-1:], l+len(res)-1, to_rebuild)[1:]


def int_(data, l):
	return bytes([35]) + args.r(data)


def setc(data, l, k=(37, 38)):
	try:
		return bytes([k[0]]) + args.rr(data)
	except Exception:
		return bytes([k[1]]) + args.cc(data)


def binclude(data, l):
	with open(data[0][1:-1], "rb") as f:
		return f.read()


def dd(data, l, f=args._dd):
	res = b''
	d = []
	for x in data:
		if x == ",":
			if not d:
				raise Exception("Missed operand")
			res += f(d, l+len(res), to_rebuild)
			d = []
		else:
			d.append(x)
			continue
	res += f(d, l+len(res), to_rebuild)
	return res
	
def db(data, l):
	return dd(data, l, args._db)


def dw(data, l):
	return dd(data, l, args._dw)


def df(data, l):
	return dd(data, l, args._df)


def rb(data, l, k=1):
	if len(data) != 1 or not re.match(int_re, data[0]):
		raise Exception("Wrong operand")
	return b'\x00' * k * args.to_int(data[0])


def rw(data, l):
	return rb(data, l, 2)


def rd(data, l):
	return rb(data, l, 4)


def times(data, l, cmd):
	global to_rebuild
	len_rebuilds = len(to_rebuild)
	data_ = cmd[data[0]](data[1:-1], l)
	if re.match(args.int_re, data[-1]):
		n = args.to_int(data[-1])
		rebuilds = to_rebuild[len_rebuilds:]
		for i in range(1, n):
			rebuilds = copy.deepcopy(rebuilds)
			for r in rebuilds:
				r[1] += len(data_)
			to_rebuild += rebuilds
		return data_ * n
	raise Exception


def rpix(data, l):
	try:
		return bytes([110]) + args.rcb(data)
	except Exception:
		return bytes([109]) + args.rr(data)


def test(data, l):
	return bytes([113]) + args.r(data)


def ftest(data, l):
	return bytes([114]) + args.r(data)
