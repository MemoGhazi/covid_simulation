import random
import json
from math import ceil 
"""
I have tested this program by changing parameters such as infection_rate and mortality_rate
and I have found that altering mortality_rate is so important rather than infection_rate.
by increasing mortality_rate instantly the number of death has changed.
"""
N_population = 2500
health_state = [0, 1, 2]
initial_sick_case_rate = 0.1
infection_rate = 0.3
mortality_rate = 0.0002
days=25

def generate_citizen():
    """
    this function generate citizen Id and nested dictionay to insert related info 
    

    citizen: A dictionary which person ID as a key and values as follow:
        'status'  is health status, initialy all population is healthy(means status= 0),
        'day_cnt' is used as counter of day for sick citizen, 
        'control' is a list to prevent visiting people two times
    sick_cases: randomly refer 1 (sick status) to part of population base on initial_sick_case_rate
    by help of sample function
    """
    citizen={}
    for person_id in range(N_population):
        citizen[person_id]={'status': 0, 'day_cnt': 0,'control':[]}
    initial_sick_case = ceil(initial_sick_case_rate * N_population)
    citizen_num = list(citizen.keys())
    sick_cases = random.sample(citizen_num,initial_sick_case)
    for case in sick_cases:
        citizen[case]['status']= 1
    return citizen

def might_seen(person):
    """
    this function return a maximum 20 of people who were not seen earlier by person


    last_seen_ppl: people who were met one time by person
    full_stack_ppl : people who were met by 20 person and should not meet any more
    people_not_seen_before : all population who were not seen by a person and are not 
    the person and are not the full_stack_ppl
    rand_seen: random integer between 0 and maximum people who were not seen but not greater than 20
    group_to_see: random people of 0 to 20 citizen from people_not_seen_before population
    list_comprehesion: append person to all individuals of group_to_see
    """
    last_seen_ppl = citizen.get(person).get('control')
    full_stack_ppl = [i for i in citizen.keys() if len(citizen.get(i).get('control'))==20]
    citizen_list = list(citizen.keys())
    people_not_seen_before = list(set(citizen_list) - set(last_seen_ppl+full_stack_ppl+[person] ))
    rand_seen = random.randint(0, 20-len(last_seen_ppl))
    group_to_see = random.sample(people_not_seen_before, rand_seen)
    [citizen.get(i)['control'].append(person) for i in group_to_see if person not in citizen.get(i)['control']] #list_comprehesion
    return group_to_see
    
def infecting_people(person,citizen_status):
    """
    this function change the status of citizen to sick(status=1) if the conditions were met
    you can track the infected people and find the source of infectious by uncommenting print functin

    group: group of people between (0,20) individuals to meet by person
    group_infect_num: number of individuals who are infected in group ~~> is used for report
    condition_1: among member of group if person is healthy and member is infectd, the probablity 
    of infecting person by member will be estimated
    condition_2: among member of group if person is infected and member is healthy, the probablity 
    of infecting member by person will be estimated
    """
    group = might_seen(person)
    length_of_group = len(group)
    group_infect_num = len([i for i in group if citizen.get(i).get('status')==1])
    for member in group:
        if citizen_status == 0 and citizen[member]['status']==1: # condition_1

            rnd = random.random()
            if rnd < infection_rate:
                citizen[person]['status'] = 1
                # print(f'''citizen number {person}
                # get infected by citizen number {member}
                # length of group {length_of_group} 
                # number of infected in group {group_infect_num} 
                #         ****''')
                break

        elif citizen_status == 1 and citizen[member]['status']==0: # condition_2
            rnd = random.random()
            if rnd < infection_rate:
                citizen[member]['status'] = 1 
                # print(f'''citizen number {member}
                # get infected by citizen number {person}
                # length of group {length_of_group} 
                # number of infected in group {group_infect_num}''')

def day_counting():
    """
    this function is called every day and iterate all citizen in order to update status and day counter every day
    by uncommenting print function we can track citizen who get healed or dead.

    condition_1: if citizen is healthy the probablity of being infectd is inspected.
    condition_2: if citizen is sick the probablity of infecting others is inspected and
    three sub_condition will be inspected:
        sub_condition_1= the probablity of death for sick person
        sub_condition_1= update day counter for sick person
        sub_condition_1= update status if the person were not dead during 10 days
    pass_away: total number of death in one day
    healed: total number of sick person in one day
    """
    pass_away=0
    healed=0
    citizen_list = list(citizen.keys())

    [citizen.get(i)['control'].clear() for i in citizen_list]
    for person in citizen_list:
        if citizen.get(person).get('status') == 0:  # condition_1
            infecting_people(person, citizen_status=0)

        elif citizen.get(person).get('status') == 1:  # condition_2
            infecting_people(person, citizen_status=1)
            rnd = random.random()
            if rnd < mortality_rate:      # sub_condition_1
                citizen.get(person)['status'] = 2
                death_day=citizen.get(person)['day_cnt']
                # print(f'citizen number of {person} has passed away in day {death_day} of disease')
                pass_away+=1

            elif citizen.get(person).get('day_cnt') < 10:  # sub_condition_2
                citizen.get(person)['day_cnt']+=1

            elif citizen.get(person).get('day_cnt') == 10:  # sub_condition_3
                citizen.get(person)['status']=0
                citizen.get(person)['day_cnt']=0
                # print(f'citizen number of {person} get healed************')
                healed+=1
    print(f'{healed} number get heald and {pass_away} passed away just today')


citizen = generate_citizen()
for i in range(1,days+1):  # 
    print(f'***************day {i}****************')
    day_counting()
    print('Total number of disease just for today',len([i for i in citizen.keys() if citizen.get(i)['status']==1]))
    print('Total number of death until today',len([i for i in citizen.keys() if citizen.get(i)['status']==2]))
