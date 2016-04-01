

 function initFavor(){
   if(isFavor=="False"){
           $(".ui-icon-shadow").removeClass().addClass('ui-icon ui-icon-star ui-icon-shadow no');
    }
    else{
           $(".ui-icon-shadow").removeClass().addClass('ui-icon ui-icon-star ui-icon-shadow yes');
    }
}

 function countNum(){
     if(isFavor=="False"){
         $(".ui-icon-shadow").removeClass().addClass('ui-icon ui-icon-star ui-icon-shadow yes');
         isFavor="True";
     }
     else{
         $(".ui-icon-shadow").removeClass().addClass('ui-icon ui-icon-star ui-icon-shadow no');
         isFavor="False";
     }  
    $.ajax({
        type: "post",
        url: "/customershopdetail",
        data: {
            shopId_favor:shopId_favor,
            customerId:customerId,
            isFavor:isFavor
        },
        success: function(data){
            alert(data);
        },
        dataType:"json"
    });
 }

 
function send_msg(shopId_order){
    // $.ajax({
    //     type: "post",
    //     url: "/customerorder",
    //     data: {
    //         shopId_order:shopId_order,
    //         customerId:customerId
    //     },
    //     success: function(data){
    //         alert(data);
    //     },
    //     dataType:"json"

    // });
    $.post("http://2.cargotest.sinaapp.com/customerorder",
        {
          shopId_order:shopId_order,
          customerId:customerId
        },
        function (data, status) {
            if (data=="unset plate number") {
                document.location.href="#unsetPlateNumFailPage"
            }
            else if(data=="customer breach"){
                document.location.href="#breakRecordFailPage"
            }
            else if(data=="has unfinished record") {
                document.location.href="#unFinishFailPage";
            }
            else if(data=="has no auto order") {
                document.location.href="#noAutoOrderFailPage";
            }
            else {
                document.location.href="#successPage";          
            }
        }
    );
}


minsold=30;
seconds = 59;
function show_time(){
  if(minsold != 0){
         window.setTimeout("show_time()", 1000);
         if(seconds == 59)
             minsold=Math.floor(minsold-1);
         seconds=Math.floor(seconds);
        span_dt_dt.innerHTML=minsold+" 分 "+seconds+" 秒" ;
        if(seconds != 0)
            seconds = (seconds-1);
        else
            seconds = 59;
  }
  else{
    span_dt_dt.innerHTML="预约时间已到" ;
  }
}
show_time();
