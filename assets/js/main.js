
$(function(){
    $('form').on('submit', function(e){
        $('#loading-container').css('display',"block")
    });
})
$("#close-btn").on("click", function(e){
    $("#loading-container").css('display','none')
    window.stop()
});

window.onpopstate = function() {
    $("#loading-container").css('display','none')
 }; history.pushState({}, '');
