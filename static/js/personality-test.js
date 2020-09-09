// A personality quiz


let total = 0;
let scores = [0,0,0,0,0,0,0,0,0,0]
let selected = [null, null, null, null, null, null, null, null, null, null]
let buttons = document.getElementsByClassName('value-btn')



// Get the weight associated to the value
const findValueWeight = (value) => {
  switch(value){
      case 'Strongly Agree': return 5;
      case 'Agree': return 3;
      case 'Neutral': return 0;
      case 'Disagree': return -3;
      case 'Strongly Disagree': return -5;
  }
}

// When user clicks a value to agree/disagree with the prompt, display to the user what they selected

let curr_prompt_btn = null

let prev_btn = null

const theAction = (item) => {
  if (curr_prompt_btn === item){
      return
    }
    prev_btn = curr_prompt_btn
    curr_prompt_btn = item
    const prompt_id = item.classList[0]
    selected[Number(prompt_id.replace('prompt', ''))] = item
    const prompt = document.getElementById(prompt_id)
    curr_prompt_btn = item
    const buttons_ = document.getElementsByClassName(prompt_id)
    if (prev_btn !== null){
      prev_btn.classList.remove('active')
      prev_btn.classList.remove('marked')
      scores[Number(prompt_id.replace('prompt', ''))] = (Number(prompt.className) *
          findValueWeight(prev_btn.innerText));
      returnTotal()
    }

    curr_prompt_btn.classList.add('active')
    curr_prompt_btn.classList.add('marked')
    scores[Number(prompt_id.replace('prompt', ''))] = (Number(prompt.className) *
        findValueWeight(curr_prompt_btn.innerText));
    returnTotal()

  }



function returnTotal(){
  total = 0
  scores.forEach((item)=>{
    total = total + item
  })
  selected.forEach((item)=>{
    if (item !== null){
       item.classList.add('active')
    }

  })
  for (let i = 0; i < buttons.length; i++){
    if (! selected.includes(buttons[i])){
      buttons[i].classList.remove('active')
    }
  }
}






  $('#submit-btn').click(function () {
    let response
    let email = document.getElementById('email').classList[2]
    let  input_email
      try{
        input_email = document.getElementsByName('email')[0].value

      }catch (typeError) {
        input_email = email
      }
    const category = document.getElementById('category').classList[1]

    if (selected.includes(null) ||
        (email === undefined && input_email === '')) {
      alert('You have not finished filling your form')
      return
    }
    if (email === undefined) {
        email = input_email
      }
    $.ajax({
    url: window.location.origin+'/personality_test/submit/',
    type: 'GET',
    data: {"score": total, "category": category, "email": email},
    success: (data) => {
        response = data

        if (response === 'Finished')
            window.open(window.location.origin+'/personality_test/result/', '_self')

        if (response === 'Remaining')
            window.open(window.location.href, '_self')
        }

  })

})