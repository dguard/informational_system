window.Eumkd = {
    Search: {
        initializeSelect2Autocomplete: function($element, autocompleteUrl, params) {
            !params && (params = {});

            params = $.extend({
                placeholder: "Не выбрано",
                minimumInputLength: 3,
                ajax: {
                    url: autocompleteUrl,
                    dataType: 'json',
                    data: function (term) { return { term: term } },
                    results: function (data) { return { results: data } }
                },
                initSelection: function(element, callback) {
                    var id   = $(element).data('value'),
                        name = $(element).val();

                    if(name == "") {
                        id = '';
                        name = 'Не выбрано';
                    }
                    callback({ 'id': id, 'name': name })
                },
                formatResult: function(item) {
                    return item.name;
                },
                formatSelection: function(data) {
                    return data.name;
                }
            }, params);

            $element.select2(params);
        },
        initializeSelect2Dropdown: function($element, params) {
            !params && (params = {});

            var format = function(field) {
                if (field.id === 'false') {
                    return "<b>" + field.text + "</b>";
                }
                return field.text;
            };

            params = $.extend({
                formatResult: format,
                formatSelection: format,
                escapeMarkup: function(m) { return m; }
            }, params);

            $element.select2(params);
        }
    }
};