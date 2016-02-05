class UserDB(object):

  def __init__(self, db):
    self.db = db
    self.ready = False
    self.load_from_table()
    self.temporary_users = set()

  def append(self, account):
    self.temporary_users.add(account)

  def add(self, account):
    self.users.add(account)
    d.self.db.runQuery(
        'INSERT OR REPLACE INTO admins (account) VALUES (?)', account)

  def load_from_table(self):
    d = self.db.runQuery('SELECT account FROM admins')
    d.addCallback(self.gotAdminAccounts)
    d.addErrback(self.gotError)

  def gotError(self, *args):
    print args

  def gotAdminAccounts(self, results):
    self.users = set(row[0] for row in results)
    self.ready = True

  def __contains__(self, item):
    if item in self.temporary_users:
      return True
    if self.ready:
      return item in self.users
    else:
      raise ValueError('admin users list hasn\'t loaded yet.')
