from matplotlib import pyplot as plt
from matplotlib_venn import venn3, venn3_circles, venn2, venn2_circles

def vs(qi, nh):
    with open(qi) as f_qi:
        with open(nh) as f_nh:

            def my_func(file):
                my_dict = {}
                for i in file:
                    line = i.strip()
                    # name = ''
                    if line.startswith('>'):
                        name = line
                        my_dict[name] = ''
                        continue
                    my_dict[name] += line
                my_set = set()
                for k, y in my_dict.items():
                    my_set.add(y.upper())
                return my_set, my_dict

            f_qi_set = my_func(f_qi)[0]
            f_nh_set, f_nh_dic = my_func(f_nh)

            name_list = ['qiime1', 'NuoHe']
            num_list = []
            num_list.append(len(f_qi_set))
            num_list.append(len(f_nh_set))
            for a, b in zip(name_list, num_list):
                plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
            plt.bar(name_list, num_list, width=0.5, color='rgb')
            plt.ylim(0, 300000)
            plt.title('OTU Counts')
            plt.show()

            v = venn2(subsets=(len(f_nh_set) - len(f_nh_set & f_qi_set), len(f_qi_set) - len(f_nh_set & f_qi_set), len(f_nh_set & f_qi_set)), set_labels=('NuoHe', 'qiime1'))
            plt.show()
            return

if __name__ == '__main__':
    qi = 'C:\\Users\\jbwang\\Desktop\\otus.fa'
    nh = 'C:\\Users\\jbwang\\Desktop\\OTUs.fasta'

    print(vs(qi, nh))