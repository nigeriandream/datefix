from .models import User, Couple
import random
import json


def get_path(request):
    return f'http://{str(request.get_host())}{str(request.get_full_path(True))}'



def _3_point(yourChoice, maximum, Choice):
    if (yourChoice == 0) or abs(yourChoice - Choice) == 0:
        return 1
    
    if abs(Choice - yourChoice) == 1:
        return (1/2)
    
    return 0    
    
    
def age_range(me, you):
   min_ =  me.choice_data_()['min-age'] 
   max_ = me.choice_data_()['max-age']
   age = you.user_data_()['age']
   if int(age) in range(int(min_), int(max_)):
       return 1
   elif abs(int(min_)-int(age)) < 5 and abs(int(max_)-int(age)) < 5:
       return 0.5
   else:
       return 0
       
   
    
   

def _2_point(minimum, maximum, choice):
    if choice < minimum :
        return 0
    if minimum == 0:
        return 1
    total = (maximum - minimum) + 1
    point = (choice - minimum) + 1
    score = (point/total)
    return score


def compare_users(me, you):
    mark = 0
    absolute_match = ['residence-lga', 'residence-state', 'origin-lga',
                      'origin-state', 'denomination', 'religion', 'marital-status', 'children',
                  'blood-group', 'genotype']

    _2_spectrum = ['net-worth', 'education', 'body-shape']

    _3_spectrum = ['complexion', 'height', 'body-type', 'drink', 'smoke', 'conscientiousness', 'openess',
            'extraversion', 'agreeableness', 'neurotism']
    deal_breakers = json.loads(me.deal_breaker)
    print(deal_breakers)
    total = len(absolute_match) + len(_3_spectrum) + len(_2_spectrum) + 1
    
    for i in deal_breakers:
        if i == 'No Dealbreaker':
            continue
        if me.choice_data_()[i] == you.user_data_()[i]:
            mark = mark + 1
        else:
            return 0
    
    for i in absolute_match:
        if me.choice_data_()[i] == you.user_data_()[i] or me.choice_data()[i] == 'Does Not Matter':
            mark = mark + 1
            
    for i in _2_spectrum:
        if me.choice_data()[i] == 'Does Not Matter':
            mark = mark + 1
        mark = mark + _2_point(me.choice_data_()[i], 5, you.user_data_()[i])
    
    
    for i in _3_spectrum:
        if me.choice_data()[i] == 'Does Not Matter':
            mark = mark + 1
        mark = mark + _3_point(me.choice_data_()[i], 5, you.user_data_()[i])
    
    mark = mark + age_range(me, you)
    
    return (mark/total) * 100

def match_user(user):
    success_list = []
    no_list = []
    # filter users 
    all_users = [x for x in User
                 .objects.all() \
                      if (x.complete_match() is False) \
                      and( str(x.id) not in user.jilted_list()) and (x.is_couple() is False )\
                          and (str(x.id) not in user.no_list()) and x.sex == 'male' and 
                          (x.user_data is not None or x.user_data == '')]
    # compare filtered users with user and return matches
    
    for peep in all_users:
        data = {}
        peep_score = compare_users(user, peep)
        my_score = compare_users(peep, user)
        if peep_score >= 50 and my_score >= 50:
            data = {
                "alpha" : peep.username,
                str(peep.id): peep_score,
                "Residence": peep.user_data_['residence-state'],
                "Origin": peep.user_data_['origin-state'],
                "Religion": peep.user_data_['religion'],
                "denomination": peep.user_data_['denomination'],
                "Has Children": peep.user_data_['children']           
                }
            
            success_list.append(sorted(data.items()))
            
        else:
            no_list.append(str(peep.id))
    success_list = mergeSort(success_list)
    user.successful_matches = json.dumps(success_list) 
    user.no_matches = json.dumps(no_list)
    user.save()
    return    
    # matches = []
    # num = 2- user.matches.__len__()
    # if len(success_list['matches'])>= num:
    #     for i in range(num):
    #         matches.append(str(success_list['matches'][success_list['scores'].index(max(success_list['scores']))]))
    #         success_list['matches'].remove(matches[0])
    #         success_list['scores'].remove(max(success_list['scores']))
    #     user.successful_matches = ','.join(success_list)   
    #     user.no_matches = ','.join(no_list)
    #     user.matches = ','.join(matches+user.matches_())
    #     user.save()
    #     return True
    # return False
   
def lucky_draw(num):
    lucky_ones = []
    lists = Couple.objects.all()
    for i in range(num):
        random.shuffle(lists)
        lucky_ones.append(lists[0])
    return lucky_ones

def get_username():
    username = 'User_'+str(random.randint(1, 123456789))
    try:
        User.objects.get(username=username)
        get_username()
    except User.DoesNotExist:
        return username
    


def get_new_match(user,id_):
    jilted_list = user.jilted_list()
    jilted_list.append(str(id_))
    user.jilted_matches = ','.join(jilted_list)
    success_list = {}
    success_list['scores'] = user.successful_scores()
    success_list['matches'] = user.successful_list()
    user.save()
    if len(user.successful_list()) >= 1:
        new_match = success_list['matches'][success_list['scores'].index(max(success_list['scores']))]
        success_list['scores'].remove(user.successful_scores[user.successful_list.index(str(new_match))])
        success_list['matches'].remove(str(new_match))
        user.successful_matches = json.dumps(success_list)
        user_matches = user.matches_()
        user_matches.remove(str(id_))
        user_matches.append(new_match)
        user.matches = ','.join(user_matches)
        user.save()
        return True
    return False
        
    

def update_list_field(user,item, value):
    data = json.loads(user.user_data)
    data[item] = value
    user.profile_changed = True
    user.user_data = json.dumps(data)
    user.save()
    

def adjust_minimum(user, score):
    if score != user.min_score:
        user.min_score = score
        user.save()
        match_user(user)
        
def jilt(user, id_):
    jilted_list = user.jilted_list()
    jilted_list.append(str(id_))
    user.jilted_matches = ','.join(jilted_list)
    user.save()
    
def mergeSort(nlist):
    if len(nlist)>1:
        mid = len(nlist)//2
        lefthalf = nlist[:mid]
        righthalf = nlist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)
        i = j =k = 0
        while i < len(lefthalf) and j < len(righthalf):

            if lefthalf[i][0][1] < righthalf[j][0][1]:
                nlist[k]= lefthalf[i]
                i = i + 1
            else:
                nlist[k] = righthalf[j]
                j = j + 1
            k = k+1
        while i < len(lefthalf):
            nlist[k] = lefthalf[i]
            i = i + 1
            k = k + 1
        while j < len(righthalf):
            nlist[k] = lefthalf[i]
            j = j + 1
            k = k + 1
    return nlist[:9]