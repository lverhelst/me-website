$(document).keydown(function(e) {
    switch (e.which) {
      case 37: // left
        var href = $('#prev').attr('href');
        if(href === undefined)
            break; //donothing
        window.location.href = href;
        e.preventDefault(); 
        break;
  
      case 39: // right
        var href = $('#next').attr('href');
        if(href === undefined)
            break; //donothing
        window.location.href = href;
        e.preventDefault(); 
        break;
    }
  });



/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function togglebtn() {
  document.getElementById("dropdown-content").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
//window.onclick = function(event) {
//  if (!event.target.matches('.dropbtn')) {
//    var dropdowns = document.getElementsByClassName("dropdown-content");
//    var i;
//    for (i = 0; i < dropdowns.length; i++) {
//      var openDropdown = dropdowns[i];
//      if (openDropdown.classList.contains('show')) {
//        openDropdown.classList.remove('show');
//      }
//    }
//  }
//} 