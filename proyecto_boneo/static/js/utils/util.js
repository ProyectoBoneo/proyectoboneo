var MainController = function(){
    this.configure_dates();
};

MainController.prototype.configure_dates =
function(){
    $.fn.datepicker.dates['es'] = {
        days: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
        daysShort: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
        daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"],
        months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
        monthsShort: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
        today: "Hoy"
    };
};


MainController.prototype.configure_date_controls =
function(){
    var dates = $(".date").filter(function(){return $(this).prop("data-date_configured") != "true";});
    $(dates).datepicker({format:'dd/mm/yyyy', language:'es'}).on('changeDate',
    function(ev) {
        $("div.datepicker").hide();
    });
    $(dates).prop("data-date_configured", "true");
};

MainController.prototype.configure_controls =
function(){
    new TypeaheadController().register_typeaheads();
    this.configure_date_controls();
};

var mainController = new MainController();


function getMainController(){
    return mainController;
}

function append_row(table, row_objects){
    var row = table.insertRow(table.rows.length);
    for(var index = 0; index < row_objects.length; index++){
        var cell = row.insertCell(index);
        var row_object = row_objects[index];
        if (row_object instanceof Array){
            for(var int_index = 0; int_index < row_object.length; int_index++){
                if(typeof row_object[int_index] == "object") {
                    cell.appendChild(row_object[int_index]);
                }
                else{
                    $(cell).html(row_object);
                }
            }
        }else{
            if(typeof row_object == "object"){
                cell.appendChild(row_object);
            }
            else{
                $(cell).html(row_object);
            }
        }
    }
    return row;
}

function newSelect(elements, attr_list){
    attr_list = attr_list || null;
    var select = document.createElement("select");
    select.setAttribute("class", "select form-control");
    for(var index = 0; index < elements.length; index++){
        var option = document.createElement("option");
        option.setAttribute("value", elements[index][0]);
        option.text = elements[index][1];
        select.appendChild(option);
    }
    if (attr_list instanceof Array){
        for(index = 0; index < attr_list.length; index++){
            select.setAttribute(attr_list[index][0], attr_list[index][1]);
        }
    }
    return select;
}

function filter_click(element){
    var form = $(element).parents("form");
    $(form).prop("target", "");
    $(form).find("#id_render_pdf_report").prop("checked", false);
    $(form).find("#id_render_xls_report").prop("checked", false);
}

function filter_print(element){
    var form = $(element).parents("form");
    $(form).prop("target", "_blank");
    $(form).find("#id_render_pdf_report").prop("checked", true);
    $(form).find("#id_render_xls_report").prop("checked", false);
}

function filter_sheet(element){
    var form = $(element).parents("form");
    $(form).prop("target", "");
    $(form).find("#id_render_pdf_report").prop("checked", false);
    $(form).find("#id_render_xls_report").prop("checked", true);
}

function renumber_lines(table){
    $(table).find("tbody tr:not('.deleted_row')").each(function(idx, element){
        var td = $(element).find("td.line_number");
        $(td).html((idx + 1).toString());
    });
}

function find_empty_or_create(container, verifier, prefix){
    var rows = $(container).find("tbody tr:not('.deleted_row')");
    var row = null;
    $(rows).each(function(idx, element){
        if(verifier(element)){
            row = element;
        }
    });
    if(row==null) {
        row = addForm(container, prefix);
    }
    return row;
}