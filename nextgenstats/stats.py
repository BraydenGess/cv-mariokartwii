from tools.utility import remove_newline
import os
class Course():
    def __init__(self,name=None,length=None,AP=None,d_races=None,r_races=None,CPI=None):
        self.name = name
        self.length = length
        self.AP = AP
        self.d_races = d_races
        self.r_races = r_races
        self.CPI = CPI

def recalculate_coursestats():
    item_dict = dict()
    course_dict = dict()
    f = open('nextgenstats/information/coursedata.csv', 'r')
    course_data = f.readlines()
    for i in range(len(course_data)):
        data = course_data[i].split(',')
        course = Course(name=data[0], length=data[1], AP=remove_newline(data[2]),d_races=[],r_races=[])
        course_dict[i] = course
        item_dict[data[0]] = i
    f.close()
    data_folder = 'nextgenstats/data/'
    for datafile in os.listdir(data_folder):
        f = open(data_folder+datafile,'r')
        race_data = f.readlines()
        for i in range(len(race_data)):
            race_dataline = race_data[i].split(',')
            print(race_dataline)
    return 42

recalculate_coursestats()