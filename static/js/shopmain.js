var hasClickAutoOrder = false;
var lastOrderTime = -1;
var arriveCount = 0;


//查看某条服务记录的评价
function checkComment(c){
	alert(c);

}

function ajaxSendAutoOrder(){
	var count = document.getElementById("counter").firstChild.nodeValue;
	$.post("/shopmain",
		{
			auto_order_num:count
		},
		function(data,status){
	});
	hasClickAutoOrder = false;
}
//车店要抢的单数量+1
function addCount()
{
	var count = document.getElementById("counter").firstChild.nodeValue;
	if(count<10){
		count++;
		x=document.getElementById("counter");  // 找到元素
		x.innerHTML=count;
	}
	if(!hasClickAutoOrder){
		hasClickAutoOrder = true;
		setTimeout(ajaxSendAutoOrder, 5000);
	}
}
//车店要抢的单数量-1
function reduceCount()
{
	var count = document.getElementById("counter").firstChild.nodeValue;
	if (count>0){
		count--;
		x=document.getElementById("counter");  // 找到元素
		x.innerHTML=count;
	}
	if(!hasClickAutoOrder){
		hasClickAutoOrder = true;
		setTimeout(ajaxSendAutoOrder, 5000);
	}
}
//车店要抢的单数量清零
function closeCount()
{
	var count = document.getElementById("counter").firstChild.nodeValue;
	count = 0;
	x=document.getElementById("counter");  // 找到元素
	x.innerHTML=count;
	if(!hasClickAutoOrder){
		hasClickAutoOrder = true;
		ajaxSendAutoOrder();
	}
}

//订单接收
data1 = [
		{"car_number":"粤A98765",
		"owner":"moumou",
		"phone":"13580554986"
		},
		{"car_number":"阿A98765",
		"owner":"mo飞ou",
		"phone":"135zzzz4986"
		}
];

//将data中的所有订单显示在表中
function addOrder(data)
{
	for(i=0; i<data.length; i++){
		addItem(data[i]);
		reduceCount();
	}
	var ts = "有"+data.length+"位车主预约了洗车！";
	alert(ts);
}
//将一条订单显示在表中
function addItem(item)
{
	$tr = "<tr id='"+item.record_id+"'>";
	$tr += "<td>洗车</td>";
	$tr += "<td>"+item.car_number+"</td>";
	$tr += "<td>"+item.customer+"</td>";
	$tr += "<td>"+item.phone+"</td>";
	//计算预约时间段
	var rsHour = item.reserve_time.substring(11,13);
	var rsMin = item.reserve_time.substring(14,16);
	reMin = rsMin*1+30;
	reHour = rsHour;
	if(reMin>=60){
		reMin -= 60;
		reHour++;
	}
	if(reHour>=24)
		reHour = "00";
	if(reHour<10)
		reHour ="0"+reHour;
	if(reMin<10)
		reMin = "0"+reMin;

	$tr += "<td>"+rsHour+":"+rsMin+"~"+reHour+":"+reMin+"</td>";
	//抽取估计到达时间
	var eHour = item.eva_time.substring(11,13);
	var eMin = item.eva_time.substring(14,16);
	$tr += "<td>"+eHour+":"+eMin+"</td>";
	$tr += "<td><input id='' type='button' value='已到' onclick='deleteTr(this)'></td></tr>";	
	$tr += "</tr>";	
	$("#table_coming_head").after($tr);			
}			


function ajaxGetNewOrder(){
	$.post("/shopmain",
		{
			record_id:lastOrderTime
		},
		function(data,status){
			if(status =="success"&&data.length>3){
				var json = JSON.parse(data);
				addOrder(json);
				if(arriveCount>0)
					 $("#arrive_null").css("display","none");
				lastOrderTime = json[0].record_id;
			}
	});
}

//点击已到的处理
function deleteTr(obj) {
	trid = $(obj).parent().parent().attr("id");
	finishOrder(trid);
    $(obj).parent().parent().remove();
    if(arriveCount>0){
    	arriveCount--;
    	if(arriveCount == 0){
    		$("#arrive_null").css("display","inline");
    	}
    }
}
function finishOrder(finish_id)
{
	$.post("/shopmain",
		{
			finish_record_id:finish_id
		},
		function(data,status){
			alert("本条订单已转入已完成列表");
	});
}

