
$(function(){
    $('form').on('submit', function(e){
        $('#loading-container').css('display',"block")
    });
})
$("#close-btn").on("click", function(e){
    $("#loading-container").css('display','none')
    window.stop()
});
// if (window.history && window.history.pushState){
//     alert('HELLO')
// }
window.onpopstate = function() {
    $("#loading-container").css('display','none')
 }; history.pushState({}, '');
