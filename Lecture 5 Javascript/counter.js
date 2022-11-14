//let counter=0;
//if there is no value for counter is laready stored in localstorage then set the value as 0
if(!localStorage.getItem('counter')){
    localStorage.setItem('counter',0);
}

function count(){
    //store the value we get from the localstorage in a variable counter
    let counter=localStorage.getItem('counter');
    counter++;
    //alert(counter);
    document.querySelector('h1').innerHTML=counter;
    //seting the localstorage value of counter to the value counter
    localStorage.setItem('counter',counter);
    if(counter%10==0){
        alert(`Your counter is now at ${counter}`);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    //when the page is loaded set the value we get from the local storage as the value in h1 tag
    document.querySelector('h1').innerHTML=localStorage.getItem('counter');

    //running the count function when the button is pressed
    document.querySelector('button').onclick = count;
    //running the count function internally after every 3 seconds even when the button is not pressed
    //setInterval(count,3000);
    });