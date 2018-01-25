from evelink.api import APIResult


class TestAPIResult(APIResult):
    def __new__(cls, access_mask, expire_ts, keypair_type):
        result = {
            'access_mask':  access_mask,
            'expire_ts':    expire_ts,
            'type':         keypair_type
        }
        return super(TestAPIResult, cls).__new__(cls, result, None, None)


TEST_RESULTS = {
    'full': {
        'all': TestAPIResult(4294967295, None, 'account'),
        'char_corp': TestAPIResult(4294967295, None, 'char'),
        'char_noncorp': TestAPIResult(4294967295, None, 'char')
    },
    'partial': {
        'all': TestAPIResult(4294901631, None, 'account'),
        'char_corp': TestAPIResult(4294901631, None, 'char'),
        'char_noncorp': TestAPIResult(4294901631, None, 'char')
    },
    'blank': {
        'all': TestAPIResult(0, None, 'account'),
        'char_corp': TestAPIResult(0, None, 'char'),
        'char_noncorp': TestAPIResult(0, None, 'char')
    },
    'full_expires': {
        'all': TestAPIResult(4294967295, 0, 'account'),
        'char_corp': TestAPIResult(4294967295, None, 'char'),
        'char_noncorp': TestAPIResult(4294967295, None, 'char')
    }
}
