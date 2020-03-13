function cloneMore(selector, type) {
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

function deleteForm(prefix, btn) {
  var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
  console.log('var total = ' + total)
  if (total > 1) {
    console.log(btn)
    console.log(btn.prev())
    btn.first('.instruction-form').remove();
    var forms = $('.instruction-form');
    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
    console.log('formCount = ' + forms.length)
    for (var i = 0, formCount = forms.length; i < formCount; i++) {
      $(forms.get(i)).find(':input').each(function() {
        console.log($(forms.get(i)).find(':input'))
        console.log('this = ' + this)
        console.log('prefix = ' + prefix)
        console.log('index = ' + i)
        updateElementIndex(this, prefix, i);
      });
    }
  }
  return false;
}

function updateElementIndex(el, prefix, ndx) {
  var id_regex = new RegExp('(' + prefix + '-\\d+)');
  var replacement = prefix + '-' + ndx;
  console.log('id_regex = ' + id_regex)
  console.log('replacement = ' + replacement)
  if ($(el).attr("for")) {
    $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
  }

  if (el.id) {
    el.id = el.id.replace(id_regex, replacement);
  }

  if (el.name) {
    el.name = el.name.replace(id_regex, replacement);
  }
}