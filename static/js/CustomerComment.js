
if(isCommented == 'True')
     document.location.href="#isCommentedPage";

$(document).ready(function(){
    var clickId=0;//点击到的星星位置
    $("li").mousemove(function(){
        if(clickId==0){
            //如果未点击过，则执行此函数，否则就不用弄了，贪方便了= =

            var focusId=$(this).attr("val")/1;
           
            //id属性返回的好像不是一个num，所以用这个，不熟
            var i=1;
            for(;i<=5;i++){
                if(i<=focusId){
                    $("#"+i).removeClass().addClass('yes');
                }
                else{
                    $("#"+i).removeClass().addClass('no');
                }
            }
   
        }
        
    });
    $("li").click(function(){
        var focusId=$(this).attr("id")/1;
             
　　　　if(focusId>=clickId){
            var i=clickId+1;
            for(;i<=focusId;i++){
                $("#"+i).removeClass().addClass('yes');
            }
        }else{
            var i=focusId+1;
            for(;i<=clickId;i++){
                $("#"+i).removeClass().addClass('no');
            }
        }
        clickId=focusId;
    });
    $("li").mouseleave(function(){//未有点击时实现鼠标离开则无亮星星
        if(clickId==0){
　　　　　　var i=1;
            for(;i<=5;i++){
                $("#"+i).removeClass().addClass('no');
            }
        }
    });

    $("#submit").click(function(){
        $.ajax({
            type: "POST",
            url: "/customercomment",
            data: {
                recordId:{{recordId}},
                starRating:clickId,
                comment:$('#comment').val()},
            success: function(data){
                // $('#comment').val(data);
                if (data=="comment success")
                  document.location.href='#successSubmitPage';
            }
        });
    }); 
});