import easygui

def gui_input():
    easygui.msgbox('  This is a (List-based Evolutionary Algorithm) program built by Yingkai Liu'
                   '\n                                enjoy!                                      '
                   '\n'
                   '\n                  should you find any problems, contact                     '
                   '\n                      water@mail.nankai.edu.cn                              ',
                   'List-based Evolutionary Algorithm')

    number_of_gene_input = easygui.enterbox(
        msg='           Here you need to specify number of chromosome sites first.',
        title='-number_of_gene',
        default='5')

    number_of_gene = int(number_of_gene_input)
    gene_set_field_name = []
    for i in range(number_of_gene):
        gene_set_field_name.append("*****************" + str(i) + "th gene's high")
        gene_set_field_name.append("low")
        gene_set_field_name.append("number of interval")

    gene_set_input = easygui.multenterbox(
        msg='Here you need to specify the high,low,step of each parameter\n and of course, it starts from zero\n',
        title='LEA-gene_pool[]',
        fields=gene_set_field_name,
        values = [5,0,5,5,0,5,5,0,5,5,0,5,5,0,5])
        #values=[str(7 * i - i + 6) for i in range(len(gene_set_field_name))])

    hi_of_each_gene = []
    lo_of_each_gene = []
    n_of_each_gene = []

    step_of_each_gene = []
    range_of_each_gene = []
    val_of_each_gene = []

    for i in range(number_of_gene):
        hi_of_each_gene.append(float(gene_set_input[3 * i + 0]))
        lo_of_each_gene.append(float(gene_set_input[3 * i + 1]))
        n_of_each_gene.append(int(gene_set_input[3 * i + 2]))

    for i in range(number_of_gene):
        # take the absolute of high - low
        step_of_each_gene.append(abs((hi_of_each_gene[i] - lo_of_each_gene[i]) / float(n_of_each_gene[i] - 1)))
        range_of_each_gene.append(abs(hi_of_each_gene[i] - lo_of_each_gene[i]))
        val_of_each_gene.append([])

    for m in range(number_of_gene):
        for k in range(n_of_each_gene[m]):
            val_of_each_gene[m].append(lo_of_each_gene[m] + k * step_of_each_gene[m])

    confirm_message = ''
    for i in range(number_of_gene):
        info = ['***the ', str(i), 'th Gene:',
                '\n                 High:: ', str(hi_of_each_gene[i]),
                '\n                  Low:: ', str(lo_of_each_gene[i]),
                '\n                Range:: ', str(range_of_each_gene[i]),
                '\n                    N:: ', str(n_of_each_gene[i]),
                '\n                 Step:: ', str(step_of_each_gene[i]),
                '\n                         **********Gene Set @ site ' + str(i) + '**********',
                '\n                        ', str(val_of_each_gene[i]),
                '\n']
        confirm_message += ''.join(info)

    easygui.textbox(msg='Here is the confirm message of your input:\n'
                        '\n'
                        'total site = ' + str(number_of_gene) + '\n',
                    title='NSGA-confirm_message',
                    text=confirm_message,
                    codebox=True)

    gene_pool = val_of_each_gene

    return gene_pool


def gui_display_population(self, n=1):
    """
    the name says all
    :return:
    """
    info_population = []

    for number, individual in enumerate(self.individuals):
        individual_str = ''.join((str(number), '   |||   ', str(individual), '\n'))
        info_population.append(individual_str)
    population_message = ''.join(info_population)

    msg = 'Display generation number : ' + str(self.generation_number) + '\n' + \
          'individual#|||                       chromosome                 |fitness\n' \
          '-----------|||--------------------------------------------|-------\n' + \
          'fittest : ' + str(self.find_fittest(n))
    easygui.textbox(msg=msg, text=population_message, codebox=True)