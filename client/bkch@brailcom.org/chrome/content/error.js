function bkch_display_error (message)
{
    var after_function = function () {
        this.find_element ('error-description').setAttribute ('value', message);
    }
    bkch_switch_page ('chrome://bkch/content/error.xul', 'error-description', after_function);
}
