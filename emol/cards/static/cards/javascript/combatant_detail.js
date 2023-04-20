function csrf_token() {
    return $("[name=csrfmiddlewaretoken]").val();
}

function form_loaded() {
    $('#edit-combatant-sca-name').focus();

    // if can edit waiver date -->            
    $("#edit-waiver-date_signed").datepicker({ format: "yyyy-mm-dd", autoclose: true })
        .on('changeDate', function (event) {
            var url = '/api/waiver/' + $('#uuid').val() + "/",
                data = { date_signed: $(this).val() };

            $.ajax({
                url: url,
                method: 'PUT',
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: 'application/json; charset=UTF-8',
                headers: { "X-CSRFToken": csrf_token() },
                success: function (response, status, xhr) {
                    toastr.success("Waiver date updated");
                    $("#edit-waiver-expiration_date").val(xhr.responseJSON.expiration_date);
                },
                error: function (xhr, status, error) {
                    toastr.error("Error updating wavier: " + error);
                },
            });
        });

    // If can update card info
    $(".card-date").datepicker({ format: "yyyy-mm-dd", autoclose: true })
        .on('changeDate', function (event) {
            var discipline = $(this).data("discipline"),
                uuid = $("#uuid").val(),
                url = '/api/card-date/' + uuid + "/",
                data = {
                    date_issued: $(this).val(),
                    uuid: uuid,
                    discipline_slug: discipline,
                };

            $.ajax({
                url: url,
                method: 'PUT',
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: 'application/json; charset=UTF-8',
                headers: { "X-CSRFToken": csrf_token() },
                success: function (response, status, xhr) {
                    toastr.success("Card date updated");
                },
                error: function (xhr, status, error) {
                    toastr.error("Error updating card date: " + error);
                },
            });
        });
};
