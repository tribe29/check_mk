# yapf: disable
checkname = 'alcatel_power'

info = [[u'1', u'1', u'0x35000001', u'0'], [u'2', u'1', u'0x35000001', u'1'],
        [u'3', u'1', u'0x35000001', u''], [u'4', u'1', u'0x35000002', u'0'],
        [u'5', u'1', u'0x35000002', u'1'], [u'6', u'1', u'0x35000002', u''],
        [u'7', u'2', u'0x35000001', u'0'], [u'8', u'2', u'0x35000001', u'1'],
        [u'9', u'2', u'0x35000001', u''], [u'10', u'2', u'0x35000002', u'0'],
        [u'11', u'2', u'0x35000002', u'1'], [u'12', u'2', u'0x35000002', u'']]

discovery = {
    '': [
        (u'2', {}),
        (u'3', {}),
        (u'5', {}),
        (u'8', {}),
        (u'9', {}),
        (u'11', {}),
    ],
}

checks = {
    '': [(u'1', {}, []), (u'2', {}, [(0, 'Supply status OK', [])]),
         (u'3', {}, [(0, 'Supply status OK', [])]), (u'5', {}, [(0, 'Supply status OK', [])]),
         (u'8', {}, [(2, 'Supply in error condition (2)', [])]),
         (u'11', {}, [(2, 'Supply in error condition (2)', [])]),
         (u'9', {}, [(2, 'Supply in error condition (2)', [])])]
}
