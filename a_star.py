import argparse
import math
import random

class State:
  moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  def __init__(self, st, g, parent, N):
    global base, H
    self.g = g
    self.parent = parent
    self.N = N
    if H == 1:
        h = State.calc_bad_p(st, base.copy(), N)
    else:
        h = State.calch(st, base.copy(), N)
    self.f = self.g + h
    self.repr_num = State.factoriadic_to_nth(base.copy(), State.str_to_factoriadic(base.copy(), st))
    self.possible_moves = State.get_possible_moves(st, N)
  
  def __repr__(self):
    return f"State {str(self.repr_num)}"

  def __eq__(self, other):
    if not isinstance(other, State):
      return False
    return self.repr_num == other.repr_num

  def __lt__(self, other):
    if self.f == other.f:
      return self.g > other.g
    return self.f < other.f

  def __le__(self, other):
    return self.f <= other.f

  def __gt__(self, other):
    if self.f == other.f:
      return self.g < other.g
    return self.f > other.f

  def __ge__(self, other):
    return self.f >= other.f

  def __hash__(self):
    return hash(self.repr_num)

  def __str__(self):
    return f"State {str(self.repr_num)}"

  def get_full_form(self):
    return State.factoriadic_to_str(base, State.nth_to_factoriadic(self.repr_num))

  @staticmethod
  def get_possible_moves(st, N):
    possible_moves = []
    idx = st.index(0)
    i = idx // N
    j = idx % N
    for move in State.moves:
      if i + move[0] >= 0 and i + move[0] < N \
        and j + move[1] >= 0 and j + move[1] < N:
        possible_moves.append(move)
    return possible_moves

  @staticmethod
  def calch(rep, base, N):
    h = 0
    for idx, char in enumerate(rep):
      idx_orig = base.index(char)
      i_orig = idx_orig // N
      j_orig = idx_orig % N
      i = idx // N
      j = idx % N

      manhattan_dist = abs(i_orig - i) + abs(j_orig - j)
      h += manhattan_dist
    return h

  @staticmethod
  def calc_bad_p(rep, base, N):
    h = 0
    for idx, char in enumerate(rep):
      idx_orig = base.index(char)
      i_orig = idx_orig // N
      j_orig = idx_orig % N
      i = idx // N
      j = idx % N

      if i_orig * 3 + j_orig != i * 3 + j:
          h +=1
    return h

  @staticmethod
  def str_to_factoriadic(base, state):
    num = 0
    base_ = base.copy()
    for number in state:
      idx = base_.index(number)
      num = num * 10 + idx
      base_ = base_[:idx] + base_[idx+1:]
    return num

  @staticmethod
  def factoriadic_to_nth(base, fact):
    fact_str = str(fact)
    base_len = len(base)
    while len(fact_str) != base_len:
      fact_str = "0" + fact_str
  
    num = 0
    fact_str = reversed(fact_str)
    for idx, char in enumerate(fact_str):
      num += int(char) * factorials[idx]
    return num

  @staticmethod
  def factoriadic_to_str(base, fact):
    fact_str = str(fact)
    while len(fact_str) < len(base):
      fact_str = "0" + fact_str
    result = []
    base_ = base.copy()
    for idx, char in enumerate(fact_str):
      result.append(base_[int(char)])
      base_.remove(base_[int(char)])

    return result

  @staticmethod
  def nth_to_factoriadic(n):
    if n == 0:
      return 0
    remainders = []
    i = 1
    while n != 0:
      remainders.append(str(n % i))
      n = n//i
      i += 1
    remainders.reverse()
    return int("".join(remainders))

