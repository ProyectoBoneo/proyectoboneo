function deleteFormInscripciones(row_element, prefix) {
    var new_row = null;
    var row;
    if($(row_element).hasClass('dynamic-form')){
        row = row_element;
    }else {
        row = $(row_element).parents('.dynamic-form');
    }
    if(!$(row).hasClass("deleted_row")) {
        var container = $(row).parents("table");
        var rows = $(container).find(".dynamic-form:not('.deleted_row')");
        $(row).prop("hidden", true);
        $(row).addClass("deleted_row");
        var delete_input = $(row).find("input[id*='DELETE']");
        $(delete_input).prop("checked", true);
        $(delete_input).val("on");
    }
    return new_row;
}

var InscripcionesController = function(){
    var self = this;
    self.formset_prefix = 'form';

    $('.delete-row').click(function() {
         deleteFormInscripciones(this);
    })
};




InscripcionesController.prototype.reset_row_status = function(row){
    renumber_lines($("#id_forms_table"));
};
