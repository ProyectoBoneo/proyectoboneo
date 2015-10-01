function open_modal_observaciones(observaciones_boton, observaciones_input){
    var observaciones = $(observaciones_input).val();
    var modal = $("#observaciones_modal");
    var observaciones_modal_input = $("#observaciones_modal_input");
    $(observaciones_modal_input).val(observaciones);

    var boton_cancelar = $("#observaciones_modal_cancel");
    var boton_confirmar = $("#observaciones_modal_confirm");

    $(boton_cancelar).off("click");
    $(boton_confirmar).off("click");

    $(boton_cancelar).click(function(){
        $(modal).modal('hide');
    });
    $(boton_confirmar).click(function(){
        $(observaciones_input.val($(observaciones_modal_input).val()));
        set_observaciones_button_class(observaciones_boton, observaciones_input);
        $(modal).modal('hide');
    });
    $(modal).modal('show');
}

function set_observaciones_button_class(observacion_button, input_observaciones){
    if($(input_observaciones).val().trim() != "") {
        $(observacion_button).addClass("has");
    }else{
        $(observacion_button).removeClass("has");
    }
}