class MyPriorityList():
  def __init__(self):
    self.content = []

  def __repr__(self):
    return str(self.content)

  def __len__(self):
    return len(self.content)

  def contains(self, item):
    if item in self.content:
      return self.content[self.content.index(item)]
    else:
      return -1

  def get_first(self):
    item = self.content[0]
    self.content = self.content[1:]
    return item
  
  def append(self, item):
    if len(self.content) == 0:
      self.content.append(item)
    elif len(self.content) == 1:
      if self.content[0] > item:
        self.content = [item] + self.content
      else:
        self.content.append(item)
    else:
      if self.content[0] > item:
        self.content = [item] + self.content
      elif self.content[-1] <= item:
        self.content.append(item)
      else:
        for i in range(len(self.content) - 1):
          if self.content[i] <= item and self.content[i + 1] > item:
            self.content = self.content[:i] + [item] + self.content[i:]
            break

  def remove(self, item):
    self.content.remove(item)

def solution(last_node, N):
  node = last_node
  if node.parent:
    solution(node.parent, N)
  print_beautify(node.get_full_form(), N)  

def print_beautify(state, N):
    for i in range(N):
        for j in range(N):
            print(state[i * N + j], end=" ")
        print()
    print()

def modify_node(state, move):
  state_copy = state.copy()
  null_pos = state_copy.index(0)
  next_pos = null_pos + move[0] * 3 + move[1]
  tmp = state_copy[next_pos]
  state_copy[next_pos] = 0
  state_copy[null_pos] = tmp
  return state_copy

def a_star_solver(start, goal):
  global args
  open_, close_ = MyPriorityList(), []
  open_.append(State(start, 0, None, 3))
  num_steps = 0

  while len(open_) != 0:
    N = open_.get_first()
    num_steps += 1
    close_.append(N)
    state_N = N.get_full_form()
    if state_N == goal:
      if args.solseq:
        solution(N, 3)
      if args.pcost:
          print(N.g)
      if args.nvisited:
          print(num_steps)
      break
    
    for move in N.possible_moves:
      new_state = modify_node(state_N, move)
      N_new = State(new_state, N.g + 1, N, 3)
      if N_new.g > 31:
          continue
      if N.parent == N_new:
        continue
      X = open_.contains(N_new)
      if X != -1 and X <= N_new:
        continue
      elif X!= -1:
        open_.remove(X)
      if N_new in close_:
        X = close_[close_.index(N_new)]
        if X <= N_new:
          continue
        else:
          close_.remove(X)
      open_.append(N_new)

def generate_random_state(N, M):
    global base
    start = [x for x in range(1, N)] + [0]
    base = start
    curr_state = State(start, 0, None, int(N ** 0.5))
    prev_states = [curr_state]
    while M:
        move = random.sample(curr_state.possible_moves, 1)
        new_state = modify_node(curr_state.get_full_form(), move[0])
        curr_state = State(new_state, 0, curr_state, int(N ** 0.5))
        if curr_state in prev_states:
            continue
        else:
            M -=1
            prev_states.append(curr_state)
    print_beautify(curr_state.get_full_form(), int(N ** 0.5))

base = [1, 2, 3, 4, 5, 6, 7, 8, 0]
factorials = [math.factorial(x) for x in range(16)]

parser = argparse.ArgumentParser("Solve N puzzle", add_help=False)
parser.add_argument("-input", type=str)
parser.add_argument("-solseq", action='store_true')
parser.add_argument("-pcost", action='store_true')
parser.add_argument("-nvisited", action='store_true')
parser.add_argument("-h", type=int)
parser.add_argument("-rand", nargs=2, type=int)

args = parser.parse_args()

start = []
puzzle_size = 0
H = 2

if args.input:
    with open(args.input, "rt") as rt:
        lines = rt.readlines()
    for line in lines:
        line = line.split()
        start += [int(x) for x in line]

elif args.rand:
    puzzle_size = args.rand[0]
    rand_steps = args.rand[0]
else:
    for i in range(9):
        start.append(int(input("{}. number: ".format(int(i+1)))))

if args.h:
    H = args.h

if args.rand:
    factorials = [math.factorial(x) for x in range(args.rand[0])]
    generate_random_state(*args.rand)
else:
    a_star_solver(start, base.copy())