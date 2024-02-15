from tools.utility import remove_newline

def convert_tocsv(file):
    f = open(file,'r')
    lines = f.readlines()
    data = []
    for row in lines:
        line = row.split('\t')
        line[-1] = remove_newline(line[-1])
        data.append(line)
    f = open(file,'w')
    for line in data:
        for i in range(len(line)):
            f.write(line[i])
            if i != len(line)-1:
                f.write(',')
        f.write('\n')

convert_tocsv(file='nextgenstats/data/GunGameS24.csv')