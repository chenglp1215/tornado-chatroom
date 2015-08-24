(function() {
    var $msg = $('#msg');
    var $text = $('#text');

    var WebSocket = window.WebSocket || window.MozWebSocket;
    if (WebSocket) {
        try {
            var socket = new WebSocket('ws://'+location.host+'/new-msg/socket');
        } catch (e) {}
    }

    if (socket) {
        socket.onmessage = function(event) {
            $msg.append('<p>' + event.data + '</p>');
            var target= $('#input').offset().top;
            $('body').animate({scrollTop:target}, 300);
        }

        $('form').submit(function() {
            socket.send($text.val());
            $text.val('').select();
            return false;
        });
    }
    setInterval(function(){
        $.ajax({
            url: '/user-count',
            type: 'GET',
            success: function(event) {
                $("#user-count").text('当前在线'+event + '人');
                console.log(event)
            }
        })
    }, 1000)
})();