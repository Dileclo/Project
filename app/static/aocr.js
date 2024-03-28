$(document).ready(function () {
    
    
    
    $("#TableAOCR").DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/ru.json',
        },
        buttons: [
            'copy', 'excel', 'pdf'
        ],
        scrollX: true,
        "processing": true,
        ajax: {
            url: window.location.href,
            type: "GET",
            dataSrc: '',

        },
        columns: [
            { data: "name" },
            { data: "work" },
            { data: "start_date" },
            { data: "end_date" },
            { data: "next_work" },
        ]

    });
})

function add_aocr() {
    var myModal = new bootstrap.Modal(document.getElementById('AOCR'), {
        keyboard: false
    })
    myModal.show()
}
$("#add_aocr").on("submit", function (e) {
    e.preventDefault();
    var materials = []
    var pred_teh_zak = []

    var pred_str = []
    var pred_str_control = []
    var pred_proekt = []
    var pred_vip_rab = []
    var inie = []

    $.each($("#materials").select2("data"),function(key,value){
        materials.push(JSON.stringify({'name':value['text'],'doc':value['doc']}))
    })
    $.each($("#pred_teh_zak").select2("data"),function(key,value){
        pred_teh_zak.push(JSON.stringify({'name':value['text'],'dolzhnost':value['dolzhnost']}))
    })
    
    $.each($("#pred_str").select2("data"),function(key,value){
        pred_str.push(JSON.stringify({'name':value['text'],'dolzhnost':value['dolzhnost']}))
    })
    $.each($("#pred_str_control").select2("data"),function(key,value){
        pred_str_control.push(JSON.stringify({'name':value['text'],'dolzhnost':value['dolzhnost']}))
    })
    $.each($("#pred_proekt").select2("data"),function(key,value){
        pred_proekt.push(JSON.stringify({'name':value['text'],'dolzhnost':value['dolzhnost']}))
    })
    $.each($("#pred_vip_rab").select2("data"),function(key,value){
        pred_vip_rab.push(JSON.stringify({'name':value['text'],'dolzhnost':value['dolzhnost']}))
    })
    $.each($("#inie").select2("data"),function(key,value){
        inie.push(JSON.stringify({'name':value['text'],'dolzhnost':value['dolzhnost']}))
    })
    var data = {
        "name_work":$("#name_worka").text(),
        "lico_vip_work": $('.Org_select#lico_vip_work').select2("data")[0]['inn'],
        "num_act":$("#num_act").val(),
        "start_date":$("#start_date").val(),
        "end_date":$("#start_date").val(),
        "end_date":$("#start_date").val(),
        "pred_teh_zak":pred_teh_zak,
        "pred_str":pred_str,
        'pred_str_control':pred_str_control,
        'pred_proekt':pred_proekt,
        'pred_vip_rab':pred_vip_rab,
        'inie':inie,
        'work':$("#work").val(),
        'project':$("#project").val(),
        'materials':materials,
        'isp_scheme':$("#isp_scheme").val(),
        'reglaments':$("#reglaments").val(),
        'next_work':$("#next_work").val(),
        "name_object":$("#name_orga").text()
    }
    console.log(data)
    $.ajax({
        url:"/add_aocr",
        type:"post",
        data:data,
        success:function(e){
            toastr.info(e)
            $("#AOCR").modal("toggle")
        }
    })
})
