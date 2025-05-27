def is_candidate(request):
    """
    True if this request was authenticated via the 'candidates' DB.
    Your SplitLoginBackend already sets user._state.db.
    """
    return getattr(request.user._state, "db", "") == "candidates"
