'use strict';
require(['base'], function (base) {
	var $ = base.$;
	$(document).ready(function () {
		// add tag
		var addTag = $('.js-add-tag'),
			tagList = $('.project-tag'),
			func = function () {
				var $this = $(this);
				$this.html('<div style="min-width:40px;outline-width:0" contentEditable="true"></div>');
				$this.find('div').focus().on('keypress', function (event) {
					$(this).on('blur', function () {
						$this.html('添加+');
					})
					if (event.keyCode === 13) {
						var text = $this.text(),
							origValue = $('#project-tag').val();
						origValue = origValue.slice(-1) === ',' ? origValue.slice(0, -1) : origValue;
						$('<li class="left"><div class="mr-12 bg-green-light relative white">' + 
							text +
							'<span class="absolute project-tag-del">×</span></div></li>').appendTo(tagList);
						$('#project-tag').val(origValue + ',' + text);
						$this.html('添加+');
						$this.parent().appendTo(tagList);
						return false;
					}
				})
				addTag.one('click', func)
			}
		addTag.one('click', func)

		jQuery.extend(jQuery.validator.messages, {
			required: '必选字段',
			remote: '请修正该字段',
			email: '请输入正确格式的电子邮件',
			equalTo: '两次密码不一致',
			accept: '请输入拥有合法后缀名的字符串',
		});
		// sign content
		var previous = $('#previous'),
			next = $('#next'),
			skip = $('#skip'),
			submit = $('#submit'),
			status = 0,
			headerList = $('.js-sign-header').find('li:has(a)'),
			contentList = $('.js-sign-content').children(),
			form = $('#create'),
			agreement = $('#agreement');
		agreement.on('change', function () {$()
			next.prop('disabled', !$(this).prop('checked'));
		})
		previous.on('click', function () {
			if (status === 2) {
				skip.hide();
				submit.hide();
				next.show();
			}
			$(headerList[status]).removeClass('active');
			$(headerList[status - 1]).removeClass('done').addClass('active');
			$(contentList[status]).fadeOut();
			$(contentList[status - 1]).fadeIn();
			status -= 1;
			previous.prop('disabled', false);
			next.prop('disabled', false);
		})
		next.on('click', function () {
			if (status === 1) {
				'project-name, project-location, project-time, project-img, project-tag'
				form.validate({
					rules: {
						'project-name': 'required',
						'project-location': 'required',
						'project-time': 'required',
					},
					ignore: 'project-img'
				})
				if (!form.valid()) {
					return;
				}
				skip.show();
				submit.show();
				next.hide();
			} else if (status === 2) {
				return 
			}
			$(headerList[status]).removeClass('active').addClass('done');
			$(headerList[status + 1]).addClass('active');
			$(contentList[status]).fadeOut();
			$(contentList[status + 1]).fadeIn();
			status += 1;
			previous.prop('disabled', false);
			next.prop('disabled', false);
		})

		// location
		var province = $('#province'),
		city = $('#city'),
		vacant = $('<option value=""></option>');

		// ** $.getJSON('api/location/province').success(function (data) {
		$.getJSON('js/province.json').success(function (data) {
			var provinceHtml = '';
			for (var i = 0, len = data.length; i < len; i = i + 1) {
				provinceHtml += '<option value="' + data[i].id +'">' + data[i].name + '</option>';
			}
			province.append(vacant).append(provinceHtml);
		})
		province.on('change', function () {
			vacant.remove();
			// ** $.getJSON('api/location/city/' + province.val()).success(function (data) {
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
	})
})