var switchStatus = false;
$("#togBtn").on('change', function() {
    if ($(this).is(':checked')) {
        switchStatus = $(this).is(':checked');
        document.getElementById("inputAdmin4").value = "true";
    }
    else {
       switchStatus = $(this).is(':checked');
       document.getElementById("inputAdmin4").value = "false";
    }
});