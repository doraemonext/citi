'use strict';
require(['jquery', 'jquery.cropbox', 'app/form'], function ($) {
	$(document).ready(function () {
		
		// sign content
		var form = $('#sign'),
			submit = $('#submit'),
			skip = $('#skip'),
			email,
			isIgnored = true,
			rules = {
				email: {
					email: true,
					required: true
				},
				password1: 'required',
				password2: {
					required: true,
					equalTo: '#password'
				},
				// nickname: 'required',
				// 'native': 'required',
				// occupation: 'required',
			};

		// form validate
		form.validate({
			rules: rules,
			messages: {
				idcard_image: '请上传证件照'
			}
		})

		// form to skip
		$('.js-sign-content > div').eq(2).on('change', function () {
			var formItem = $(this).find('input, select').not('#image'),
				formItemArray = $.makeArray(formItem),
				result = $.map(formItemArray, function (v) {
					return $(v).val() === '' ? null : true;
				});
			if (isIgnored === true && result.length > 0) {
				formItem.each(function () {
					$(this).rules('add', {
						required: true
					})
				})
				isIgnored = false;
			} else if (result.length === 0 && isIgnored === false) {
				formItem.each(function () {
					$(this).rules('remove');
				})
				isIgnored = true;
				form.valid();
			}
		})

		var imageWrap = $('.imageWrap'),
			imageInput = $('#image'),
			imageTrigger = imageWrap.find('img').eq(0),
			imagePreview = imageWrap.find('.imagePreview'),
			upload = $('#imageUpload'),
			cancel = $('#imageCancel'),
			imageInputFunc = function () {
				var file = this.files[0];
				if (!/image\/\w+/.test(file.type)) {
					alert('文件必须为图片');
					return false;
				}
				var reader = new FileReader();
				reader.readAsDataURL(file);
				reader.onload = function () {
					upload.show();
					cancel.show();
					imageTrigger.hide();
					$('<img src="' + this.result + '" alt=""/>')
					.appendTo(imagePreview)
					.cropbox({
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
					});
				}
			};
		imageTrigger.on('click', function () {
			imageInput.trigger('click');
		})
		imageInput.on('change', imageInputFunc)
		upload.on('click', function () {
			var formdata = new FormData(),
				imgdata = imagePreview.data('cropbox').getBlob(),
				xhr = new XMLHttpRequest(),
				callback = function () {
					var data = $.parseJSON(xhr.responseText);
					if (xhr.readyState === 4) {
						if (xhr.status === 201) {
							img.attr({
								width: 200,
								height: 300, 
								src: data.url
							})
							$('#imageId').val(data.id);
						}
					}
				};
			formdata.append('type', 0);
			formdata.append('image', imgdata);
			xhr.onreadystatechange = callback;
			xhr.open('post', '/api/image/');
			xhr.send(formdata);
			return false;
		})
		cancel.on('click', function () {
			imageInput.replaceWith(imageInput.clone());
			imageInput.on('click', imageInputFunc);
			upload.hide();
			cancel.hide();
			imageTrigger.show();
			imagePreview.find('img').data('cropbox').remove();
			imagePreview.empty();
			return false;
		})
		submit.on('click', function () {
			if (!form.valid()) {
				return false;
			}
			email = $('#email').val();
			var data = form.serialize();
			$.ajax({
				type: 'post',
				url: '/accounts/register/',
				data: data,
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                }
			}).then(
				function (data) {
					submit.hide();
					nextaction();
					$('.success a').text(email);
					$('<button class="btn bg-green-light" type="button"><a href="' +
						data.direct_url + '" class="white">去邮箱</a></button>')
					.appendTo(submit.parent()).siblings().hide();
				},
				function (data) {
					var errorInInfo = $.map(data, function (v, i) {
						return i in rules ? i : null;
					})
					form.validate().showErrors(data);
					if (errorInInfo.length > 0) {
						$('#previous').trigger('click');
					}
				}
			)
			return false;
		})
		skip.on('click', function () {
			submit.trigger('click');
		})
	})
}	)