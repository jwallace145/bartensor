function addForm(selector, type) {
  var newElement = $(selector).clone(true);
  var total = $('#id_' + type + '-TOTAL_FORMS').val();
  newElement.find(':input').each(function() {
    var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
    var id = 'id_' + name;
    $(this).attr({
      'name': name,
      'id': id
    }).val('').removeAttr('checked');
  });
  newElement.find('label').each(function() {
    var newFor = $(this).attr('for').replace('-' + (total - 1) + '-', '-' + total + '-');
    $(this).attr('for', newFor);
  });
  total++;
  $('#id_' + type + '-TOTAL_FORMS').val(total);
  $(selector).after(newElement);
}

function deleteForm(prefix, button) {
  var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

  if (total > 1) {
    $('.' + prefix + '-form').first().remove()

    var forms = $('.' + prefix + '-form');
    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);

    for (var i = 0; i < forms.length; i++) {
      $(forms.get(i)).find(':input').each(function() {

        var id_regex = new RegExp('(' + prefix + '-\\d+)');
        var replacement = prefix + '-' + i;
        if ($(this).attr("for")) {
          $(this).attr("for", $(el).attr("for").replace(id_regex, replacement));
        }

        if (this.id) {
          this.id = this.id.replace(id_regex, replacement);
        }

        if (this.name) {
          this.name = this.name.replace(id_regex, replacement);
        }
      });
    }
  }
}