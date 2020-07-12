from django.core.mail import send_mail

from .models import User, Couple
import random
import json


def get_path(request):
    return f'http://{str(request.get_host())}{str(request.get_full_path(True))}'


def _3_point(your_choice, choice):
    if (your_choice == 0) or abs(your_choice - choice) == 0:
        return 1

    if abs(choice - your_choice) == 1:
        return 1 / 2

    return 0


def age_range(me, you):
    min_ = me.choice_data_()['min-age']
    max_ = me.choice_data_()['max-age']
    age = you.user_data_()['age']
    if int(age) in range(int(min_), int(max_)):
        return 1
    elif abs(int(min_) - int(age)) < 5 and abs(int(max_) - int(age)) < 5:
        return 0.5
    else:
        return 0


def _2_point(minimum, maximum, choice):
    if choice < minimum:
        return 0
    if minimum == 0:
        return 1
    total = (maximum - minimum) + 1
    point = (choice - minimum) + 1
    score = (point / total)
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
        if you.user_data_()[i] in me.choice_data_()[i].split(',') or 'Does Not Matter' in me.choice_data()[i].split(
                ','):
            mark = mark + 1

    for i in _2_spectrum:
        if me.choice_data()[i] == 'Does Not Matter':
            mark = mark + 1
        mark = mark + _2_point(me.choice_data_()[i], 5, you.user_data_()[i])

    for i in _3_spectrum:
        if me.choice_data()[i] == 'Does Not Matter':
            mark = mark + 1
        mark = mark + _3_point(me.choice_data_()[i], you.user_data_()[i])

    mark = mark + age_range(me, you)

    return (mark / total) * 100


def match_user(user):
    try:
        success_list = []
        no_list = []
        # filter users
        all_users = [x for x in User.objects.all()
                     if (x.complete_match() is False)
                     and (str(x.id) not in user.jilted_list()) and (x.is_couple() is False)
                     and (str(x.id) not in user.no_list()) and x.sex == 'male' and
                     (x.user_data is not None or x.user_data == '')]
        # compare filtered users with user and return matches

        for peep in all_users:
            data = {}
            peep_score = compare_users(user, peep)
            my_score = compare_users(peep, user)
            if peep_score >= 50 and my_score >= 50:
                data = {
                    "alpha": peep.username,
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
        success_list = merge_sort(success_list)
        user.successful_matches = json.dumps(success_list)
        user.no_matches = json.dumps(no_list)
        user.save()
        return True
    except:
        return False


def lucky_draw(num):
    lucky_ones = []
    lists = Couple.objects.all()
    for i in range(num):
        random.shuffle(lists)
        lucky_ones.append(lists[0])
    return lucky_ones


def get_username():
    username = 'User_' + str(random.randint(1, 123456789))
    try:
        User.objects.get(username=username)
        get_username()
    except User.DoesNotExist:
        return username


def merge_sort(n_list):
    if len(n_list) > 1:
        mid = len(n_list) // 2
        left_half = n_list[:mid]
        right_half = n_list[mid:]

        merge_sort(left_half)
        merge_sort(right_half)
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):

            if left_half[i][0][1] < right_half[j][0][1]:
                n_list[k] = left_half[i]
                i = i + 1
            else:
                n_list[k] = right_half[j]
                j = j + 1
            k = k + 1
        while i < len(left_half):
            n_list[k] = left_half[i]
            i = i + 1
            k = k + 1
        while j < len(right_half):
            n_list[k] = left_half[i]
            j = j + 1
            k = k + 1
    return n_list[:9]


def flash(request, message, status, icon):
    request.session['message'] = message
    request.session['status'] = status
    request.session['icon'] = icon
    return


