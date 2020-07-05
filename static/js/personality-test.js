// A personality quiz

// This is an array of objects that stores the personality trait that is prompted to the user and the weight for each prompt. 
// If a personality trait is considered more introverted, it will have a negative weight.
// If a personlity trait is considered more extroverted, it will have a positive weight.

const prompts_1 = [{
    prompt: 'I find it difficult to introduce myself to people',
    weight: -1,
    class: 'group0'
  },
  {
    prompt: 'I get so lost in my thoughts I ignore or forget my surroundings',
    weight: -1,
    class: 'group1'
  },
  {
    prompt: 'I do not usually initiate conversations',
    weight: -1,
    class: 'group2'
  },
  {
    prompt: 'I prefer not to engage with people who seem angry or upset',
    weight: -1,
    class: 'group3'
  },
  {
    prompt: 'I choose my friends carefully',
    weight: -1,
    class: 'group4'
  },
  {
    prompt: 'I find it difficult to tell stories about myself',
    weight: -1,
    class: 'group5'
  },
  {
    prompt: 'I am usually highly motivated and energetic',
    weight: 1,
    class: 'group6'
  },
  {
    prompt: 'I find it easy to walk up to a group of people and join in conversation',
    weight: 1,
    class: 'group7'
  },
  {
    prompt: 'Being adaptable is more important than being organized',
    weight: 1,
    class: 'group8'
  },
  {
    prompt: 'I care more about making sure no one gets upset than winning a debate',
    weight: 1,
    class: 'group9'
  },
  {
    prompt: 'I often do not feel I have to justify myself to people',
    weight: 1,
    class: 'group10'
  },
  {
    prompt: 'I would rather improvise than spend time coming up with a detailed plan',
    weight: 1,
    class: 'group11'
  }
]

const prompts_2 = [{
    prompt: 'I find it difficult to introduce myself to people',
    weight: -1,
    class: 'group0'
  },
  {
    prompt: 'I get so lost in my thoughts I ignore or forget my surroundings',
    weight: -1,
    class: 'group1'
  },
  {
    prompt: 'I do not usually initiate conversations',
    weight: -1,
    class: 'group2'
  },
  {
    prompt: 'I prefer not to engage with people who seem angry or upset',
    weight: -1,
    class: 'group3'
  },
  {
    prompt: 'I choose my friends carefully',
    weight: -1,
    class: 'group4'
  },
  {
    prompt: 'I find it difficult to tell stories about myself',
    weight: -1,
    class: 'group5'
  },
  {
    prompt: 'I am usually highly motivated and energetic',
    weight: 1,
    class: 'group6'
  },
  {
    prompt: 'I find it easy to walk up to a group of people and join in conversation',
    weight: 1,
    class: 'group7'
  },
  {
    prompt: 'Being adaptable is more important than being organized',
    weight: 1,
    class: 'group8'
  },
  {
    prompt: 'I care more about making sure no one gets upset than winning a debate',
    weight: 1,
    class: 'group9'
  },
  {
    prompt: 'I often do not feel I have to justify myself to people',
    weight: 1,
    class: 'group10'
  },
  {
    prompt: 'I would rather improvise than spend time coming up with a detailed plan',
    weight: 1,
    class: 'group11'
  }
]

const prompts_3 = [{
    prompt: 'I find it difficult to introduce myself to people',
    weight: -1,
    class: 'group0'
  },
  {
    prompt: 'I get so lost in my thoughts I ignore or forget my surroundings',
    weight: -1,
    class: 'group1'
  },
  {
    prompt: 'I do not usually initiate conversations',
    weight: -1,
    class: 'group2'
  },
  {
    prompt: 'I prefer not to engage with people who seem angry or upset',
    weight: -1,
    class: 'group3'
  },
  {
    prompt: 'I choose my friends carefully',
    weight: -1,
    class: 'group4'
  },
  {
    prompt: 'I find it difficult to tell stories about myself',
    weight: -1,
    class: 'group5'
  },
  {
    prompt: 'I am usually highly motivated and energetic',
    weight: 1,
    class: 'group6'
  },
  {
    prompt: 'I find it easy to walk up to a group of people and join in conversation',
    weight: 1,
    class: 'group7'
  },
  {
    prompt: 'Being adaptable is more important than being organized',
    weight: 1,
    class: 'group8'
  },
  {
    prompt: 'I care more about making sure no one gets upset than winning a debate',
    weight: 1,
    class: 'group9'
  },
  {
    prompt: 'I often do not feel I have to justify myself to people',
    weight: 1,
    class: 'group10'
  },
  {
    prompt: 'I would rather improvise than spend time coming up with a detailed plan',
    weight: 1,
    class: 'group11'
  }
]

