const matches = document.getElementById('matches_')
let match_list = []
function select(self){
    if (! match_list.includes(self.value) && match_list.length < 2){
        match_list.push(self.value)
        self.setAttribute('selected', 'selected')
    }else if (match_list.includes(self.value) && match_list.length <= 2){
        match_list = match_list.filter((item)=>{return item !== self.value})
        self.removeAttribute('selected')
    }
    matches.value = match_list.toString()
}