import collections
import random

from twisted.internet import reactor

import plugin_base
import command


class Player(object):

  def __init__(self, account, nick, hp):
    users[nick] = self
    self.account = account
    self.nick = nick
    self.hp = hp
    self.last_enemy = None

  def strike(self, strikee, request):
    if self.hp < 1:
      return
    points = random.randint(0, 50)
    hit = strikee.take_damage(points, self, request)
    strikee.last_enemy = self

    if hit == 0:
      request.respond('you missed')
    elif strikee.hp < 1:
      self.hp += random.randint(25, 50)
      request.respond('you killed %s, your hitpoints have increased to %d' %
          (strikee.nick, self.hp))
      del users[strikee.nick]
    elif strikee.hp < 10:
      request.respond('you critically injured %s' % strikee.nick)
    else:
      request.respond('you struck %s for %d hit points' %
          (strikee.nick, hit))

  def take_damage(self, points, striker, request):
    if self.hp < 1:
      return 0
    self.hp -= points
    return points


class God(Player):

  def take_damage(self, points, striker, request):
    return 0

  def strike(self, strikee, request):
    if len(request.args) == 3 and request.args[2] == 'gently':
      hp = strikee.hp / 10
    else:
      hp = strikee.hp
    damage = strikee.take_damage(hp, self, request)
    if strikee.hp < 1:
      del users[strikee.nick]
      request.respond('you smote %s' % strikee.nick)


class NPC(Player):

  def take_damage(self, points, striker, request):
    new_request = request.for_reply('%s!NPC@NPC' % self.nick)
    for i in range(1, random.randint(3, 7)):
      reactor.callLater(i, self.strike, striker, new_request)
    return super(NPC, self).take_damage(points, striker, request)



class StatCommand(plugin_base.BaseCommand):

  def handle_user(self, request):
    request.respond(', '.join('%s: %d' % (p.nick, p.hp)
                    for p in users.itervalues()))


class PlayCommand(plugin_base.BaseCommand):

  def handle_admin(self, request):
    if len(request.args) == 4:
      player = Player(request.args[1], request.args[2], int(request.args[3]))
    else:
      self.handle_user(request)

  def handle_user(self, request):
    if request.nick in users:
      request.respond('you are already playing.')
    else:
      hp = random.randint(100, 200)
      player = Player(request.account, request.nick, hp)
      request.respond('your hp: %d' % player.hp)


class BaseHpCommand(plugin_base.BaseCommand):

  def get_player(self, request):
    try:
      player = users[request.nick]
    except KeyError:
      request.respond('you are not playing')
      return False

    if player.account != request.account:
      request.respond('you are not the real %s' % player.nick)
      return False

    return player

  def check_args(self, request, arg_count, usage='usage: {0} <nickname>'):
    if len(request.args) != arg_count:
      request.respond(usage.format(*request.args))
      return False

  def get_target(self, request):
    target_nick = request.args[1]

    try:
      target = users[target_nick]
    except KeyError:
      request.respond('%s: no such player' % target_nick)
      return False

    return target


class HealCommand(BaseHpCommand):

  def handle_user(self, request):
    target = self.get_target(request)
    if result:
      target.hp += random.randint(25, 75)


class StrikeCommand(BaseHpCommand):

  def handle_user(self, request):
    player = self.get_player(request)
    target = self.get_target(request)
    if player and target:
      player.strike(target, request)


class SummonCommand(BaseHpCommand):

  def handle_user(self, request):
    player = self.get_player(request)
    if player:
      for i in xrange(1, random.randint(2, 8)):
        npc = NPC('NPC', 'demon %d' % i, 20)
        new_request = request.for_reply('%s!NPC@NPC' % npc.nick)
        for j in xrange(1, random.randint(2, 4)):
          reactor.callLater(random.randint(1, 4), npc.strike,
                            player.last_enemy, new_request)


users = {}

God('devonian.users.undernet.org', 'devonian', 1)
God('sucralose.users.undernet.org', 'sucralose', 300)
NPC('NPC', 'gnome', 300)
NPC('NPC', 'elf', 300)
NPC('NPC', 'wizard', 300)
NPC('NPC', 'gopher', 300)


def register():
  command.CommandHandler.register('stat', StatCommand())
  command.CommandHandler.register('play', PlayCommand())
  command.CommandHandler.register('strike', StrikeCommand())
  command.CommandHandler.register('heal', HealCommand())
  command.CommandHandler.register('summon', SummonCommand())
