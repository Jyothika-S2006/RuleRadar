from ruleradar.differ import raw_changes

def test_detects_deadline_change():
    old = "Last date: 15 December\nIncome below 2.5 lakh"
    new = "Last date: 5 December\nIncome below 2.5 lakh"
    lines = raw_changes(old, new)
    assert "-Last date: 15 December" in lines
    assert "+Last date: 5 December" in lines
