var prevScrollpos = window.pageYOffset;
var now=false;
var audio = new Audio('https://qurango.net/radio/mix');
window.onscroll = function() {
var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos){    
    document.getElementById("navbar").style.top = "0";   
  } else {
    if (currentScrollPos>=70){
      document.getElementById("navbar").style.top = "-70px";
    }
  }
  prevScrollpos = currentScrollPos;
}

function radio(){
  if (now == true){
    audio.pause();
    now=false;
    document.getElementById('radio-button-replace').innerHTML=''
    document.getElementById('radio-button-replace').innerHTML='<svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 2v20.364l16-10.182L4 2Z" fill="currentColor"></path></svg> Play Radio'
    }
  else{
    now=true;
    audio.play();
    document.getElementById('radio-button-replace').innerHTML=''
    document.getElementById('radio-button-replace').innerHTML='<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-pause" viewBox="0 0 15 15"><path d="M6 3.5a.5.5 0 0 1 .5.5v8a.5.5 0 0 1-1 0V4a.5.5 0 0 1 .5-.5zm4 0a.5.5 0 0 1 .5.5v8a.5.5 0 0 1-1 0V4a.5.5 0 0 1 .5-.5z"/></svg> Pause Radio'
  }
}
