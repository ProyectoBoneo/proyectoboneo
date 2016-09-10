(function() {
  window.FilterController = (function() {
    function FilterController() {
      $("#id_render_pdf_report").hide();
      $("#id_render_xls_report").hide();
    }

    FilterController.prototype.filter_click = function(element) {
      var form;
      form = $(element).parents("form");
      $(form).prop("target", "");
      $(form).find("#id_render_pdf_report").prop("checked", false);
      return $(form).find("#id_render_xls_report").prop("checked", false);
    };

    FilterController.prototype.filter_print = function(element) {
      var form;
      form = $(element).parents("form");
      $(form).prop("target", "_blank");
      $(form).find("#id_render_pdf_report").prop("checked", true);
      return $(form).find("#id_render_xls_report").prop("checked", false);
    };

    FilterController.prototype.filter_sheet = function(element) {
      var form;
      form = $(element).parents("form");
      $(form).prop("target", "");
      $(form).find("#id_render_pdf_report").prop("checked", false);
      return $(form).find("#id_render_xls_report").prop("checked", true);
    };

    return FilterController;

  })();

  window.filterController = new FilterController();

}).call(this);