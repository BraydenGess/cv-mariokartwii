from tools.utility import remove_newline,get_scoringdict
import os
from __init__ import *

def avg(l):
    return sum(l)/len(l)

def write_tofile(information_file,course_dict):
    f = open(information_file, 'w')
    f.write('CourseName,FastStaff,LengthRank,APPoll,CPI,img,txtcolor\n')
    ### Labels ###
    for element in course_dict:
        course = course_dict[element]
        if course.course_name != 'Opening':
            f.write(course.course_name)
            f.write(',')
            f.write(course.fast_staff)
            f.write(',')
            f.write(course.length_rank)
            f.write(',')
            f.write(course.AP)
            f.write(',')
            f.write(str(course.CPI))
            f.write(',')
            f.write(course.img.split('/')[-1])
            f.write(',')
            f.write(course.txtcolor)
            f.write('\n')
def calculate_CPI():
    course_dict,course_indexlookup = make_coursedict(file_name='Rock.csv')
    scoring_dict = get_scoringdict()
    stat_folder = 'nextgenstats/data/'
    for file in os.listdir(stat_folder):
        f = open(stat_folder+file,'r')
        datalines = f.readlines()
        for i in range(len(datalines)):
            dataline = datalines[i].split(',')
            if i%4 != 3:
                key = dataline[0]
                if 'F' in key:
                    print('Incomplete Data- not 3 races in GP')
                    sys.exit()
                elixir_flag = dataline[1]
                course_name = dataline[5]
                p1 = dataline[11]
                p2 = dataline[15]
                p3 = dataline[19]
                p4 = dataline[23]
                score = scoring_dict[p1] + scoring_dict[p2] + scoring_dict[p3] + scoring_dict[p4]
                if elixir_flag == 'Y':
                    course_dict[course_indexlookup[course_name]].elixir.append(score)
                if elixir_flag == 'N':
                    course_dict[course_indexlookup[course_name]].regular.append(score)
        f.close()
    CPI_values = []
    for element in course_dict:
        course_name = course_dict[element].course_name
        elx = course_dict[element].elixir
        reg = course_dict[element].regular
        if ((sum(elx) != 0)and(sum(reg)!=0)):
            cpi = avg(elx)-avg(reg)
        else:
            cpi = -100
        if course_name != 'Opening':
            CPI_values.append([course_name,cpi])
    CPI_values.sort(key=lambda x:x[1],reverse=True)
    information_file = 'nextgenstats/information/coursedata.csv'
    for i in range(len(CPI_values)):
        course_name = CPI_values[i][0]
        course = course_dict[course_indexlookup[course_name]]
        cpi = CPI_values[i][1]
        if cpi != -100:
            course.CPI = i+1
        else:
            course.CPI = 'NR'
    write_tofile(information_file, course_dict)

calculate_CPI()