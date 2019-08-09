from datetime import datetime
import pytest

from finerplan.model import Transaction

from data.tests.transactions import computer


@pytest.mark.usefixtures('test_transactions')
def test_transaction_balance_method_unbounded(test_accounts):
    """Tests generic method to calculate transactions's balance over a period of time."""
    account = test_accounts[2]

    assert Transaction.balance(account) == 1135


@pytest.mark.usefixtures('test_transactions')
def test_transaction_balance_method_bounded(test_accounts):
    """Tests generic method to calculate transactions's balance over a period of time."""
    account = test_accounts[2]

    dt = datetime(2019, 7, 15)

    assert Transaction.balance(account, end=dt) == 1185
    assert Transaction.balance(account, start=dt) == -50
    assert Transaction.balance(account, start=datetime(2019, 7, 3), end=dt) == -15


def test_transaction_create(test_accounts):
    """
    Tests that method 'create' can handle the data from AddTransactionForm
    and create both Transaction and Installment instances.
    """
    source = test_accounts[5]
    destination = test_accounts[6]
    transaction_data = computer()
    value = transaction_data.pop('value')
    installments = transaction_data.pop('installments')

    transaction = Transaction.create(
        value=value, installments=installments, source_id=source.id,
        destination_id=destination.id, **transaction_data)

    assert Transaction.query.count() == 1
    assert transaction.installments.count() == installments
