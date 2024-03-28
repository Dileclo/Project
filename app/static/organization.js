$(document).ready(function() {
var table = new DataTable('#myTable', {

    language: {

        url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/ru.json',
    },
    "processing": true,
    searching: true,
    "ajax": {
        "url": "/organization",
        "type": "GET",
        dataSrc: '',
    },
    "columns": [
        { data: "name" },
        { data: "inn" }
    ]
});
})


$('.open').click(function () {

    var myModal = new bootstrap.Modal(document.getElementById('modalAdd'), {
        keyboard: false
    })
    myModal.show()

})
//ЗАПОЛНИТЬ ПО ИНН
$("#by_inn").click(function () {

    var inn = $("#inn").val();
    inn = { 'inn': inn }
    if (inn.length != 0) {
        $.ajax({
            type: "POST",
            url: "/by_inn",
            data: inn,
            success: function (data) {
                $("#inn_error").hide()
                $("#inn").removeClass("is-invalid")
                $("#name_org").val(data['name'])
                $("#ogrn").val(data['ogrn'])
                $("#kpp").val(data['kpp'])
                $("#address").val(data['address'])
            },
            error: function (error) {
                $("#inn").addClass("is-invalid")
                $("#inn_error").show()
            }

        })
    }
})

$('#closeAdd').click(function (e) {
    $("#modalAdd").removeClass("in");
})

//ДОБАВИТЬ ОРГАНИЗАЦИЮ
$("#addOrg").on("submit", function (e) {
    e.preventDefault();
    var data = {
        "name": $("#name_org").val(),
        "inn": $("#inn").val(),
        "ogrn": $("#ogrn").val(),
        "kpp": $("#kpp").val(),
        "address": $("#address").val(),
        "svvoreg": $("#svvoreg").val(),
        "licence": $("#licence").val(),
        "SRO": $("#SRO").val(),
        "type": $('#type :selected').text()
    }
    $.ajax({
        type: "POST",
        url: "/add_organization",
        data: data,
        success: function (date) {
            $('#modalAdd').modal('toggle');
            $('#myTable').DataTable().ajax.reload()
            toastr.info(date)

        }
    })
})
//ИЗМЕНИТЬ ОРГАНИЗАЦИЮ organization_view
$("#change").click(function (e) {
    var data = {
        "name": $("#name_org").val(),
        "inn": $("#inn").val(),
        "ogrn": $("#ogrn").val(),
        "kpp": $("#kpp").val(),
        "address": $("#address").val(),
        "svvoreg": $("#svvoreg").val(),
        "licence": $("#licence").val(),
        "SRO": $("#SRO").val(),
        "type": $('#type :selected').text()
    }
    $.ajax({
        type: "POST",
        url: "/change_organization",
        data: data,
        success: function (data) {
            toastr.info(data)

        }
    })
})
//УДАЛИТЬ ОРГАНИЗАЦИЮ organization_view
$("#delete").click(function (e) {
    var data = { "inn": $("#inn").val() }
    $.ajax({
        type: "POST",
        url: "/delete_organization",
        data: data,
        success: function (data) {
            window.location = "/organization"

        }
    })
})
