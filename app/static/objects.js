$(document).ready(function () {
    $("#TableWorks").DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/ru.json',
        },
        "processing": true,
        ajax: {
            url: window.location.href,
            type: "GET",
            dataSrc: '',
            
        },
        columns: [
            { data: "name" }]

    });
})

function add_work(){
    var myModal = new bootstrap.Modal(document.getElementById('AddWork'), {
        keyboard: false
    })
    myModal.show()
}

$("#addWork").on("submit", function (e) {
    e.preventDefault();
    $.ajax({
        url:"/addWork",
        type: "POST",
        data:{"name_work":$("#name_work").val(),"name_org":$("#name_org").text()},
        success: function (data){
            toastr.info(data)
            $("#TableWorks").DataTable().ajax.reload()
            $("#AddWork").modal("toggle")
        }
    })
})