const prompts_4 = [{
    prompt: 'I find it difficult to introduce myself to people',
    weight: -1,
    class: 'group0'
  },
  {
    prompt: 'I get so lost in my thoughts I ignore or forget my surroundings',
    weight: -1,
    class: 'group1'
  },
  {
    prompt: 'I do not usually initiate conversations',
    weight: -1,
    class: 'group2'
  },
  {
    prompt: 'I prefer not to engage with people who seem angry or upset',
    weight: -1,
    class: 'group3'
  },
  {
    prompt: 'I choose my friends carefully',
    weight: -1,
    class: 'group4'
  },
  {
    prompt: 'I find it difficult to tell stories about myself',
    weight: -1,
    class: 'group5'
  },
  {
    prompt: 'I am usually highly motivated and energetic',
    weight: 1,
    class: 'group6'
  },
  {
    prompt: 'I find it easy to walk up to a group of people and join in conversation',
    weight: 1,
    class: 'group7'
  },
  {
    prompt: 'Being adaptable is more important than being organized',
    weight: 1,
    class: 'group8'
  },
  {
    prompt: 'I care more about making sure no one gets upset than winning a debate',
    weight: 1,
    class: 'group9'
  },
  {
    prompt: 'I often do not feel I have to justify myself to people',
    weight: 1,
    class: 'group10'
  },
  {
    prompt: 'I would rather improvise than spend time coming up with a detailed plan',
    weight: 1,
    class: 'group11'
  }
]

const prompts_5 = [{
    prompt: 'I find it difficult to introduce myself to people',
    weight: -1,
    class: 'group0'
  },
  {
    prompt: 'I get so lost in my thoughts I ignore or forget my surroundings',
    weight: -1,
    class: 'group1'
  },
  {
    prompt: 'I do not usually initiate conversations',
    weight: -1,
    class: 'group2'
  },
  {
    prompt: 'I prefer not to engage with people who seem angry or upset',
    weight: -1,
    class: 'group3'
  },
  {
    prompt: 'I choose my friends carefully',
    weight: -1,
    class: 'group4'
  },
  {
    prompt: 'I find it difficult to tell stories about myself',
    weight: -1,
    class: 'group5'
  },
  {
    prompt: 'I am usually highly motivated and energetic',
    weight: 1,
    class: 'group6'
  },
  {
    prompt: 'I find it easy to walk up to a group of people and join in conversation',
    weight: 1,
    class: 'group7'
  },
  {
    prompt: 'Being adaptable is more important than being organized',
    weight: 1,
    class: 'group8'
  },
  {
    prompt: 'I care more about making sure no one gets upset than winning a debate',
    weight: 1,
    class: 'group9'
  },
  {
    prompt: 'I often do not feel I have to justify myself to people',
    weight: 1,
    class: 'group10'
  },
  {
    prompt: 'I would rather improvise than spend time coming up with a detailed plan',
    weight: 1,
    class: 'group11'
  }
]

const url = [window.location.host, 'personality_test', ''].join('/')

const email = $('#user_email')



// This array stores all of the possible values and the weight associated with the value. 
// The stronger agreeance/disagreeance, the higher the weight on the user's answer to the prompt.
var prompt_values= [{
    value: 'Strongly Agree',
    class: 'btn-default btn-strongly-agree',
    weight: 5
  },
  {
    value: 'Agree',
    class: 'btn-default btn-agree',
    weight: 3,
  },
  {
    value: 'Neutral',
    class: 'btn-default',
    weight: 0
  },
  {
    value: 'Disagree',
    class: 'btn-default btn-disagree',
    weight: -3
  },
  {
    value: 'Strongly Disagree',
    class: 'btn-default btn-strongly-disagree',
    weight: -5
  }
]


