def fix_case(f):
    def test(case):
        f(case=case)
    return test

