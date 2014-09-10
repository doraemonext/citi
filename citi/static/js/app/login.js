'use strict';
require(['jquery'], function ($) {
	$(document).ready(function () {
			var ico_close='<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 500 500" enable-background="new 0 0 500 500" xml:space="preserve"><path d="M274.649,250.002L494.894,29.77c6.812-6.812,6.812-17.847,0-24.659c-6.812-6.812-17.847-6.812-24.658,0L250.002,225.344L29.77,5.111c-6.812-6.812-17.847-6.812-24.659,0c-6.812,6.812-6.812,17.847,0,24.659l220.233,220.233L5.111,470.235c-6.812,6.812-6.812,17.847,0,24.658c6.812,6.812,17.847,6.812,24.659,0l220.233-220.244l220.233,220.244c6.812,6.812,17.847,6.812,24.658,0s6.812-17.847,0-24.658L274.649,250.002z"/></svg>';
			
			var close=document.getElementById("close");
			close.innerHTML=ico_close;

			var ico_email=document.getElementById("ico_email");
			ico_email.innerHTML=ico_close;

			var ico_password=document.getElementById("ico_password");
			ico_password.innerHTML=ico_close;
			
			$("#chkbox").click(function(){
				console.log(111,470)
				var chkbox=document.getElementById("chkbox");
				var real_chkbox=document.getElementById("real_chkbox");
				if(real_chkbox.checked==false){
					real_chkbox.checked=true;
					chkbox.style.background="#7abe9f";
				}else{
					real_chkbox.checked=false;
					chkbox.style.background="#f4f4f4";
				}
			})
	
	})
})