category_1 = [{
    'Question': 'I often do not feel I have to justify myself to people',
    'Weight': 1,
    'Category': ''
},
    {
        'Question': 'I prefer not to engage with people who seem angry or upset',
        'Weight': -1
    },
    {
        'Question': 'I do not usually initiate conversations',
        'Weight': -1
    },
    {
        'Question': 'I feel comfortable around people',
        'Weight': 1
    },
    {
        'Question': 'I keep in the background',
        'Weight': -1
    },
    {
        'Question': 'I would rather improvise than spend time coming up with a detailed plan',
        'Weight': 1
    },
    {
        'Question': 'I find it easy to walk up to a group of people and join in conversation',
        'Weight': 1
    },
    {
        'Question': 'I don\'t like to draw attention to myself',
        'Weight': -1
    },
    {
        'Question': 'I care more about making sure no one gets upset than winning a debate',
        'Weight': 1
    },
    {
        'Question': 'I get so lost in my thoughts I ignore or forget my surroundings',
        'Weight': -1
    },
]
category_2 = [{
    'Question': 'I get stressed out easily',
    'Weight': 1
},
    {
        'Question': 'I am relaxed most of the time',
        'Weight': -1
    },
    {
        'Question': 'I worry about things',
        'Weight': 1
    },
    {
        'Question': 'I seldom feel blue',
        'Weight': -1
    },
    {
        'Question': 'I am easily disturbed',
        'Weight': 1
    },
    {
        'Question': 'I get upset easily',
        'Weight': 1
    },
    {
        'Question': 'I change my mood a lot',
        'Weight': 1
    },
    {
        'Question': 'I have frequent mood swings',
        'Weight': 1
    },
    {
        'Question': 'I get irritated easily',
        'Weight': 1
    },
    {
        'Question': 'I often feel blue',
        'Weight': 1
    },
]
category_3 = [{
    'Question': 'I feel little concern for others',
    'Weight': -1
},
    {
        'Question': 'I am interested in people',
        'Weight': 1
    },
    {
        'Question': 'I insult people',
        'Weight': -1
    },
    {
        'Question': 'I sympathize with others\' feelings',
        'Weight': 1
    },
    {
        'Question': 'I am not interested in other people\'s problems',
        'Weight': -1
    },
    {
        'Question': 'I have a soft heart',
        'Weight': 1
    },
    {
        'Question': 'I am not really interested in others',
        'Weight': -1
    },
    {
        'Question': 'I take time out for others',
        'Weight': 1
    },
    {
        'Question': 'I feel others\' emotions',
        'Weight': 1
    },
    {
        'Question': 'I make people feel at ease',
        'Weight': 1
    },

]
category_4 = [{
    'Question': 'I am always prepared',
    'Weight': 1
},
    {
        'Question': 'I leave my belongings around',
        'Weight': -1
    },
    {
        'Question': 'I pay attention to detail',
        'Weight': 1
    },
    {
        'Question': 'I make a mess of things',
        'Weight': -1
    },
    {
        'Question': 'I get chores done right away',
        'Weight': 1
    },
    {
        'Question': 'I like order',
        'Weight': 1
    },
    {
        'Question': 'I try to avoid my duties',
        'Weight': -1
    },
    {
        'Question': 'I follow a schedule',
        'Weight': 1
    },
    {
        'Question': 'I am thorough in my work',
        'Weight': 1
    },
    {
        'Question': 'I often forget to put things back in their proper place',
        'Weight': -1
    },
]
category_5 = [{
    'Question': 'I have a rich vocabulary',
    'Weight': 1
},
    {
        'Question': 'I have difficulty understanding abstract ideas',
        'Weight': -1
    },
    {
        'Question': 'I have a vivid imagination',
        'Weight': 1
    },
    {
        'Question': 'I am not interested in abstract ideas',
        'Weight': -1
    },
    {
        'Question': 'I have excellent ideas',
        'Weight': 1
    },
    {
        'Question': 'I do not have a good imagination',
        'Weight': -1
    },
    {
        'Question': 'I am quick to understand things',
        'Weight': 1
    },
    {
        'Question': 'I spend time reflecting on things',
        'Weight': 1
    },
    {
        'Question': 'I am full of ideas',
        'Weight': 1
    },
    {
        'Question': 'I often use difficult words',
        'Weight': 1
    },

]

categories = ['Extraversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']

personality = (
    [
        {"title": "", "description": ""},
        {"title": "", "description": ""},
        {"title": "", "description": ""}
    ],
    [
        {"title": "", "description": ""},
        {"title": "", "description": ""},
    ],
    [
        {"title": "", "description": ""},
        {"title": "", "description": ""},
    ],
    [
        {"title": "", "description": ""},
        {"title": "", "description": ""},
    ],
    [
        {"title": "", "description": ""},
        {"title": "", "description": ""},
    ]

)

our_categories = (category_1, category_2, category_3, category_4, category_5)


def get_personality(score, category):
    if category != 'Extraversion':
        if score > 0:
            return json.dumps(personality[categories.index(category)][1])
        else:
            return json.dumps(personality[categories.index(category)][0])
    else:
        if score < -1:
            my_personality = json.dumps(personality[categories.index(category)][0])
            return my_personality
        if score > 1:
            my_personality = json.dumps(personality[categories.index(category)][2])
            return my_personality
        my_personality = json.dumps(personality[categories.index(category)][1])
        return my_personality


def display(request):
    if 'message' in request.session:
        message = request.session['message']
        status = request.session['status']
        icon = request.session['icon']
        del request.session['message'], request.session['status'], request.session['icon']
        return message, status, icon
    return None


def send_verification(request):
    if not request.session['verification_sent']:
        request.session['code'] = request.POST['csrfmiddlewaretoken']
        link = f'http://{request.get_host()}/account/verify/?code={request.POST["csrfmiddlewaretoken"]}?email={request.POST["email"]}'
        message = f''' Dear {request.user.first_name}, \n We are excited to have you on Datefix. Below is the link to 
    verify your email address, click on this link to continue.\n \n {link} \nIf you have no account with Datefix, 
    please ignore.\n\nCheers,\nDatefix Team. '''
        send_mail('Email Verification', message, 'admin@datefix.me', [request.POST['email']])
        request.session['verification_sent'] = True
    return


def dict_to_zip(data):
    questions = set([x['Question'] for x in data])
    weights = ([x['Weight'] for x in data])
    count = set([data.index(x) for x in data])
    return zip(count, questions, weights)
