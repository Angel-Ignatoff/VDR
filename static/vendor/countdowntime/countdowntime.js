(function($) {
  'use strict';

  function getTimeRemaining(endtime) {
    const total = Date.parse(endtime) - Date.now();
    const seconds = Math.floor((total / 1000) % 60);
    const minutes = Math.floor((total / 1000 / 60) % 60);
    const hours = Math.floor((total / (1000 * 60 * 60)) % 24);
    const days = Math.floor(total / (1000 * 60 * 60 * 24));

    return {
      total,
      days,
      hours,
      minutes,
      seconds,
    };
  }

  function initializeClock(id, endtime) {
    const clock = $(`#${id}`);
    const daysSpan = clock.find('.days');
    const hoursSpan = clock.find('.hours');
    const minutesSpan = clock.find('.minutes');
    const secondsSpan = clock.find('.seconds');

    function updateClock() {
      const time = getTimeRemaining(endtime);

      daysSpan.text(time.days);
      hoursSpan.text(`0${time.hours}`.slice(-2));
      minutesSpan.text(`0${time.minutes}`.slice(-2));
      secondsSpan.text(`0${time.seconds}`.slice(-2));

      if (time.total <= 0) {
        clearInterval(timeinterval);
      }
    }

    updateClock();
    const timeinterval = setInterval(updateClock, 1000);
  }

  const deadline = new Date(Date.now() + 25 * 24 * 60 * 60 * 1000 + 13 * 60 * 60 * 1000);
  initializeClock('clockdiv', deadline);
})(jQuery);
