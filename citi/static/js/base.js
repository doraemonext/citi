'use strict';
require.config({
	baseUrl: 'js/lib',
	paths: {
		'jquery': 'jquery-1.11.1.min',
		'jquery.fontavailable': 'jquery.fontavailable-1.1.min',
		'jquery.validate': 'jquery.validate.min'
	},
	shim: {
		'jquery.fontavailable': ['jquery']
	}
})
require(['jquery', 'jquery.fontavailable'], function ($) {
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

		// open & close
		var animate = function (isToggle, targetElem, isModal, dismissAnimate) {
			if (typeof dismissAnimate !== 'undefined') {
				if (dismissAnimate.indexOf('slide') !== -1) {
					isToggle ? targetElem.slideUp() : targetElem.slideDown();
				} else if (dismissAnimate.indexOf('fade') !== -1) {
					isToggle ? targetElem.fadeIn() : targetElem.fadeOut();
				} else {
					targetElem.addClass(dismissAnimate);
				}
			} else {
				isToggle ? targetElem.addClass('active') :
					targetElem.removeClass('active');
			}
			if (isModal) {
				isToggle ? $('.modal-backdrop').fadeIn() : $('.modal-backdrop').fadeOut();
			}
		}
		$('[data-dismiss], [data-toggle]').on('click', function () {
			var $this = $(this),
				data = $this.data(),
				isToggle = 'toggle' in data,
				target = data.toggle || data.dismiss,
				targetElem = isToggle ? $(target) : $this.parents('.' + target),
				isModal = targetElem.hasClass('modal'),
				dismissAnimate = targetElem.data('animate');
			animate(isToggle, targetElem, isModal, dismissAnimate);
			return false;
		})

		$('.modal').on('click', function (event) {
			var target = $(event.target);
			if (target.hasClass('modal-close') || target.hasClass('modal')) {
				animate(false, $(this), true, $(this).data('animate'))
			}
		})

		// load svg
		var svgToLoad = ['logo', 'share', 'download', 'go-to-top', 'search-icon', 'user', 'feedback', 'qqzone', 'renren', 'douban', 'sina'];
		$.each(svgToLoad, function (i, v) {
			$('.' + v).load('img/' + v + '.svg', function () {
			})
		})
		$('.position').each(function () {
			$(this).prepend('<em class="position-icon"></em>').find('.position-icon').load('img/position.svg', function () {
			})
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
	})
})
define(['jquery', 'jquery.validate'], function ($) {
	// form validate
	$('form').validate();

	return {
		$: $,
	}
})
