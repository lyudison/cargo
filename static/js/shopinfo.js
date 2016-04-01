var pictures = new Array();
var currentPicture = 1;
var numOfPicture = 3;


function getPictures(){
  pictures[0] = "http://p15.qhimg.com/bdm/1440_900_85/d/_open360/carn0228/2.jpg";
  pictures[1] = "http://p18.qhimg.com/bdm/1600_900_85/d/_open360/car01070/7.jpg";
  pictures[2] = "http://p16.qhimg.com/bdm/1440_900_85/d/_open360/car1108/6.jpg";
}

function setIndex()
{
  var index = $("#image_this").attr("src");
  index = index.substring(index.length-5, index.length-4);
  $("#imagepath").val(index);
  var ttt = $("#imagepath").val();
}

function orange(tt)
{
	var x = document.getElementById(tt);
    x.style.backgroundColor="#ed6639";
}

function gray(tt)
{
	var x = document.getElementById(tt);
   	x.style.backgroundColor="#afc0ca";
}

$(document).ready(function(){
  //图片初始化
  // getPictures();
  // $("#image_this").attr("src",pictures[currentPicture]);
  $(".images").hide("fast");
  $("#image_this").show("fast");
 
  //返回按钮
  $("#back").click(function(){
    location.href = "/shopmain";
  }); 

	$("#menu_info").css("backgroundColor","#ed6639");
 	$("#menu_info").click(function(){
 		orange("menu_info");
 		gray("menu_account");
 		gray("menu_image");
    $("#image_content").css("display","none");
    $("#info_content").css("display","inline");
    $("#account_content").css("display","none");
  });

  $("#menu_image").click(function(){
   	orange("menu_image");
 	  gray("menu_info");
		gray("menu_account");
  	$("#image_content").css("display","inline");
  	$("#info_content").css("display","none");
   	$("#account_content").css("display","none");
  });

  $("#menu_account").click(function(){
  	orange("menu_account");
 		gray("menu_info");
 		gray("menu_image");
 		$("#image_content").css("display","none");
    $("#info_content").css("display","none");
    $("#account_content").css("display","inline");
  });


  	$("#change_password_button").click(function(){
    	$("#change_password").slideDown("fast");
  	});
  	$("#slideup_password_button").click(function(){
    	$("#change_password").slideUp("fast");
  	});

  	$("#change_phone_button").click(function(){
    	$("#change_phone").slideDown("fast");
  	});
  	$("#slideup_phone_button").click(function(){
    	$("#change_phone").slideUp("fast");
  	});


  	$("#change_discribe_button").click(function(){
  		$("#discribe_area").removeAttr("readonly");
  		$("#discribe_area").css("background","#fff");
  		$("#discribe_save_button").css("display","inline");
  		$("#discribe_cancel_button").css("display","inline");
  	});
  	$("#discribe_cancel_button").click(function(){
  		$("#discribe_area").attr("readonly","readonly");
  		$("#discribe_area").css("background","transparent");
  		$("#discribe_save_button").css("display","none");
  		$("#discribe_cancel_button").css("display","none");
  	});

  	$("#change_tel_button").click(function(){
    	$("#change_tel").slideDown("fast");
  	});
  	$("#slideup_tel_button").click(function(){
    	$("#change_tel").slideUp("fast");
  	});

    //改变照片
    $("#change_image_button").click(function(){
      $("#change_image").slideDown("fast");
      setIndex();
    });
    $("#cancel_image_button").click(function(){
      $("#change_image").slideUp("fast");z
    });


    //车店图片滚动
    // $("#image_left").click(function(){
    //   currentPicture--;
    //   if (currentPicture<0){
    //     currentPicture = numOfPicture-1;
    //   };
    //   $("#image_this").attr("src",pictures[currentPicture]);
    // });
    $("#image_right").click(function(){
      var last = $("#image_last").attr("src");
      var the = $("#image_this").attr("src");
      var next = $("#image_next").attr("src");
      $("#image_last").attr("src",the);
      $("#image_this").attr("src",next);
      $("#image_next").attr("src",last);
      setIndex();
    });
    $("#image_right").mousedown(function(){
      $("#image_right").attr("src","/static/img/icon/right_arrow_active.png");
    });
    $("#image_right").mouseup(function(){
      $("#image_right").attr("src","/static/img/icon/right_arrow.png");
    });
    $("#image_left").click(function(){
      var last = $("#image_last").attr("src");
      var the = $("#image_this").attr("src");
      var next = $("#image_next").attr("src");
      $("#image_last").attr("src",next);
      $("#image_this").attr("src",last);
      $("#image_next").attr("src",the);
      setIndex();
    });
    $("#image_left").mousedown(function(){
      $("#image_left").attr("src","/static/img/icon/left_arrow_active.png");
    });
    $("#image_left").mouseup(function(){
      $("#image_left").attr("src","/static/img/icon/left_arrow.png");
    });
});
