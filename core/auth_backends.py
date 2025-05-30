from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class SplitLoginBackend(ModelBackend):
    """
    Authenticate against the DB specified by POST['role'] (candidates | companies).
    Falls back to 'default' so superusers can still log in.
    """
    def authenticate(self, request, username=None, password=None, role=None, **kwargs):
        db_order = [role] if role in {"candidates", "companies"} else []
        #db_order.append("default")                      # always last

        for db in db_order:
            try:
                user = User.objects.using(db).get(email__iexact=username)
            except User.DoesNotExist:
                continue
            if user.check_password(password):
                user._state.db = db                    # remember where it came from
                return user
