'use strict';
require(['base', 'lib/jquery.cropbox'], function (base) {
	var $ = base.$;
	$(document).ready(function () {
		jQuery.extend(jQuery.validator.messages, {
			required: '必选字段',
			remote: '请修正该字段',
			email: '请输入正确格式的电子邮件',
			equalTo: '两次密码不一致',
			accept: '请输入拥有合法后缀名的字符串'
		});
		// sign content
		var previous = $('#previous'),
			next = $('#next'),
			skip = $('#skip'),
			submit = $('#submit'),
			status = 0,
			headerList = $('.js-sign-header').find('li:has(a)'),
			contentList = $('.js-sign-content').children(),
			form = $('#sign'),
			agreement = $('#agreement'),
			email;

		// form validate
		form.validate({
			rules: {
				email: {
					email: true,
					required: true
				},
				password: 'required',
				repassword: {
					required: true,
					equalTo: '#password'
				},
				nickname: 'required',
				province: 'required',
				occupation: 'required',
			}
		})

		// check scroll bottom
		$('.js-scroll').on('scroll', function () {
			var $this = $(this),
				scrollTop = $this.scrollTop(),
				innerHeight = $this.height(),
				outerHeight = $this.find('.js-scroll-wrap').height();
			if (1 || scrollTop + innerHeight >= outerHeight) {
				agreement.prop('disabled', false);
				agreement.on('change', function () {
					next.prop('disabled', !$(this).prop('checked'));
				})
			}
		})
		var prevaction = function () {
				$(headerList[status]).removeClass('active');
				$(headerList[status - 1]).removeClass('done').addClass('active');
				$(contentList[status]).fadeOut();
				$(contentList[status - 1]).fadeIn();
				status -= 1;
				previous.prop('disabled', false);
				next.prop('disabled', false);
				$(document.body).animate({scrollTop: 160})
			},
			nextaction = function () {
				$(headerList[status]).removeClass('active').addClass('done');
				$(headerList[status + 1]).addClass('active');
				$(contentList[status]).fadeOut();
				$(contentList[status + 1]).fadeIn();
				status += 1;
				previous.prop('disabled', false);
				next.prop('disabled', false);
				$(document.body).animate({scrollTop: 160})
			};

		previous.on('click', function () {
			if (status === 2) {
				skip.hide();
				submit.hide();
				next.show();
			}
			prevaction();
		})
		
		next.on('click', function () {
			if (status === 1) {
				if (!form.valid()) {
					return;
				}
				skip.show();
				submit.show();
				next.hide();
			}
			nextaction();
		})

		// location
		var province = $('#province'),
		city = $('#city'),
		vacant = $('<option value=""></option>');
		$.getJSON('js/province.json').success(function (data) {
			var provinceHtml = '';
			for (var i = 0, len = data.length; i < len; i = i + 1) {
				provinceHtml += '<option value="' + data[i].id +'">' + data[i].name + '</option>';
			}
			province.append(vacant).append(provinceHtml);
		})
		province.on('change', function () {
			vacant.remove();
			$.getJSON('js/' + province.val() + '.json').success(function (data) {
				var cityHtml = '';
				for (var i = 0, len = data.length; i < len; i = i + 1) {
					cityHtml += '<option value="' + data[i].id +'">' + data[i].name + '</option>';
				}
				city.empty().append(vacant).append(cityHtml);
			})
		})
		city.on('change', function () {
			vacant.remove();
		})

		// var img
		var imgwrap = $('.imgupload'),
			imgInput = $('#image'),
			img = imgwrap.find('img').eq(0),
			preview = imgwrap.find('.preview'); 
		img.on('click', function () {
			imgInput.trigger('click');
		})
		imgInput.on('change', function () {
			var file = this.files[0];
			window.test = this.files;
			if (!/image\/\w+/.test(file.type)) {
				alert('图片必须为文件');
				return false;
			}
			var reader = new FileReader();
			reader.readAsDataURL(file);
			reader.onload = function () {
				$('#upload').show();
				img.hide();
				$('<img src="' + this.result + '" alt=""/>').appendTo(preview);
				var imgpreview = preview.find('img');
				imgpreview.cropbox({
					width: 300,
					height: 200,
					zoom: 3,
					result: {
						cropX: 0,
						cropY: 0,
						cropW: 300,
						cropH: 200
					}
				}).parent().find('button').on('click', function () {
					return false;
				}).end().end().on('cropbox', function () {
				})
			}
		})
		$('#upload').on('click', function () {
			var data = $(imgpreview.data('cropbox').getDataURL);
			$.post('/api/image').success(function (data) {
				var id = data.id,
					url = data.url;
				img.attr({
					width: 200,
					height: 300,
					src: url
				})
				$('imageId').val(id);
				imageInput.val(id);
			})
		})
		$('#submit').on('click', function () {
			email = $('#email').val();
			var data = form.serialize();
			$.ajax({
				type: 'post',
				url: '?next=/accounts/register',
				data: data,
			}).success(function (data) {
				submit.hide();
				nextaction();
				$('.success a').text(email);
				$('<button class="btn bg-green-light" type="button"><a href="' +
					data.direct_url + '" class="white">去邮箱</a></button>')
				.appendTo(submit.parent()).siblings().hide();
			})
			return false;
		})
	})
})