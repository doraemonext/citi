'use strict';
require.config({
	baseUrl: 'js/lib',
	paths: {
		'jquery': 'jquery-1.11.1.min',
		'jquery.fontavailable': 'jquery.fontavailable-1.1.min',
		'jquery.validate': 'jquery.validte.min'
	},
	shim: {
		'jquery.validate': ['jquery'],
		'jquery.fontavailable': ['jquery']
	}
})
require(['jquery', 'jquery.fontavailable', '../slider'], function ($, _, slider) {
	$(document).ready(function () {
		($.fontAvailable('microsoft yahei') && $.fontAvailable('youyuan')) ?
			$('<link>')
				.attr({
					rel: 'stylesheet',
					href: 'css/font.css'
				})
				.appendTo('head') :
				$('body');
		console.log($.fontAvailable('microsoft yahei'));

		// slider init
		window.Slider = new slider.Slider(['img/test1.jpg', 'img/test2.jpg', 'img/test3.jpg', 'img/test4.jpg'], {
						width: 980,
						height: 400,
						interval: 3000,
						speed: 600
					})

		// change multi-line words into ... when overflow
		var textOverflow = function (elem, height) {
			elem = elem.jquery ? elem : $(elem);
			while (elem.height() >= height) {
				elem.text(elem.text().slice(0, -1));
			}
			elem.text(elem.text().slice(0, -3) + '...')
		}
		textOverflow($('.tab-content .active .js-text-overflow'), 100);
		
		// tab
		$('#project-single-tab a').on('click', function () {
			var $this = $(this),
				tabName = $this.attr('href'),
				tabContent = $(tabName),
				tabTriangle = $this.parents('ul').find('.js-tab-triangle');
			$this.parent().siblings().removeClass('active').end().addClass('active').append(tabTriangle);
			tabContent.siblings().removeClass('active').end().addClass('active');
			textOverflow(tabContent.find('.js-text-overflow'), 100);
			return false;
		})

		// notify
		$('header .modal-close').on('click', function () {
			$('header').addClass('js-close-notify');
		})
		// modal init
		$('.modal').on('click', function () {
			var target = $(event.target);
			if (target.hasClass('modal-close') ||
				target.hasClass('modal')) {
				$(this).fadeOut();
				$('.modal-backdrop').fadeOut();
			}
		})

		// login
		$('.user').on('click', function () {
			$('.login').fadeIn();
			$('.modal-backdrop').fadeIn();
		})

		// sign content
		var previous = $('#previous'),
			next = $('#next'),
			status = 0,
			headerList = $('.js-sign-header').find('li:has(a)'),
			contentList = $('.js-sign-content').children();
		$('.js-scroll').on('scroll', function () {
			var $this = $(this),
				scrollTop = $this.scrollTop(),
				innerHeight = $this.height(),
				outerHeight = $this.find('.js-scroll-wrap').height(),
				agreement = $('#agreement');
			if (1 || scrollTop + innerHeight >= outerHeight) {
				agreement.prop('disabled', false);
				agreement.on('change', function () {
					next.prop('disabled', !$(this).prop('checked'));
				})
			}
		})
		previous.on('click', function () {
			if (status > 0) {
				$(headerList[status]).removeClass('active');
				$(headerList[status - 1]).removeClass('done').addClass('active');
				$(contentList[status]).fadeOut();
				$(contentList[status - 1]).fadeIn();
				status -= 1;
			}
			previous.prop('disabled', false);
			next.prop('disabled', false);
		})
		next.on('click', function () {
			if (status < 2) {
				$(headerList[status]).removeClass('active').addClass('done');
				$(headerList[status + 1]).addClass('active');
				$(contentList[status]).fadeOut();
				$(contentList[status + 1]).fadeIn();
				status += 1;
			}
			previous.prop('disabled', false);
			next.prop('disabled', false);
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
	})
})