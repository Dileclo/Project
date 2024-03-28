$(".open_person").click(function () {
    var myModal = new bootstrap.Modal(document.getElementById('Person'), {
        keyboard: false
    })
    myModal.show()
})

$("#add_person").on("submit",function(e){
    e.preventDefault()
    var data = {
        'fio':$("#person_fio").val(),
        'person_dolzhnost':$("#person_dolzhnost").val(),
        'person_org':$('#person_org').select2("data")[0]['inn'],
        'prikaz':$("#prikaz").val(),
        'person_licence':$('#person_licence').val()
    }
    $.ajax({
        url : '/add_person',
        type:'post',
        data:data,
        success: function (data){
            toastr.info(data)
            $("#Person").modal("toggle")
        }
    })
})