$(function (){
    var comunicados_link = $("#comunicados");
    var comunicados_endpoint = "/aula_virtual/comunicados/pendientes/";
    $.get(comunicados_endpoint, function (data){
       if (data.comunicados_no_leidos) {
           var notification = document.createElement('span');
           $(notification).toggleClass('notification-comunicados');
           $(notification).html(data.comunicados_no_leidos);
           $(comunicados_link).append(notification);
       }
    });
});