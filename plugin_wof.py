import collections
import random

from twisted.internet import reactor

import command
import plugin_base

games = {}
scores = collections.defaultdict(lambda: collections.defaultdict(int))


def write_scores(request):
  chan_scores = scores[request.channel]
  if len(chan_scores):
    request.respond(', '.join(("%s=%d" % (k, v))
        for k, v in chan_scores.iteritems()))


class Puzzle(object):

  def __init__(self, puzzle):
    self.puzzle = puzzle.upper()
    self.guessed = ""

  def solution(self):
    solution = ''
    for c in self.puzzle:
      if c.isspace() or c in self.guessed:
        solution += c
      else:
        solution += '*'
    return solution

  def guess(self, letter):
    self.guessed += letter[0].upper()


class WOFCommand(plugin_base.DatabaseCommand):

  def __init__(self):
    self.query = 'SELECT phrase FROM bosslike ORDER BY RANDOM() LIMIT 1'

  def report_success(self, result, request):
    puzzle = Puzzle(result[0][0])
    games[request.channel] = puzzle
    request.respond(puzzle.solution())
    write_scores(request)

  def report_error(self, failure, request):
    request.respond('error: %s' % failure.getErrorMessage())

class GiveMeACommand(plugin_base.BaseCommand):

  def handle_user(self, request):
    puzzle = games[request.channel]
    puzzle.guess(request.args[1][0].upper())
    request.respond(puzzle.solution())


class SolveCommand(plugin_base.BaseCommand):

  def handle_user(self, request):
    puzzle = games[request.channel]
    guess = request.args[1].upper()
    if puzzle.puzzle == guess:
      chan_scores = scores[request.channel]
      chan_scores[request.nick] += 1
      request.respond("You solved it!")
      write_scores(request)

    else:
      request.respond("Nope!")


def register():
  command.CommandHandler.register('wof', WOFCommand())
  command.CommandHandler.register('solve', SolveCommand())
  command.CommandHandler.register('g', GiveMeACommand())
  command.CommandHandler.register('gimmea', GiveMeACommand())
