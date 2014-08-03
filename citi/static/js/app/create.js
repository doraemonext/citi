'use strict';
require(['jquery'], function ($) {
	$(document).ready(function () {
		// add tag
		var addTag = $('.js-add-tag'),
			tagList = $('.project-tag'),
			func = function () {
				var $this = $(this);
				$this.html('<div style="min-width:40px;outline-width:0" contentEditable="true"></div>');
				$this.find('div').focus()
				.on('blur', function () {
					$(this).html('添加+')
				})
				.on('keypress', function (event) {
					if (event.keyCode === 13) {
						var text = $this.text(),
							origValue = $('#project-tag').val(),
							newLi = $('<li class="left"><div class="mr-12 bg-green-light relative white">' + 
							text +
							'<span class="absolute project-tag-del js-tag-del">×</span></div></li>');
						newLi.appendTo(tagList);
						newLi.find('span').one('click', function () {
							var input = $('#project-tag'),
								valueToDel = $(this).parent().text().slice(0, -1),
								value = input.val();
							value = value.replace(valueToDel + ',', '');
							value = value.replace(',' + valueToDel, '');
							$(this).parents('li').remove();
							input.val(value);
							console.log($('#project-tag').val());
						})
						origValue += origValue.length === 0 ? text : (origValue.slice(-1) === ',' ? text : ',' + text);
						$('#project-tag').val(origValue);
						console.log($('#project-tag').val());
						$this.html('添加+');
						$this.parent().appendTo(tagList);
						
						return false;
					}
				})
				addTag.one('click', func)
			}
		addTag.one('click', func);
		
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

		$('.js-add-scheme, .js-add-reward').on('click', function () {
			var $this = $(this),
				reward = $('<div class="panel"><div class="panel-header relative"><div class="close absolute" data-dismiss="panel">×</div><h4>回报</h4></div><div class="panel-body"><div><label class="mr-12 green left" for="reward-desc">回报描述:</label><input type="text" id="reward-desc" name="reward-desc" class="input"></div><div><label class="mr-12 green left" for="reward-pic">回报图片:</label><input type="file" id="reward-pic" name="reward-pic" class="input"><button type="text" class="btn bg-green-light white">上传</button></div></div></div>') }),
				scheme;
	})
})