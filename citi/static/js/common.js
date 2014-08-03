require.config({
	baseUrl: '/static/js/lib',
	paths: {
		app: '../app',
		jquery: 'jquery-1.11.1.min',
		'jquery.fontavailable': 'jquery.fontavailable-1.1.min',
		'jquery.validate': 'jquery.validate.min',
	},
	shim: {
		'jquery.cropbox': {
			deps: ['jquery'],
			exports: 'jQuery.fn.cropbox'
		},
		'jquery.validate': {
			deps: ['jquery'],
			exports: 'jQuery.fn.validate'
		},
		'jquery.fontavailable': {
			deps: ['jquery'],
			exports: 'jQuery.fontAvailable'
		},
		'jquery.form': {
			deps: ['jquery'],
			exports: 'jQuery.fn.form'
		}
	}
})

require(['jquery', 'jquery.validate'], function ($) {
	$(document).ready(function () {
		/*($.fontAvailable('microsoft yahei') && $.fontAvailable('youyuan')) ?
		$('<link>')
		.attr({
			rel: 'stylesheet',
			href: 'css/font.css'
		})
		.appendTo('head') :
		$('body');
		console.log($.fontAvailable('microsoft yahei'));*/

		// open & close for modal & tab
		var animate = function (isToggle, targetElem, dismissAnimate, diff, elem) {
			var animation,
				isCustom;
			if (typeof dismissAnimate !== 'undefined') {
				isCustom = false;
				if (dismissAnimate.indexOf('slide') !== -1) {
					animation = isToggle ? 'slideDown' : 'slideUp';
				} else if (dismissAnimate.indexOf('fade') !== -1) {
					animation = isToggle ? 'fadeIn' : 'fadeOut';
				}
			} else {
				isCustom = true;
				animation = isToggle ? 'addClass' : 'removeClass';
			}
			if (diff !== 'tab') {
				if (!isCustom) {
					targetElem[animation]();
				}
				targetElem[animation]('active');
			} else {
				$(elem).parent().siblings().removeClass('active').end().addClass('active');
				targetElem.siblings().removeClass('active').end().addClass('active');
			}
			if (diff === 'modal') {
				isToggle ? $('.modal-backdrop').fadeIn() : $('.modal-backdrop').fadeOut();
			}
		};

		var moduleSetup = function (elem) {
			var elem = elem.jquery ? elem : $(elem),
				data = elem.data(),
				isToggle = 'toggle' in data,
				diff = data.toggle || data.dismiss,
				target, targetElem, isModal, dismissAnimate;
			if (diff === 'tab') {
				target = elem.attr('href');
			} else if (isToggle)  {
				target = elem.data('target');
			} else if (!isToggle) {
				target = elem.data('dismiss');
			}
			targetElem = isToggle ? $(target) : elem.parents('.' + target);
			dismissAnimate = targetElem.data('animate');

			return {
				isToggle: isToggle,
				diff: diff,
				targetElem: targetElem,
				dismissAnimate: dismissAnimate
			}
		}

		$('[data-dismiss], [data-toggle]').on('click', function () {
			var result = moduleSetup(this);
			animate(result.isToggle, result.targetElem, result.dismissAnimate, result.diff, this);
			return false;
		})

		$('.modal').on('click', function (event) {
			var target = $(event.target);
			if (target.hasClass('modal-close') || target.hasClass('modal')) {
				animate(false, $(this), $(this).data('animate'), 'modal')
			}
		})

		// load svg
		var svgToLoad = ['share', 'download', 'go-to-top', 'search-icon', 'user', 'feedback', 'qqzone', 'renren', 'douban', 'sina', 'logo'];
		$.each(svgToLoad, function (i, v) {
			$('.' + v).load('/static/img/' + v + '.svg')
		})
		$('.position').each(function () {
			$(this).prepend('<em class="position-icon"></em>').find('.position-icon').load('img/position.svg');
		})

		// search icon
		$('.search-icon').on('mouseover', function () {
			$(this).parent().addClass('active').find('.search-icon').end().find('.input-search').trigger('focus');
			$(this).siblings().one('blur', function () {
				$(this).parent().removeClass('active').find('.search-icon');
			})
		})

		// toolbar
		$(window).on('scroll', function () {
			var goToTop = $('.go-to-top').parent();
			$(this).scrollTop() >= 1000 ? goToTop.removeClass('hide') : goToTop.addClass('hide');
		})
		$('.go-to-top').parent().on('click' ,function () {
			$(document.body).animate({scrollTop: 0})
		})

		// fix the problem of the modal animation in chrome
		$('.modal').show();

		// extend jQuery
		$.fn.extend({
			textOverflow: function (maxHeight) {
				var origHeight = this.height();
				while (this.height() >= maxHeight) {
					this.text(this.text().slice(0, -1));
				}
				origHeight >= maxHeight && this.text(this.text().slice(0, -3) + '...');
			}
		})
		$('.tab-content .active .js-text-overflow').textOverflow(100);

		$.extend($.validator.messages, {
			required: '必选字段',
			remote: '请修正该字段',
			email: '请输入正确格式的电子邮件',
			equalTo: '两次密码不一致',
			accept: '请输入拥有合法后缀名的字符串'
		});
	})
})