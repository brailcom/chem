function brailchem_display_error (message)
{
    var after_function = function () {
        this.find_element ('error-description').setAttribute ('value', message);
    }
    brailchem_switch_page ('chrome://brailchem/content/error.xul', 'error-description', after_function);
}
