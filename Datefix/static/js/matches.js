const matches = document.getElementById('girls')
const list_ = document.getElementById('list_')
let match_list = []
function select(self){
    if (! match_list.includes(self.value) && match_list.length < 2){
        match_list.push(self.value)
        self.setAttribute('selected', 'selected')
        let li = document.createElement('li')
        li.innerText = self.value
        li.id = self.value
        list_.append(li)
    }else if (match_list.includes(self.value) && match_list.length <= 2){
        match_list = match_list.filter((item)=>{return item !== self.value})
        self.removeAttribute('selected')
        let li = document.getElementById(self.value)
        list_.removeChild(li)
    }
    matches.value = match_list.toString()
}