import argparse
from typing import List, Callable
import sys
import re
# https://www.dungeonsolvers.com/2018/03/29/average-dice-roll/
# ( ( Max Die Roll + 1 ) / 2 ) * Number of Same-Sided Dice

ADD: Callable[[float, float], float] = lambda a, b : a + b
SUB: Callable[[float, float], float] = lambda a, b : a - b
TOKEN_RE: re.Pattern = re.compile('^\d+d\d+$')

class DiceException(Exception):
	pass

class IlligalOperation(DiceException):
	pass

class DanglingOperator(DiceException):
	pass

class IlligalSequence(DiceException):
	pass

def avg_dice(num_dice: float, num_sides: float) -> float:
	return ( ( num_sides + 1 ) / 2 ) * num_dice

def get_avg(dice_str: str) -> float:
	num_dice: float = float(dice_str.split('d')[0])
	num_sides: float = float(dice_str.split('d')[1])
	return avg_dice(num_dice, num_sides)

def do_op(op: Callable[[float, float], float], new_val:float, final: float) -> float:
	return op(new_val, final)

def is_op(c: str) -> bool:
	return c in ('+', '-')

def handle_op(c: str, current_token: str, final: float) -> float:
	global ADD, SUB
	new_val: float 
	if not current_token.isnumeric():
		new_val = get_avg(current_token)
	else:
		new_val = float(current_token)
	if c == '+':
		return do_op(ADD, new_val, final)
	elif c == '-':
		return do_op(SUB, new_val, final)
	else:
		raise IlligalOperation(f"operation '{c}' is not supported.")

def main(eq_og: str) -> None:
	global TOKEN_RE
	eq = eq_og.replace(' ','')
	current_token: str = eq[0]
	final: float = 0
	index: int = 1
	last_op: str = ''
	try:
		if is_op(current_token):
			print("cannot start with an operator.")
			sys.exit(0)
		if '+' not in eq and '-' not in eq:
			if TOKEN_RE.match(eq):
				final = get_avg(eq)
			else:
				raise IlligalSequence(f"Illigal sequence 1 {eq}")
		for c in eq[1:]:
			if is_op(c):
				if not TOKEN_RE.match(current_token):
					raise IlligalSequence(f"illigal sequence {current_token}{c}")
				if index + 1 >= len(eq):
					raise DanglingOperator(f"dangling operator '{c}'")
				final = handle_op(c, current_token, final)
				current_token = ''
				last_op = c
			elif not is_op(c) and (c.isnumeric() or c == 'd'):
				current_token = f"{current_token}{c}"
			else:
				print(f"Bad token '{c}'")
				sys.exit(0)
			index += 1
		if last_op != '':
			final = handle_op(last_op, current_token, final)
		print(f"Average roll for '{eq_og}' is {final}")
	except DiceException as e:
		print(e)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='dice average')
	parser.add_argument('eq', help='dice equation is a combinatiopn of (+,-) and <number>d<sides>', type=str)
	args = parser.parse_args()
	main(args.eq)

