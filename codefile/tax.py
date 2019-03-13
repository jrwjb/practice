with open('C:\\Users\\jbwang\\Desktop\\otus_tax_assignments.txt') as f1:
    with open('C:\\Users\\jbwang\\Desktop\\tax.txt', 'w') as f2:
        # f2.write(f1.readline())
        for line in f1:
            id = line.split('\t')[0]
            tax = line.strip().split('\t')[1].split(';')
            if len(tax) == 7:
                f2.write(id + '\t' + '\t'.join(tax) + '\n')
            else:
                while len(tax) < 7:
                    tax.append('NA')
                newline = id + '\t' + '\t'.join(tax)
                f2.write(newline + '\n')
            if len(tax) > 7:
                print(line)