$(".open_materials").click(function(){
    var myModal = new bootstrap.Modal(document.getElementById('Materials'), {
        keyboard: false
    })
    myModal.show()
})

$("#addMaterial").on("submit", function (e) {
    e.preventDefault()
    var data = {
        'name_mat': $('#name_mat').val(),
        'type_mat': $('#type_mat').val(),
        'doc_mat': $('#doc_mat').val(),
        'start_mat': $('#start_mat').val(),
        'end_mat': $('#end_mat').val()
    }
    $.ajax({
        url:"/add_materials",
        type:"post",
        data: data,
        success: function (e){
            toastr.info(e)
            $("#Materials").modal("toggle")
        }
    })
})
