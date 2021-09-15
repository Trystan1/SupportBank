def readFile():
    with open('sample.txt') as f:
        lines = f.readlines()

        Emails = countEmails(lines)
        print(f'{Emails}')
        f.close()

def countEmails(lines)->int:
    Emails = 0
    print(f'{len(lines)}')
    for i in range(0,lines.length):
        if (lines.substring(i, 13) == '@softwire.com'):
            Emails += 1

    return Emails

readFile