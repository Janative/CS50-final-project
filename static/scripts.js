// Passing booking ID value to modal
$(".tocancel").click(function() {
    var name = $(this).prev().val(); //use prev
    $("#modal_body").html(name);
    $("#bookId").val(name); //use val here
});

//Seating.html - coloring the seats based on availability (taken / taken by you / free) - by changing of their classes
function nastav_classes_pre_tieto_idcka(idcka, current_user) {
    for (let i = 0; i < idcka.length; i++) {
        var idcko = idcka[i]['seat_id']
        var user = idcka[i]['user_id']

        if (user == current_user) {
            document.getElementById(idcko).className.baseVal = "st2"; 
            console.log("Z JavaScriptu:" + idcko); 
        }
        else {
            document.getElementById(idcko).className.baseVal = "st1"
            console.log("Z JavaScriptu:" + idcko)
        }
    }

}

// Run the script once the page is loaded
// document.addEventListener('DOMContentLoaded', function() {
    // // Vytvorim object submitest, ktora identifikuje element s ID #takenseats
    // let takenseats = document.querySelector('.takenseats');
    
    // for (let i = 0; i < takenseats.length; i++ ) {
    //     document.getElementById("1").style.color = "#FF0000";
    //     }
    
    // })


// document.getElementById("2").className.baseVal = "st1"






  