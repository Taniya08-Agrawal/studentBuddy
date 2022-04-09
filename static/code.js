window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'UA-187726107-1');

   
$("#login_form").on('submit', function(event) {
	event.preventDefault();
	var email = $("#loginemail").val();
	var password = $("#loginpassword").val();
	if ($.trim(email)=="") {
		$("#loginemail").focus();
		return false;
	}
	if ($.trim(password)=="") {
		$("#loginpassword").focus();
		return false;
	}
	$(".loginbtn").val("Please Wait...");
	$(".loginbtn").attr('disable',true);
	$.ajax({
		url: 'https://www.paraphraser.io/login',
		type: 'POST',
		dataType: "json",
		data: {
			"email" : email,
			"password" : password
		},
		success: function(res){
			console.log(typeof(res));
			if (res.message =="error") {
				$("#login_error").show();
				$("#login_error").html("Incorrect Email OR Password");
			}else if (res.message =="email_not_verified"){
				$("#login_error").show();
				$("#login_error").html("Please verify your email!");
				$("#login_form,#signup_form").hide();
				$("#email_verify_form").show();
				$("#verifyemail").val(email);
			}else if (res.message == "success"){
				$("#login_success").show();
				$("#login_success").html("Logged In Successfully!");
				setTimeout(function(){
					window.location.replace('https://www.paraphraser.io/');
				},2000);
			}else if(res.message == 'not_premium'){

				window.location.replace('https://www.paraphraser.io/pricing-plans?id='+res.id);
			}
			setTimeout(function(){
				$("#login_success").hide();
				$("#login_error").hide();
			},3000);
			$(".loginbtn").val("Log In");
			$(".loginbtn").attr("disable",false);
		}
	});
});	
$("#signup_form").on('submit', function(event) {
	event.preventDefault();
	var fullname = $("#signupfullname").val();
	var email = $("#signupemail").val();
	var password = $("#signuppassword").val();
	if ($.trim(fullname)=="") {
		$("#signupfullname").focus();
		return false;
	}
	if ($.trim(email)=="") {
		$("#signupemail").focus();
		return false;
	}
	if ($.trim(password)=="") {
		$("#signuppassword").focus();
		return false;
	}
	$(".signupbtn").val("Please Wait...");
	$(".signupbtn").attr("disable",true);
	$.ajax({
		url: 'https://www.paraphraser.io/signup',
		type: 'POST',
		data: {
			"fullname" : fullname,
			"email" : email,
			"password" : password
		},
		success: function(res){
			if (res=="error") {
				$("#login_error").show();
				$("#login_error").html("Something Went Wrong. Please try again!");
			}else if (res=="email_error") {
				$("#login_error").show();
				$("#login_error").html("Email already Exists!");
			}else if (res=="success"){
				window.location.replace('https://www.paraphraser.io/pricing-plans');
				
			}
			setTimeout(function(){
				$("#login_success").hide();
				$("#login_error").hide();
			},3000);
			$(".signupbtn").val("Sign Up");
			$(".signupbtn").attr("disable",false);
		}
	});
});
$("#changelanguage").on('change', function(event) {
	event.preventDefault();
	window.location.replace($(this).val());
});


function alert_box(msg="",title="Error!", close = false,background="",ok="OK"){

	if(background !== ""){
		$('.alert-box-img').css({background:'url('+background+')',
		height: "155px"
		});
		$('.alert-box-ok').html(ok);
	}
	$('.alert-box-heading').html(title);
	$('.alert-box-subheading').html(msg);
	$('.alert-box-wrap, .alert-box').show();
	if(close){
		setTimeout(() => {
			alert_box_hide();
		}, 500);
	}
}

function alert_box_hide(){
	$('.alert-box-wrap, .alert-box').hide();
}

$('.alert-box-wrap, .alert-box-ok').on('click', function(){
	alert_box_hide()
 });
 function change_url(url){
window.location.replace(url);
}

$(function() {
	$('#mobile-app-promo span.close-app-btn').on('click', function(){
		$('#mobile-app-promo').hide();
	});

			setTimeout(() => {
			if($('.adsenbox').length > 0){ $('.adsenbox').removeClass('bg-gray')}
		}, 100);
	
	window.addEventListener("resize",function(){is_mobile=window.innerWidth<768,is_mobile_x=window.innerWidth<576,window.is_mobile=is_mobile,window.is_mobile_x=is_mobile_x});

		setTimeout(() => {
		var callBackCaptcha = "";
		$.getScript( "https://www.google.com/recaptcha/api.js"+callBackCaptcha, function( data, textStatus, jqxhr ) {
			console.log( jqxhr.status, "recaptcha Load." );
		});
	}, 2500);
	
	setTimeout(() => { $("head").append('<link rel="stylesheet" href="https://www.paraphraser.io/assets/frontend/css/themify-icons.css">'); }, is_mobile ? 3000 : 1000 );
});

