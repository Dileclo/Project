$(document).ready(function () {
    $('.Org_select').select2({
        theme: "bootstrap-5",
        dropdownParent: $("#Object"),
        ajax: {
            url: "/objects",
            type: "GET",
            dataType: 'json',
            processResults: function (data) {
                console.log(data)
                return {

                    results: $.map(data, function (item) {
                        return {
                            text: item.text,
                            id: item.id,
                            inn: item.inn
                        }
                    })
                }
            }
        }
    });
    $("#TableObjects").DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/ru.json',
        },
        "processing": true,
        ajax: {
            url: "/aocr",
            type: "GET",
            dataSrc: '',
            
        },
        columns: [
            { data: "name" }        ]

    });
})

function add_object() {
    var myModal = new bootstrap.Modal(document.getElementById('Object'), {
        keyboard: false
    })
    myModal.show()
}

$("#add_object").on("submit", function (e) {
    e.preventDefault();
    var data = {
        'name':$("#name_obj").val(),
        'address':$("#name_obj").val(),
        'zastroyshik':$('.Org_select#zastroyshik').select2("data")[0]['inn'],
        'lico_os_str':$('.Org_select#lico_os_str').select2("data")[0]['inn'],
        'lico_os_proekt':$('.Org_select#lico_os_proekt').select2("data")[0]['inn']
    }
    console.log(data)
    $.ajax({
        url: "/add_object",
        type: "POST",
        data: data,
        success: function (e) {
            toastr.info(e)
            $('#Object').modal('toggle');
            $("#TableObjects").DataTable().ajax.reload()
        }
    })
})
