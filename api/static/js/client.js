$(
    function(){
        setInterval(fetchData, 200)
    }
)

function fetchData(){    
    $.ajax({
        type: "GET",
        url: "/getmessages",
        dataType: "json",
        success: function(messages) {
            var messages_box = $("#messages");
            var container = messages_box[0];
            var firstTime = true;

            $.each(messages, function(idx, msg){
                const new_message = `[${msg.channel}] >> ${msg.message}<br>`;
                messages_box.append(new_message);
            
                if (firstTime) {
                    container.scrollTop = container.scrollHeight;
                    firstTime = false;
                } else if (container.scrollTop + container.clientHeight === container.scrollHeight) {
                    container.scrollTop = container.scrollHeight;
                }
                  
            })
        },
        error: function() {
            console.log("No se ha podido obtener la información");
        }
    });
}