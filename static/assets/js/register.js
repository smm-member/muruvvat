function edit_region() {
    fetch('https://muruvvat.netlify.app/regions.json')
    .then(response => response.json())
    .then(response => {
    var ans = ""
    var data = document.getElementById('region').value;
    var a = JSON.parse(JSON.stringify(response))[data]
    a.forEach(i => {
      ans+=`<option value="${i}">${i}</option>`
    });
    document.getElementById("location").innerHTML = ans;
  })
  }
  edit_region()