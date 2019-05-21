$(window).scroll(function(){
    if($(document).scrollTop() > 10){
        $()
        $('.TheHome').css({
            opacity: '0',
            transition: '0.5s ease-in-out'
        });
    }
    if($(document).scrollTop() < 10){
        $()
        $('.TheHome').css({
            opacity: '1',
            transition: '0.5s ease-in-out'
        });
    }
  });