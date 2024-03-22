$(document).ready(function() {
    $.ajax({
        url: '/candyland/',
        type: 'GET',
        success: function(response) {
            var winner = response.variable;
            if (winner == 0) {
                $('winner').hide();
            }
            else {
                var message = "Player " + winner + " wins!";
                $('winner').show(message);
            }
        }
    });
});