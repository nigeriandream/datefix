// A personality quiz

// This is an array of objects that stores the personality trait that is prompted to the user and the weight for each prompt. 
// If a personality trait is considered more introverted, it will have a negative weight.
// If a personlity trait is considered more extroverted, it will have a positive weight.

var prompts = [{
    prompt: 'I often do not feel I have to justify myself to people',
    weight: 1,
    class: 'group0',
    id: 1
  },
  {
    prompt: 'I prefer not to engage with people who seem angry or upset',
    weight: -1,
    class: 'group1',
    id: 1
  },
  {
    prompt: 'I do not usually initiate conversations',
    weight: -1,
    class: 'group2',
    id: 1
  },
  {
    prompt: 'I feel comfortable around people',
    weight: 1,
    class: 'group3',
    id: 1
  },
  {
    prompt: 'I keep in the background',
    weight: -1,
    class: 'group4',
    id: 1
  },
  {
    prompt: 'I would rather improvise than spend time coming up with a detailed plan',
    weight: 1,
    class: 'group5',
    id: 1
  },
  {
    prompt: 'I find it easy to walk up to a group of people and join in conversation',
    weight: 1,
    class: 'group6',
    id: 1
  },
  {
    prompt: 'I don\'t like to draw attention to myself',
    weight: -1,
    class: 'group7',
    id: 1
  },
  {
    prompt: 'I care more about making sure no one gets upset than winning a debate',
    weight: 1,
    class: 'group8',
    id: 1
  },
  {
    prompt: 'I get so lost in my thoughts I ignore or forget my surroundings',
    weight: -1,
    class: 'group9',
    id: 1
  },
  {
    prompt: 'I get stressed out easily',
    weight: 1,
    class: 'group10',
    id: 2
  },
  {
    prompt: 'I am relaxed most of the time',
    weight: -1,
    class: 'group11',
    id: 2
  },
  {
    prompt: 'I worry about things',
    weight: 1,
    class: 'group12',
    id: 2
  },
  {
    prompt: 'I seldom feel blue',
    weight: -1,
    class: 'group13',
    id: 2
  },
  {
    prompt: 'I am easily disturbed',
    weight: 1,
    class: 'group14',
    id: 2
  },
  {
    prompt: 'I get upset easily',
    weight: 1,
    class: 'group15',
    id: 2
  },
  {
    prompt: 'I change my mood a lot',
    weight: 1,
    class: 'group16',
    id: 2
  },
  {
    prompt: 'I have frequent mood swings',
    weight: 1,
    class: 'group17',
    id: 2
  },
  {
    prompt: 'I get irritated easily',
    weight: 1,
    class: 'group18',
    id: 2
  },
  {
    prompt: 'I often feel blue',
    weight: 1,
    class: 'group19',
    id: 2
  },
  {
    prompt: 'I feel little concern for others',
    weight: -1,
    class: 'group20',
    id: 3
  },
  {
    prompt: 'I am interested in people',
    weight: 1,
    class: 'group21',
    id: 3
  },
  {
    prompt: 'I insult people',
    weight: -1,
    class: 'group22',
    id: 3
  },
  {
    prompt: 'I sympathize with others\' feelings',
    weight: 1,
    class: 'group23',
    id: 3
  },
  {
    prompt: 'I am not interested in other people\'s problems',
    weight: -1,
    class: 'group24',
    id: 3
  },
  {
    prompt: 'I have a soft heart',
    weight: 1,
    class: 'group25',
    id: 3
  },
  {
    prompt: 'I am not really interested in others',
    weight: -1,
    class: 'group26',
    id: 3
  },
  {
    prompt: 'I take time out for others',
    weight: 1,
    class: 'group27',
    id: 3
  },
  {
    prompt: 'I feel others\' emotions',
    weight: 1,
    class: 'group28',
    id: 3
  },
  {
    prompt: 'I make people feel at ease',
    weight: 1,
    class: 'group29',
    id: 3
  },

]



