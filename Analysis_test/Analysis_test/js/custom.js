$(document).ready(function () {
    var onMobile = false;
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) { onMobile = true; }
    if ((onMobile === false)) {
        $("body").hasClass("nobg");
    } else {
        $("body").removeClass("nobg");
    }
    //Fixed menu - Fix the menu to the top after you scroll past it
    var fixedmenuTop = $('.fixedmenu').offset().top;
    $(window).scroll(function () {
        var currentScroll = $(window).scrollTop();
        if (currentScroll >= fixedmenuTop) {
            $('.fixedmenu').css({
                position: 'fixed',
                top: '0',
                left: '0'
            });
        } else {
            $('.fixedmenu').css({
                position: 'relative'
            });
        }
    });

    /**** Appear JS ****/
    if ($.fn.appear) {
        $('[data-ride="animated"]').appear();
        if (!$('html').hasClass('ie no-ie10')) {
            $('[data-ride="animated"]').addClass('appear');
            $('[data-ride="animated"]').on('appear', function () {
                var $el = $(this), $ani = ($el.data('animation') || 'fadeIn'), $delay;
                if (!$el.hasClass('animated')) {
                    $delay = $el.data('delay') || 0;
                    setTimeout(function () {
                        $el.removeClass('appear').addClass($ani + " animated");
                    }, $delay);
                }
            });
        };
        $('.number-animator').appear();
        $('.number-animator').on('appear', function () {
            $(this).animateNumbers($(this).attr("data-value"), true, parseInt($(this).attr("data-animation-duration")));
        });

        $('.animated-progress-bar').appear();
        $('.animated-progress-bar').on('appear', function () {
            $(this).css('width', '0%').animate({ 'width': $(this).attr("data-percentage") }, 1000);
        });
    }

    /**** Animate Numbers ****/
    if ($.fn.animateNumbers) {
        $('.animate-number').each(function () {
            $(this).animateNumbers($(this).attr("data-value"), true, parseInt($(this).attr("data-animation-duration")));
        })
    }

    //Smooth scrolling - Smooth scroll after clicking an element with the class 'smoothscroll'
    $('.smoothscroll').bind('click.smoothscroll', function (e) {
        e.preventDefault();

        var target = this.hash,
        $target = $(target);

        $('html, body').stop().animate({
            'scrollTop': $target.offset().top - 0
        }, 900, 'swing', function () {
            window.location.hash = target;
        });
        return false;
    });

    $('h1.fittext').fitText(1, { minFontSize: '50px', maxFontSize: '100px' });
    $('h2.fittext').fitText(1, { minFontSize: '40px', maxFontSize: '80px' });
    $('h3.fittext').fitText(1, { minFontSize: '30px', maxFontSize: '60px' });
    $('h4.fittext').fitText(1, { minFontSize: '20px', maxFontSize: '40px' });
    $('h5.fittext').fitText(1, { minFontSize: '15px', maxFontSize: '30px' });
    $('h6.fittext').fitText(1, { minFontSize: '10px', maxFontSize: '20px' });

    //Contact Form
    $('#contactform').submit(function () {

        var action = $(this).attr('action');

        $('#message').slideUp(300, function () {
            $('#message').hide();

            $('#submit')
			.after('<img src="images/status.gif" class="loader">')
			.attr('disabled', 'disabled');

            $.post(action, {
                name: $('#name').val(),
                email: $('#email').val(),
                phone: $('#phone').val(),
                subject: $('#subject').val(),
                comments: $('#comments').val(),
                verify: $('#verify').val()
            },
			function (data) {
			    document.getElementById('message').innerHTML = data;
			    $('#message').slideDown(300);
			    $('#contactform img.loader').fadeOut(300, function () { $(this).remove() });
			    $('#submit').removeAttr('disabled');
			    if (data.match('success') != null) $('#contactform').slideUp(300);
			}
		);

        });

        return false;

    });

    $('#toggle').click(function (e) {
        e.stopPropagation();
    });
    $('html').click(function (e) {
        if (!$('.toggle').is($(e.target))) {
            $('#toggle').prop("checked", false);
        }
    });
    //});


    //$(window).load(function () {

    $('#status').fadeOut(); // will first fade out the loading animation
    $('#preloader').delay(350).fadeOut('slow'); // will fade out the white DIV that covers the website.
    $('body').delay(350).css({ 'overflow-y': 'visible' });

    //FitText
    setTimeout(function () {
        $('h1.fittext').fitText(1, { minFontSize: '50px', maxFontSize: '100px' });
        $('h2.fittext').fitText(1, { minFontSize: '40px', maxFontSize: '80px' });
        $('h3.fittext').fitText(1, { minFontSize: '30px', maxFontSize: '60px' });
        $('h4.fittext').fitText(1, { minFontSize: '20px', maxFontSize: '40px' });
        $('h5.fittext').fitText(1, { minFontSize: '15px', maxFontSize: '30px' });
        $('h6.fittext').fitText(1, { minFontSize: '10px', maxFontSize: '20px' });
    }, 200);

    // Featured work slider
    $('#featured-work-slider').bxSlider({
        auto: false,
        mode: 'fade',
        pager: true,
        controls: true,
        nextText: '',
        prevText: ''
    });

    // Quote slider
    var quoteslider = $('#quote-slider').bxSlider({
        auto: true,
        responsive: true,
        adaptiveHeight: true,
        mode: 'horizontal',
        pager: false,
        controls: false
    });

    $('#quote-next').click(function () {
        quoteslider.goToNextSlide();
        return false;
    });

    $('#quote-prev').click(function () {
        quoteslider.goToPrevSlide();
        return false;
    });
});
