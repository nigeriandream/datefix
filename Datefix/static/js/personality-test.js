// A personality quiz

// This is an array of objects that stores the personality trait that is prompted to the user and the weight for each prompt. 
// If a personality trait is considered more introverted, it will have a negative weight.
// If a personlity trait is considered more extroverted, it will have a positive weight.

let email = $('#email').val()
let category = $('#category').val()
let total = 0;



// Keep a running total of the values they have selected. If the total is negative, the user is introverted. If positive, user is extroverted.
// Calculation will sum all of the answers to the prompts using weight of the value * the weight of the prompt.


// Get the weight associated to group number
function findPromptWeight(prompts, group) {
  var weight = 0;

  for (var i = 0; i < prompts.length; i++) {
    if (prompts[i].class === group) {
      weight = prompts[i].weight;
    }
  }

  return weight;
}

// Get the weight associated to the value
function findValueWeight(values, value) {
  let weight = 0;

  for (let i = 0; i < values.length; i++) {
    if (values[i].value === value) {
      weight = values[i].weight;
    }
  }

  return weight;
}

// When user clicks a value to agree/disagree with the prompt, display to the user what they selected
$('.value-btn').mousedown(function () {
  let classList = $(this).attr('class');
  // console.log(classList);
  let  classArr = classList.split(" ");
  // console.log(classArr);
  let this_group = classArr[0];
  // console.log(this_group);

  // If button is already selected, de-select it when clicked and subtract any previously added values to the total
  // Otherwise, de-select any selected buttons in group and select the one just clicked
  // And subtract deselected weighted value and add the newly selected weighted value to the total
  if ($(this).hasClass('active')) {
    $(this).removeClass('active');
    total -= (findPromptWeight(prompts, this_group) * findValueWeight(prompt_values, $(this).text()));
  } else {
    // $('[class='thisgroup).prop('checked', false);
    total -= (findPromptWeight(prompts, this_group) * findValueWeight(prompt_values, $('.' + this_group + '.active').text()));
    // console.log($('.'+this_group+'.active').text());
    $('.' + this_group).removeClass('active');

    // console.log('group' + findValueWeight(prompt_values, $('.'+this_group).text()));
    // $(this).prop('checked', true);
    $(this).addClass('active');
    total += (findPromptWeight(prompts, this_group) * findValueWeight(prompt_values, $(this).text()));
  }

  console.log(total);
})



$('#submit-btn').click(function () {
  $.ajax({
    url: window.location.host + '/personality_test/',
    type: 'POST',
    data: {"score": total, "category": category, "email": email},
    success: (data) => {
      if (data === 'finished')
        window.open(window.location.host + '/personality_test/result/', '_self')

      if (data === 'remaining')
        window.open(window.location.href, '_self')
    }

  })
})