// This stores the total values from each prompts
let totals = [0, 0, 0, 0, 0]


//This array stores the personality results
let personalities = ['', '', '', '', '']

// For each prompt, create a list item to be inserted in the list group
function createPromptItems(prompt) {

  for (var i = 0; i < prompt.length; i++) {
    var prompt_li = document.createElement('li');
    var prompt_p = document.createElement('p');
    var prompt_text = document.createTextNode(prompt[i].prompt);

    prompt_li.setAttribute('class', 'list-group-item prompt');
    prompt_p.appendChild(prompt_text);
    prompt_li.appendChild(prompt_p);

    document.getElementById('quiz').appendChild(prompt_li);
  }
}


function createValueButtons(prompt) {
  for (var li_index = 0; li_index < prompt.length; li_index++) {
    var group = document.createElement('div');
    group.className = 'btn-group btn-group-justified';

    for (var i = 0; i < prompt_values.length; i++) {
      var btn_group = document.createElement('div');
      btn_group.className = 'btn-group';

      var button = document.createElement('button');
      var button_text = document.createTextNode(prompt_values[i].value);
      button.className = 'group' + li_index + ' value-btn btn ' + prompt_values[i].class;
      button.appendChild(button_text);

      btn_group.appendChild(button);
      group.appendChild(btn_group);

      document.getElementsByClassName('prompt')[li_index].appendChild(group);
    }
  }
}


const array_prompt = [prompts_1, prompts_2, prompts_3, prompts_4, prompts_5]
let viewed = 0

const next_button = document.getElementById('next_btn')
next_button.onclick = () =>{
    viewed +=1
    if (viewed === array_prompt.length){
        show_result()
    }
    createPromptItems(array_prompt[viewed])
    createValueButtons(array_prompt[viewed])

    // For each group, find the value that is active and compute total
    // When user clicks a value to agree/disagree with the prompt,
    // display to the user what they selected

    $('.value-btn').mousedown(compute_total())

}

const result_view = $('.results')
const quiz_view = $('#quiz')

const show_result = () => {


  // Hide the quiz after they submit their results
  quiz_view.addClass('hide');
  $('#submit-btn').addClass('hide');
  $('#retake-btn').removeClass('hide');

  result_view.removeClass('hide');
  result_view.addClass('show');


    // After clicking submit, get the results

  document.getElementById('results_0').innerHTML = compute_personality(0)
  document.getElementById('results_1').innerHTML = compute_personality(1)
  document.getElementById('results_2').innerHTML = compute_personality(2)
  document.getElementById('results_3').innerHTML = compute_personality(3)
  document.getElementById('results_4').innerHTML = compute_personality(4)

  //send user's data to database
  send_to_db()
}


const prompt_results = [
    [
        {personality: '', description: ''},
      {personality: '', description: ''},
    {personality: '', description: ''}
    ],
    [
        {personality: '', description: ''},
      {personality: '', description: ''},
    {personality: '', description: ''}
    ],
    [
        {personality: '', description: ''},
      {personality: '', description: ''},
    {personality: '', description: ''}
    ],
    [
        {personality: '', description: ''},
      {personality: '', description: ''},
    {personality: '', description: ''}
    ],
    [
        {personality: '', description: ''},
      {personality: '', description: ''},
    {personality: '', description: ''}
    ]
]


const compute_personality = (index) =>{
  const prompt_result = prompt_results[index]
  if (totals[index] < 0) {
    personalities[index] = prompt_result[0].personality
    return (prompt_result[0].description);
  }
  if (totals[index] > 0) {
    personalities[index] = prompt_result[1].personality
        return (prompt_result[1].description)
    }
  personalities[index] = prompt_result[2].personality
  return(prompt_result[2].description)

    }


// Keep a running total of the values they have selected. If the total is negative, the user is introverted. If positive, user is extroverted.
// Calculation will sum all of the answers to the prompts using weight of the value * the weight of the prompt.