$(".special_cource_text").hover(function() {
    $(".special_cource_text").removeClass('active');
    $(this).addClass('active');
  }, function() {
    $(".special_cource_text").removeClass('active');
    $(".plan2").addClass('active');
  });
  $('#summarize_now').on('click', function(event) {
    event.preventDefault();
    onSubmit();
  });
  var lang = 'text-summarizer';



  function onSubmit(){
    var captcharesponse = grecaptcha.getResponse();
      var innerText = $('#input-content').val() || '';
     
      if(!innerText){
        alert_box("Input Text Required ","Validation Error");
      }else if(innerText.length < 200){
        alert_box("Atleast require minimum 200 characters","Validation Error");
      }else if(!captcharesponse){
        alert_box("","Captcha required");
      }else{
        btn_status('#summarize_now',1);
        var strr = innerText.replace("'","`").split(" ").slice(0,1000).join(" ");
        var strr = strr.replaceAll('‘',"`");
        var strr = strr.replaceAll('’',"`");
        var breakdata = strr.match(/[^\s.!?]+[^.!?\r\n]+[.!?]*/g);
        var chunks = 1;
        var sendArr = new Array;
        var brdata = '';
        totalLen = breakdata.length
        $.each(breakdata,function(index,value){
          brdata += value;
          var chunkLim = 5;
          if((chunks == chunkLim) || (chunks == totalLen)){
            sendArr.push(brdata);
            brdata = '';
            chunks = 1;
            totalLen = totalLen-chunkLim;
          }else{
            chunks++;
          }
        });
        var mode = $("#mode").val();
        var la = "English";
        var capc = captcharesponse;
        var done = 0;
        var base_url = "https://www.paraphraser.io/";
        runAllAjax(strr.split(),mode,la,capc,done);
        function runAllAjax(array,mode,la,capc,done=0) {
          $("#output-content,#input-content").css('opacity', '0.3');
          $(".paraphrase-loader").fadeIn();
          var i = 0;
          var totlLen = array.length;
          var percnt = Math.floor(100/totlLen);
          var percntNew = 0;
          var itrs = totlLen - 1;
          
          var newPercentageLoader = window.setInterval(function(){
            percntNew++;
            $('#percent-suggested').html(percntNew+"%");
                  $('#percent-progress').attr('aria-valuenow',percntNew);
                  $('#percent-progress').css('width',percntNew+"%");
          }, 900);
  
          var summerylen = parseInt($('#summeryLength').val());
  
          function next() {
            var strr = array[i];
            $.ajax({
              async: true,
              url:base_url+"frontend/summarizerBeta",
              method:"post",
              dataType: "JSON",
              data:{data:strr, percnt: 70, sorder: 'no',captcha:capc},
              beforeSend: function(){
                btn_status('#summarize_now',1,'  Processing... ');
              },
              success: function(resultdata){
                clearInterval(newPercentageLoader);
  
                if(resultdata.error) {
                  alert_box(resultdata.msg || "Somthing Went Wrong");
                } else {
                  result = resultdata.result
                
                    if(i > itrs) {
                      $("#output-content,#input-content").css('opacity', '1');
                      $(".paraphrase-loader").fadeOut();
   
                    } else {
                      if (done==0) {
                        done = 1;
                      }
                      
                      datt+='</p>';
  
                      html += datt ;
                      html += '</div>';
                      html = html.replace(/4444/g, '');
                      $("#output-content").html(html);
                      $('#_text_to_exported').val(striptags(html));
  
                      // -- Output End
                      $('#percent-suggested').html(percntNew+"%");
                      $('#percent-progress').attr('aria-valuenow',percntNew);
                      $('#percent-progress').css('width',percntNew+"%");
                      $("#copy_to_clipboard_box").css('display','flex');
                      i++;
                      // next();
                    }
  
                }
  
                
              }
            }).always(function(xh){
                $("#output-content,#input-content").css('opacity', '1');
                $(".paraphrase-loader").fadeOut();
                btn_status('#summarize_now',0);
                console.log('captcha reset')
                grecaptcha.reset();
              });
          }
          next();
        }
        $("#select-ouput").click(function(){$("#ouput-content-box").selectText()});
        jQuery.fn.selectText = function(){
          var doc = document;
          var element = this[0];
          console.log(this, element);
          if (doc.body.createTextRange) {
              var range = document.body.createTextRange();
              range.moveToElementText(element);
              range.select();
          } else if (window.getSelection) {
              var selection = window.getSelection();        
              var range = document.createRange();
              range.selectNodeContents(element);
              selection.removeAllRanges();
              selection.addRange(range);
          }
        };
      }
  }