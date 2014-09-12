'use strict';
define(['jquery'], function() {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    var ImageUpload = function(data) {
		// data = {input, readTrigger, uploadTrigger, cancel, imagePreview, url, imageModify, callbacks, uploadOnRead}
		var that = this,
			url = data.url,
			imageRead = function() {
				if (data.imageRead) {
					data.imageRead.call(that);
				}
				if (data.uploadOnRead) {
					that.createFileReader(imageModify, imageUpload);
				} else {
					that.createFileReader(imageModify);
				}
				return false;
			},
			imageModify = function() {
				if (data.imageModify) {
					data.imageModify.call(that);
				}
				return false;
			},
			imageUpload = function(file) {
                if (data.imageUpload) {
                    data.imageUpload.call(that);
                }
				that.upload(data.data, data.callbacks, url, file);
				return false;
			},
			imageCancel = function() {
				data.cancel.call(that);
				var temp = that.input.clone();
				that.input.replaceWith(temp);
				that.input = temp;
				that.input.on('change', imageRead);
				that.imagePreview.empty();
				return false;
			},
			callbacks = data.callbacks;
		this.uploadOnRead = data.uploadOnRead;
		this.input = $(data.input);
		this.readTrigger = $(data.readTrigger);
		this.uploadTrigger = $(data.uploadTrigger);
		this.imagePreview = $(data.imagePreview);
		this.cancelTrigger = $(data.cancelTrigger);

		this.readTrigger.on('click', function() {
			that.input.trigger('click');
			return false
		});
		this.input.on('change', imageRead);
		this.uploadTrigger.on('click', imageUpload);
		this.cancelTrigger.on('click', imageCancel);
	};
	ImageUpload.prototype = {
		constructor: ImageUpload,
		createImagePreview: function(src) {
			this.imagePreview.append('<img src="' + src + '" alt=""/>')
		},
		createFileReader: function(imageModify, imageUpload) {
			var file = this.input[0].files[0],
				that = this;
			if (!/image\/\w+/.test(file.type)) {
				alert('文件必须为图片');
				return false;
			}
			var reader = new FileReader();
			reader.readAsDataURL(file);
			reader.onload = function() {
				that.createImagePreview(this.result);
				if (that.uploadOnRead) {
					imageUpload(file);
				} else {
					imageModify();
				}
			};
		},
		createXMLHttpRequest: (function() {
			if (window.ActiveObject) {
				return function() {
					return new ActiveObject('Microsoft.XMLHTTP');
				}
			} else if (window.XMLHttpRequest) {
				return function() {
					return new XMLHttpRequest();
				}
			}
		})(),
		createFormData: function(data, file) {
			var that = this,
				formData = new FormData();
			$.each(data, function(i, v) {
				if ($.type(v) === 'function') {
					formData.append(i, v.call(that));
				}
				formData.append(i, v);
			})
			return formData;
		},
		upload: function(data, callbacks, url, file) {
			var that = this,
				xhr = this.createXMLHttpRequest(),
				formData = this.createFormData(data),
				callback = function() {
					window.response = xhr;
					if (xhr.readyState === 1) {
						if (!csrfSafeMethod('post') && !(url.indexOf('http') !== -1)) {
							xhr.setRequestHeader('X-CSRFToken', csrftoken);
						}
					} else if (xhr.readyState === 4) {
                        var response = $.parseJSON(xhr.responseText);
						$.each(callbacks, function(i, v) {
							if (xhr.status === parseInt(i)) {
								v.call(that, response);
							}
						})
					}
				};
			if (typeof file !== 'undefined') {
				formData.append('image', file);
			}
			xhr.onreadystatechange = callback;
			xhr.open('post', url);
			xhr.send(formData);
		}
	}
	return {
		ImageUpload: ImageUpload
	}
})
