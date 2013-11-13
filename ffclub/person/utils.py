import re

name_break_pattern = re.compile("[\sA-Z]")


def blackout_name(name):
    nameSeq = list(name)
    if len(name) > 5:
        break_index = len(name)
        match = name_break_pattern.search(name, 1)
        if match is not None:
            break_index = match.start()
        nameSeq[break_index-1] = '*'
        nameSeq[break_index-2] = '*'
    elif len(name) > 1:
        black_index = 1
        while nameSeq[black_index] == ' ':
            black_index += 1
        nameSeq[black_index] = '*'
    return ''.join(nameSeq)


def blackout_email(email):
    emailSeq = list(email)
    if '@' in email:
        break_index = email.index('@')
    else:
        return email
    if break_index > 6:
        emailSeq[break_index - 2] = '*'
        emailSeq[break_index - 3] = '*'
        emailSeq[break_index - 4] = '*'
    elif break_index > 3:
        emailSeq[break_index - 1] = '*'
        emailSeq[break_index - 2] = '*'
    elif break_index > 1:
        emailSeq[break_index - 1] = '*'
    return ''.join(emailSeq)