const compute_total = ()=> {
  const classList = $(this).attr('class');
  // console.log(classList);
  const classArr = classList.split(" ");
  // console.log(classArr);
  const this_group = classArr[0];
  // console.log(this_group);

  // If button is already selected, de-select it when clicked and subtract any previously added values to the total
  // Otherwise, de-select any selected buttons in group and select the one just clicked
  // And subtract deselected weighted value and add the newly selected weighted value to the total
  if ($(this).hasClass('active')) {
    $(this).removeClass('active');
    totals[viewed] -= (findPromptWeight(array_prompt[viewed], this_group) * findValueWeight(prompt_values, $(this).text()));
  } else {
    // $('[class='thisgroup).prop('checked', false);
    total[viewed] -= (findPromptWeight(array_prompt[viewed], this_group) * findValueWeight(prompt_values, $('.' + this_group + '.active').text()));
    // console.log($('.'+this_group+'.active').text());
    $('.' + this_group).removeClass('active');

    // console.log('group' + findValueWeight(prompt_values, $('.'+this_group).text()));
    // $(this).prop('checked', true);
    $(this).addClass('active');
    total[viewed] += (findPromptWeight(array_prompt[viewed], this_group) * findValueWeight(prompt_values, $(this).text()));
  }

  console.log(total[viewed]);

}


// Get the weight associated to group number
const findPromptWeight = (prompts, group) =>{
  var weight = 0;

  for (var i = 0; i < prompts.length; i++) {
    if (prompts[i].class === group) {
      weight = prompts[i].weight;
    }
  }

  return weight;
}

// Get the weight associated to the value
const findValueWeight = (values, value) => {
  var weight = 0;

  for (var i = 0; i < values.length; i++) {
    if (values[i].value === value) {
      weight = values[i].weight;
    }
  }

  return weight;
}

const send_to_db =()=>{
  const user_data = {email : email.val() , score : JSON.stringify(totals),
    personality : JSON.stringify(personalities)}
  $.ajax({
    url: url,
    data: user_data,
    type : 'GET',
    json : true,
    success : (data)=>{
      console.log(data)
    }
  })
}



// '<b>You are introverted!</b><br><br>\
// 		Introverts are tricky to understand, since it’s so easy for us to assume that introversion is the same as being shy, when, in fact, introverts are simply people who find it tiring to be around other people.\n\
// <br><br>\
// I love this explanation of an introvert’s need to be alone:\n\
// <br><br>\
// For introverts, to be alone with our thoughts is as restorative as sleeping, as nourishing as eating.\n\n\
// <br><br>\
// Introverted people are known for thinking things through before they speak, enjoying small, close groups of friends and one-on-one time, needing time alone to recharge, and being upset by unexpected changes or last-minute surprises. Introverts are not necessarily shy and may not even avoid social situations, but they will definitely need some time alone or just with close friends or family after spending time in a big crowd.\
// 		'



// '<b>You are ambiverted!</b><br><br>\
// 		Since introverts and extroverts are the extremes of the scale, the rest of us fall somewhere in the middle. \
// 		Many of us lean one way or the other, but there are some who are quite balanced between the two tendencies. \
// 		These people are called ambiverts.\
// <br><br>\
// So let’s look at how an ambivert compares.\
// <br><br>\
// Ambiverts exhibit both extroverted and introverted tendencies. This means that they generally enjoy being around people,\
//  but after a long time this will start to drain them. Similarly, they enjoy solitude and quiet, but not for too long. \
//  Ambiverts recharge their energy levels with a mixture of social interaction and alone time.'

// '<b>You are extroverted!</b><br><br>\
// 		On the opposite side of the coin, people who are extroverted are energized by people. They usually enjoy spending time with others, as this is how they recharge from time spent alone focusing or working hard.\
// <br><br>\
// I like how this extrovert explains the way he/she gains energy from being around other people:\
// <br><br>\
// When I am among people, I make eye contact, smile, maybe chat if there’s an opportunity (like being stuck in a long grocery store line). As an extrovert, that’s a small ‘ping’ of energy, a little positive moment in the day.'