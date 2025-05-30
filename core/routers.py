class ReadOnlyRouter:
    """Let writes follow Django’s default DB; we only care about reads for login."""
    def db_for_read(self, model, **hints):   return None
    def db_for_write(self, model, **hints):  return None
    def allow_migrate(self, db, app_label, **hints): return True