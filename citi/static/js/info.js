'use strict';
require(['base'], function (base) {
	var $ = base.$;
	$(document).ready(function () {
		$('.pop-up .modal-close').on('click', function () {
			$('.pop-up').slideUp();
		})
	})
})