/*
 * This script updates the select fields from the "Add Transaction" form
 */

function updateAccounts(id, data) {
  let account_select = document.getElementById(id);
  optionHTML = '';
  regex = /(Expenses - )|(Income - )/g;
  for (let account of data) {
    optionHTML += '<option value="' + account.id + '">' + account.name.replace(regex, '') + '</option>';
  }
  account_select.innerHTML = optionHTML;
}

$(function() {
  $( "#transactionKind" ).change(function() {
    kind = $(this).find("input[name='transaction_kind']:checked").val();

    fetch('/accounts/' + kind).then(function(response) {
      response.json().then(function(data) {
        console.table(data)
        updateAccounts('source_id', data.sources)
        updateAccounts('destination_id', data.destinations)
      })
    })
  })
});