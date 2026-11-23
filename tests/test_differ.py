from ruleradar.differ import raw_changes


def test_detects_deadline_change():
    old = "Last date: 15 December\nIncome below 2.5 lakh"
    new = "Last date: 5 December\nIncome below 2.5 lakh"
    lines = raw_changes(old, new)
    assert "-Last date: 15 December" in lines
    assert "+Last date: 5 December" in lines


def test_raw_changes_detects_modified_line():
    old = "Deadline: 30 Nov\nFee: Rs 200"
    new = "Deadline: 10 Dec\nFee: Rs 200"
    diff = raw_changes(old, new)
    assert "-Deadline: 30 Nov" in diff
    assert "+Deadline: 10 Dec" in diff
    assert not any("Fee: Rs 200" in line for line in diff)


def test_raw_changes_empty_when_identical():
    text = "Deadline: 30 Nov"
    assert raw_changes(text, text) == []
