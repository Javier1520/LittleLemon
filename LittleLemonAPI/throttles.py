from rest_framework.throttling import UserRateThrottle

class FifteenCallsPerMinute(UserRateThrottle):
    scope = 'fifteen'