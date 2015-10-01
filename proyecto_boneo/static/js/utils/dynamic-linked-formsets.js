var AltaInlineController = function(
    url_form_rendering,
    form_prefix,
    formset_container_id,
    modal_id,
    inline_form_container_id,
    modal_confirm_button_id,
    find_empty_or_create_callback){
        this.url_form_rendering = url_form_rendering;
        this.prefix = form_prefix;
        this.formset_container_id = formset_container_id;
        this.modal_id = modal_id;
        this.modal_form_container_id = inline_form_container_id;
        this.modal_confirm_button_id = modal_confirm_button_id;
        this.find_empty_or_create_callback = find_empty_or_create_callback;
};


AltaInlineController.prototype.formToFormset =
function(form_container, formset_row){
    $(form_container).find('[name]').each(function(idx, element){
       $(formset_row).find("[name$='" + $(element).prop("name") + "']").val($(element).val());
    });
};


AltaInlineController.prototype.formsetToForm =
function(formset_row, form_container){
    $(form_container).find('[name]').each(function(idx, element){
       $(element).val($(formset_row).find("[name$='" + $(element).prop("name") + "']").val());
    });
};


AltaInlineController.prototype.eliminarForm = function(line_number){
    var self = this;
    var formset_container = $("#" + self.formset_container_id);
    var input = $(formset_container).find("[id$=linked_line_number]").filter(function(){return $(this).val() == line_number});
    deleteForm(input, self.prefix);
};


AltaInlineController.prototype.confirmarNuevoForm =
function(line_number, success_callback){
    var self = this;
    var chequeform = $("#" + self.modal_form_container_id);
    var row = find_empty_or_create($("#" + self.formset_container_id),
        self.find_empty_or_create_callback, self.prefix);
    self.formToFormset(chequeform, row);
    $(row).find("[name$=linked_line_number]").val(line_number);
    $("#" + self.modal_id).modal('hide');
    $(chequeform).html("");
    success_callback(row);
};


AltaInlineController.prototype.confirmarForm =
function(row, success_callback){
    var self = this;
    var chequeform = $("#" + self.modal_form_container_id);
    self.formToFormset(chequeform, row);
    $("#" + self.modal_id).modal('hide');
    $(chequeform).html("");
    success_callback(row);
};


AltaInlineController.prototype.nuevoForm =
function(line_number, success_callback){
    var self = this;
    var chequeform = $("#" + self.modal_form_container_id);
    $(chequeform).html("");
    $.get(self.url_form_rendering, function(data){
        var confirmButton = $("#" + self.modal_confirm_button_id);
        $(confirmButton).off("click");
        $(confirmButton).click(function(){
            self.validarFormulario(function(){self.confirmarNuevoForm(line_number, success_callback)});
        });
        $("#" + self.modal_id).modal('show');
        $(chequeform).html(data);
        getMainController().configure_controls();
    });
};


AltaInlineController.prototype.validarFormulario =
function(callback){
    var self = this;
    var chequeform = $("#" + self.modal_form_container_id);
    var get_data = $("#" + self.modal_form_container_id + " *").serialize();
    $.get(self.url_form_rendering, get_data,
    function (data){
        if(data == 'valid'){
            callback();
        }else{
            $(chequeform).html(data);
            getMainController().configure_controls();
        }
    })
};


AltaInlineController.prototype.editarForm =
function(line_number, success_callback){
    var self = this;
    var chequeform = $("#" + self.modal_form_container_id);
    $(chequeform).html("");
    $.get(self.url_form_rendering, function(data){
        var row = null;
        $("#" + self.formset_container_id).find("[name$='linked_line_number']").each(function(idx, element){
            if($(element).val() == line_number){
                row = $(element).parents("tr");
            }
        });
        var confirmButton = $("#" + self.modal_confirm_button_id);
        $(confirmButton).off("click");
        $(confirmButton).click(function(){
            self.validarFormulario(function(){self.confirmarForm(row, success_callback)});
        });
        $("#" + self.modal_id).modal('show');
        $(chequeform).html(data);
        self.formsetToForm(row, chequeform);
        getMainController().configure_controls();
    });
};


