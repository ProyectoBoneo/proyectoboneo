function registerTypeaheads(row){
    $(row).find("span.twitter-typeahead").remove();
    $(row).find(".typeahead-form-input").each(function(idx, element){
        element.setAttribute("data-lookup-activated", "false");
    });
    var typeaheadController = new TypeaheadController();
    typeaheadController.register_typeaheads();
}

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function addForm(container, prefix) {
    var formCount = $(container).find('.dynamic-form').length;
    var row = $(container).find(".dynamic-form:not('.deleted_row'):first").clone(true).get(0);
    $(row).removeAttr('id').insertAfter($(container).find('.dynamic-form:last'));
    $(row).find("[name]").each(function() {
        updateElementIndex(this, prefix, formCount);
        $(this).val('');
    });
    $(row).attr('id', prefix + '-' + formCount + '-row');
    $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
    registerTypeaheads(row);
    return row;
}


function deleteForm(row_element, prefix) {
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
        var substract = false;
        if ($(rows).length == 1) {
            new_row = addForm(container, prefix);
            substract = true;
        }
        $(row).prop("hidden", true);
        $(row).addClass("deleted_row");
        var delete_input = $(row).find("input[id*='DELETE']");
        $(delete_input).prop("checked", true);
        $(delete_input).val("on");
        if (substract) {
            var formCount = $(container).find('.dynamic-form').length;
            $('#id_' + prefix + '-TOTAL_FORMS').val(formCount - 1);
        }
    }
    return new_row;
}