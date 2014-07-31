'use strict';
require(['base', 'lib/jquery.cropbox'], function (base) {
	var $ = base.$;
	$(document).ready(function () {
		$('.nav-link').hover(
			function () {
				$(this).addClass('active');

			},
			function () {
				$(this).removeClass('active');
			}
		)
	})
})