//已完成列表处理 
function addSearchOrder(data)
{
	for(i=0; i<data.length; i++){
		addItem2(data[i]);
	}
}
function addItem2(item)
{
	$tr = "<tr id='"+item.record_id+"'>";
	$tr += "<td>洗车</td>";	
	$tr += "<td>"+item.car_number+"</td>";
	$tr += "<td>"+item.customer+"</td>";
	$tr += "<td>"+item.phone+"</td>";
	$tr += "<td>"+item.reserve_time+"</td>";
	$tr += "<td><input id='' type='button' value='查看评价' onclick='checkComment(this)'></td></tr>";	
	$tr += "</tr>";
	$("#table_finish_head").after($tr);
}
function ajaxGetOldOrder(stime, etime){
	$.post("/shopmain",
		{
			start_time:stime,
			end_time:etime
		},
		function(data,status){
			if(status =="success"){
				$("#table_finish tr:not(:first)").remove();
				if(data.length>3){
					var objs = JSON.parse(data);
					addSearchOrder(objs);
					$("#finish_null").css("display","none");
				}
				else{
					$("#finish_null").css("display","inline");
				}
			}
	});
}
function doSearch()
{
	var st = $("#start_year").val()+"-";
	st += $("#start_month").val()+"-";
	st += $("#start_day").val();

	var et = $("#end_year").val()+"-";
	et += $("#end_month").val()+"-";
	et += $("#end_day").val();

	ajaxGetOldOrder(st,et);
}
//查看某条服务记录的评价
function checkComment(cmt){
	trid = $(cmt).parent().parent().attr("id");
	ajaxCommentOrder(trid);
}
function ajaxCommentOrder(cid)
{
	$.post("/shopmain",
		{
			comment_record_id:cid
		},
		function(data,status){
			alert(data);
	});
}


//初始化日期----------------------------------------------------------------------------
function createSelect(ActionFlag,yy,mm,dd) { 
	var selYear = document.getElementById(yy); 
	var selMonth = document.getElementById(mm); 
	var selDay = document.getElementById(dd); 
	var dt = new Date(); 
	if(ActionFlag == 1) { 
		MinYear = dt.getFullYear()-5; 
		MaxYear = dt.getFullYear(); 

		for(var i = MinYear; i <= MaxYear; i++) { 
			var op = document.createElement("OPTION"); 
			op.value = i; 
			op.innerHTML = i; 
			selYear.appendChild(op); 
		} 
		selYear.selectedIndex = 5; 

		for(var i = 1; i < 13; i++) { 
			var op = document.createElement("OPTION"); 
			op.value = i; 
			op.innerHTML = i; 
			selMonth.appendChild(op); 
		} 
		selMonth.selectedIndex = dt.getMonth(); 
	} 

	var date = new Date(selYear.value, selMonth.value, 0); 
	var daysInMonth = date.getDate(); 
	selDay.options.length = 0; 

	for(var i = 1; i <= daysInMonth ; i++) { 
		var op = document.createElement("OPTION"); 
		op.value = i; 
		op.innerHTML = i; 
		selDay.appendChild(op); 
	} 
	
	selDay.selectedIndex = dt.getDate() - 1; 
}

$(document).ready(function(){
	//请求Order
	setInterval("ajaxGetNewOrder()",2000);

	var isFresh = true;

 	$("#menu_coming").click(function(){
 		x = document.getElementById("menu_coming");
    	x.style.color="#ed6639";
    	x = document.getElementById("menu_finish");
    	x.style.color = "#7f909a"; 

    	$("#table_finish").slideUp("fast");
    	$("#table_coming").slideDown("fast");
  	});

  	$("#menu_finish").click(function(){
    	x = document.getElementById("menu_finish");
    	x.style.color="#ed6639";
    	x = document.getElementById("menu_coming");
    	x.style.color = "#7f909a"; 

    	$("#table_coming").slideUp("fast");
    	$("#table_finish").slideDown("fast");
    	if(isFresh){
    		createSelect(1,"start_year","start_month","start_day");
    		createSelect(1,"end_year","end_month","end_day");
    		doSearch();
    		isFresh = false;
    	}
  	});

  	//退出登录
  	$("#logout").click(function(){
  		closeCount();
  		ajaxLogout();
  		location.href = "/shoplogin";
  	});
});

function ajaxLogout()
{
	// alert("logout");
	$.post("/shopmain",
		{
			logout:true
		},
		function(data,status){
			// alert(data);
	});
}