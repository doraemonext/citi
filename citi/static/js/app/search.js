'use strict';
require(['jquery'], function ($) {
	$(document).ready(function () {
		$('.search-box').on('click', 'a', function () {
			console.log(this.innerHTML);
			var searchReg = /[?&]?(\w+)\=(\w+)/g,
				currentHref = document.location.href,
				newHref = 'project_list/?',
				searchItem = {},
				result,
				$this = $(this);
			while( (result = searchReg.exec(currentHref)) != null) {
				searchItem[result[1]] = result[2];
			}
			searchItem = $.extend(searchItem, $this.data());
			newHref = /(.*\.html)/.exec(document.location.href)[1] + '?' + $.param(searchItem);
			window.location.href = newHref;
			return false;
		})
		// $('.js-diy').on('click', function () {
		// 	$('.change-location').fadeIn();
		// })
		// $('.change-location .modal-close').on('click', function () {
		// 	$('.change-location').fadeOut();
		// })
	})
})