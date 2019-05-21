anime.timeline({loop: true})
  .add({
    targets: '.Name .word',
    scale: [14,1],
    opacity: [0,1],
    easing: "easeOutCirc",
    duration: 900,
    delay: function(el, i) {
      return 900 * i;
    }
  }).add({
    targets: '.Name',
    opacity: 0,
    duration: 1000,
    easing: "easeOutExpo",
    delay: 1000
  });
  $(document).ready(function(){
    setTimeout(function(){
    $('#successMessage').fadeOut();}, 3000);
  });
