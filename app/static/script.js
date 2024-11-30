      function toggle_details(id)  {
        element = document.getElementById('taskdetails-'+id);
        if (element) {
          if (element.classList.contains("show")) {
            element.classList.remove("show");            
            //btn.innerHTML = "&#x25bc";  // Down Arrow
          } 
          else {
            element.classList.add("show");            
            //btn.innerHTML = "&#x25b2;";  // Up Arrow
          }
        }
      }      