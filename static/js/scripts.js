$(function() {

    const $smartScroll = $('.smart-scroll');
    const $scrollTop = $('.scroll-top');
    const $pageScroll = $('a.page-scroll');
    const $colorSwitcher = $('.color-switcher ul li');
    const $themeColor = $('#theme-color');
    const $switcherWrap = $('.switcher-wrap');
    const slickAboutSettings = {
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        dots: true,
        arrows: false
    };

    feather.replace();

    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="popover"]').popover();

    $pageScroll.on('click', function(event) {
        const $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top - 20
        }, 1000);
        event.preventDefault();
    });

    $('.slick-about').slick(slickAboutSettings);

    let scrollTop = 0;
    $(window).scroll(function() {
        const scroll = $(window).scrollTop();
        if (scroll > 80) {
            if (scroll > scrollTop) {
                $smartScroll.addClass('scrolling').removeClass('up');
            } else {
                $smartScroll.addClass('up');
            }
        } else {
            $smartScroll.removeClass('scrolling up');
        }
        scrollTop = scroll;
        $scrollTop.toggleClass('active', scroll >= 600);
    });

    $scrollTop.on('click', function() {
        $('html, body').stop().animate({
            scrollTop: 0
        }, 1000);
    });

    $('.switcher-trigger').click(function() {
        $switcherWrap.toggleClass('active');
    });
    
    $colorSwitcher.click(function() {
        const color = $(this).attr('data-color');
        $themeColor.attr('href', `css/${color}.css`);
        $colorSwitcher.removeClass('active');
        $(this).addClass('active');
    });

});
