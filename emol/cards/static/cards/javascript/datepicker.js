/*Enable datepicker controls on any fields with the class datepicker*/
(function ($) {
    "use strict";

    $(document).ready(function () {
        $(".datepicker").datepicker({ format: "yyyy-mm-dd", autoclose: true });
    })
})(jQuery);
