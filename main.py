#Log librarie and API import
import gspread
import logging

if __name__ == '__main__':
    #Configurations of log file
    logging.basicConfig(filename = 'Desafio-Tunts.Rocks-2024\monitored_activities.logs', 
                        format='%(asctime)s %(levelname)-8s %(message)s', 
                        level=logging.DEBUG, 
                        datefmt='%Y-%m-%d %H:%M:%S')

    #Api connected and dheet authentication
    gc = gspread.service_account(filename = 'Desafio-Tunts.Rocks-2024\keys.json')
    sh = gc.open_by_key('1F0Mo_CrKpUj4qqq8vGEDTLhfOClg8v-W082kFJqH4wQ')
    ws = sh.worksheet('engenharia_de_software')
    logging.info('API connected and sheet authentication successful')

    #Data aquisition from worksheet
    aluno = ws.col_values(2)[3:]
    faltas = ws.col_values(3)[3:]
    p1 = ws.col_values(4)[3:]
    p2 = ws.col_values(5)[3:]
    p3 = ws.col_values(6)[3:]
    logging.info('Data acquired from sheets')

    #Creation of lists for furthr operations
    average_list = []
    situation_list = []
    naf_list = []
    logging.info('Lists Created')

    #For loop to calculate and define status of each student
    for i in range(len(aluno)):
        #Data conversion to calculate the average
        p1[i] = int(p1[i])
        p2[i] = int(p2[i])
        p3[i] = int(p3[i])
        faltas[i] = int(faltas[i])
        logging.info(f'Data from {aluno[i]} converted from str to int for calculations')

        #Average calculation and append in a list previous created
        average = ((p1[i]+p2[i]+p3[i])/3.0)/10.0
        average_list.append(average)
        logging.info(f'{aluno[i]} Average grade {average:.2f} calculated and appended in average_list')
        logging.info(f'{aluno[i]} had {faltas[i]} absences')

        #Absences condition test
        if faltas[i] > (0.25*60.0):
            situation_list.append('Reprovado')
            naf_list.append(0)
            logging.info(f'{aluno[i]} disapproved status for absences appendend in situation_list')

        #Grade below minimum limit test
        elif average < 5.0:
            situation_list.append('Reprovado')
            naf_list.append(0)
            logging.info(f'{aluno[i]} disapproved for grades status appendend in situation_list')

        #Final Exam eligibility test
        elif average >= 5.0 and average < 7.0:
            situation_list.append('Exame Final')
            naf = (10.0 - average)*2
            naf = int(naf+0.5)*10
            naf_list.append(naf)
            logging.info(f'{aluno[i]} eligible for final exam status appendend in situation_list')

        #If all test above fail the deafult situation is defined
        else:
            situation_list.append('Aprovado')
            naf_list.append(0)
            logging.info(f'{aluno[i]} Approved status appendend in situation_list')

    #New values updated in tehe worksheet
    ws.update("G4", [[g] for g in situation_list])
    ws.update("H4", [[h] for h in naf_list])
    logging.info('Data updated to sheets')