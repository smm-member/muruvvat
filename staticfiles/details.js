var prevScrollpos = window.pageYOffset;
var read=true;
var prog='t';
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

function color_chang(n) {
    if (prog!=n){
        if (read==false){
            document.getElementById('pills-read-tab').style.color = 'black';
            document.getElementById('pills-translate-tab').style.color = 'white';
            read=true;
        }
        else{
            document.getElementById('pills-translate-tab').style.color = 'black';
            document.getElementById('pills-read-tab').style.color = 'white';
            read=false;

        }
        prog=n
    }
}