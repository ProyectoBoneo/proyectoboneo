var InscripcionesController = function(){
    var self = this;
    self.formset_prefix = 'form';
    $('.add-row').click(function() {
        var row = addForm(this.parentNode, self.formset_prefix);
        self.reset_row_status(row);
    });

    $('.delete-row').click(function() {
        var replacement_row = deleteForm(this, self.formset_prefix);
        if(replacement_row != null){
            self.reset_row_status(replacement_row);
        }
    })
};

InscripcionesController.prototype.reset_row_status = function(row){
    renumber_lines($("#id_forms_table"));
};
