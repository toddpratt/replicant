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
    if letter in self.guessed:
      return False
    self.guessed += letter[0].upper()
    return True


class WOFCommand(plugin_base.DatabaseCommand):

  def __init__(self):
    self.query = 'SELECT phrase FROM bosslike ORDER BY RANDOM() LIMIT 1'

  def handle(self, request):
    if request.channel in games:
      request.respond("A game is already in progress.")
    else:
      super(WOFCommand, self).handle(request)

  def report_success(self, result, request):
    puzzle = Puzzle(result[0][0])
    games[request.channel] = puzzle
    request.respond(puzzle.solution())
    write_scores(request)

  def report_error(self, failure, request):
    request.respond('error: %s' % failure.getErrorMessage())


class PuzzleCommand(plugin_base.BaseCommand):

  def handle_user(self, request):
    try:
      puzzle = games[request.channel]
    except KeyError:
      request.respond("There's no active game.")
    else:
      self.handle_player(request, puzzle)


class GiveMeACommand(PuzzleCommand):

  def handle_player(self, request, puzzle):
    letter = request.args[1][0].upper()
    if puzzle.guess(letter):
      request.respond(puzzle.solution())
    else:
      request.respond("Someone already guessed '%s'" % letter)


class SolveCommand(PuzzleCommand):

  def handle_player(self, request, puzzle):
    guess = request.args[1].upper()
    if puzzle.puzzle == guess:
      chan_scores = scores[request.channel]
      chan_scores[request.nick] += 1
      request.respond("You solved it!")
      del games[request.channel]
      write_scores(request)

    else:
      request.respond("Nope!")


def register():
  command.CommandHandler.register('wof', WOFCommand())
  command.CommandHandler.register('solve', SolveCommand())
  command.CommandHandler.register('g', GiveMeACommand())
  command.CommandHandler.register('gimmea', GiveMeACommand())