// This array stores all of the possible values and the weight associated with the value. 
// The stronger agreeance/disagreeance, the higher the weight on the user's answer to the prompt.
var prompt_values = [{
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

// For each prompt, create a list item to be inserted in the list group
function createPromptItems() {

  for (var i = 0; i < prompts.length; i++) {
    var prompt_li = document.createElement('li');
    var prompt_p = document.createElement('p');
    var prompt_text = document.createTextNode(prompts[i].prompt);

    prompt_li.setAttribute('class', 'list-group-item prompt');
    prompt_p.appendChild(prompt_text);
    prompt_li.appendChild(prompt_p);

    document.getElementById('quiz').appendChild(prompt_li);
  }
}

// For each possible value, create a button for each to be inserted into each li of the quiz
// function createValueButtons() {

// 	for (var li_index = 0; li_index < prompts.length; li_index++) {
// 		for (var i = 0; i < prompt_values.length; i++) {
// 			var val_button = document.createElement('button');
// 			var val_text = document.createTextNode(prompt_values[i].value);

// 			val_button.setAttribute('class', 'value-btn btn ' + prompt_values[i].class);
// 			val_button.appendChild(val_text);

// 			document.getElementsByClassName('prompt')[li_index].appendChild(val_button);
// 		}
// 	}
// }
function createValueButtons() {
  for (var li_index = 0; li_index < prompts.length; li_index++) {
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

createPromptItems();
createValueButtons();


let prompts_1 = questions.filter(function (e) {
  return e.id == 1;
});

let prompts_2 = questions.filter(function (e) {
  return e.id == 2;
});

let prompts_3 = questions.filter(function (e) {
  return e.id == 3;
});

let prompts_4 = questions.filter(function (e) {
  return e.id == 4;
});

let prompts_5 = questions.filter(function (e) {
  return e.id == 5;
});


// Keep a running total of the values they have selected. If the total is negative, the user is introverted. If positive, user is extroverted.
// Calculation will sum all of the answers to the prompts using weight of the value * the weight of the prompt.
var total = 0;

// Get the weight associated to group number
function findPromptWeight(prompts_1, group) {
  var weight = 0;

  for (var i = 0; i < prompts_1.length; i++) {
    if (prompts_1[i].class === group) {
      weight = prompts_1[i].weight;
    }
  }

  return weight;
}

// Get the weight associated to the value
function findValueWeight(values, value) {
  var weight = 0;

  for (var i = 0; i < values.length; i++) {
    if (values[i].value === value) {
      weight = values[i].weight;
    }
  }

  return weight;
}



// When user clicks a value to agree/disagree with the prompt, display to the user what they selected
$('.value-btn').mousedown(function () {
  var classList = $(this).attr('class');
  // console.log(classList);
  var classArr = classList.split(" ");
  // console.log(classArr);
  var this_group = classArr[0];
  // console.log(this_group);

  // If button is already selected, de-select it when clicked and subtract any previously added values to the total
  // Otherwise, de-select any selected buttons in group and select the one just clicked
  // And subtract deselected weighted value and add the newly selected weighted value to the total
  if ($(this).hasClass('active')) {
    $(this).removeClass('active');
    total -= (findPromptWeight(prompts_1, this_group) * findValueWeight(prompt_values, $(this).text()));
  } else {
    // $('[class='thisgroup).prop('checked', false);
    total -= (findPromptWeight(prompts_1, this_group) * findValueWeight(prompt_values, $('.' + this_group + '.active').text()));
    // console.log($('.'+this_group+'.active').text());
    $('.' + this_group).removeClass('active');

    // console.log('group' + findValueWeight(prompt_values, $('.'+this_group).text()));
    // $(this).prop('checked', true);
    $(this).addClass('active');
    total += (findPromptWeight(prompts_1, this_group) * findValueWeight(prompt_values, $(this).text()));
  }

  console.log(total);
})



$('#submit-btn').click(function () {
  // After clicking submit, add up the totals from answers
  // For each group, find the value that is active
  $('.results').removeClass('hide');
  $('.results').addClass('show');

  if (total < 0) {
    // document.getElementById('intro-bar').style.width = ((total / 60) * 100) + '%';
    // console.log(document.getElementById('intro-bar').style.width);
    // document.getElementById('intro-bar').innerHTML= ((total / 60) * 100) + '%';
    document.getElementById('results').innerHTML = '<b>You are introverted!</b><br><br>\
  Introverts are tricky to understand, since it’s so easy for us to assume that introversion is the same as being shy, when, in fact, introverts are simply people who find it tiring to be around other people.\n\
<br><br>\
I love this explanation of an introvert’s need to be alone:\n\
<br><br>\
For introverts, to be alone with our thoughts is as restorative as sleeping, as nourishing as eating.\n\n\
<br><br>\
Introverted people are known for thinking things through before they speak, enjoying small, close groups of friends and one-on-one time, needing time alone to recharge, and being upset by unexpected changes or last-minute surprises. Introverts are not necessarily shy and may not even avoid social situations, but they will definitely need some time alone or just with close friends or family after spending time in a big crowd.\
  ';
  } else if (total > 0) {
    document.getElementById('results').innerHTML = '<b>You are extroverted!</b><br><br>\
  On the opposite side of the coin, people who are extroverted are energized by people. They usually enjoy spending time with others, as this is how they recharge from time spent alone focusing or working hard.\
<br><br>\
I like how this extrovert explains the way he/she gains energy from being around other people:\
<br><br>\
When I am among people, I make eye contact, smile, maybe chat if there’s an opportunity (like being stuck in a long grocery store line). As an extrovert, that’s a small ‘ping’ of energy, a little positive moment in the day.';
  } else {
    document.getElementById('results').innerHTML = '<b>You are ambiverted!</b><br><br>\
  Since introverts and extroverts are the extremes of the scale, the rest of us fall somewhere in the middle. Many of us lean one way or the other, but there are some who are quite balanced between the two tendencies. These people are called ambiverts.\
<br><br>\
So let’s look at how an ambivert compares.\
<br><br>\
Ambiverts exhibit both extroverted and introverted tendencies. This means that they generally enjoy being around people, but after a long time this will start to drain them. Similarly, they enjoy solitude and quiet, but not for too long. Ambiverts recharge their energy levels with a mixture of social interaction and alone time.'
  }

  // Hide the quiz after they submit their results
  $('#quiz').addClass('hide');
  $('#submit-btn').addClass('hide');
  $('#retake-btn').removeClass('hide');
})

// Refresh the screen to show a new quiz if they click the retake quiz button
$('#retake-btn').click(function () {
  $('#quiz').removeClass('hide');
  $('#submit-btn').removeClass('hide');
  $('#retake-btn').addClass('hide');

  $('.results').addClass('hide');
  $('.results').removeClass('show');
})