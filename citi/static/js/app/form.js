'use strict'
require(['jquery'], function ($) {
	// process
	var previous = $('#previous'),
		next = $('#next'),
		skip = $('#skip'),
		submit = $('#submit'),
		status = 0,
		headerList = $('.js-sign-header').find('li:has(a)'),
		contentList = $('.js-sign-content').children(),
		form = $('#sign, #create'),
		agreement = $('#agreement');

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
		if (status > 0) {
			if (!form.valid()) {
				return;
			}
		}
		if (status === 1) {
			skip.show();
			submit.show();
			next.hide();
		}
		nextaction();
	})

	// province & city
	var province = $('#province'),
		city = $('#city'),
		vacant = $('<option value=""></option>');
	$.getJSON('/api/location/province/').success(function (data) {
		var provinceHtml = '';
		for (var i = 0, len = data.length; i < len; i = i + 1) {
			provinceHtml += '<option value="' + data[i].id +'">' + data[i].name + '</option>';
		}
		province.append(vacant).append(provinceHtml);
	})
	province.on('change', function () {
		vacant.remove();

		$.getJSON('/api/location/city/' + province.val() + '/').success(function (data) {
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
