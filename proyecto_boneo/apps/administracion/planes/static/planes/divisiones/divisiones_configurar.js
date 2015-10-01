var DivisionesConfigurarController = function(){
    var self = this;
    $("#id_cantidad_anios").change(function(){
        self.arrange_divisiones(parseInt($(this).val()));
    });
};

DivisionesConfigurarController.prototype.arrange_divisiones = function(years){
    var table = $("#forms_table");
    var body = $(table).find("tbody");
    var filas =  $(body).find("tr:not('.deleted_row')");
    var longitud_actual = $(filas).length;
    if (longitud_actual > years){
        $(filas).filter(function(){return parseInt($(this).find(".line_number").html()) > years}).each(
            function(idx, element){
               deleteForm(element, 'form');
            });
    }
    else{
        var forms_faltantes = years - longitud_actual;
        for(var i = 1; i <= forms_faltantes; i++){
            var row = addForm(body, 'form');
            $(row).find("[id$='-cantidad_divisiones']").val('1');
        }
    }
    renumber_lines(table);
    filas =  $(body).find("tr");
    $(filas).each(function(idx, element){
        var line_number = $(element).find(".line_number").html();
        $(element).find("[id$='-anio']").val(line_number);
    });
};
