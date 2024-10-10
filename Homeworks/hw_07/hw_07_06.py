"""
Завдання 6. Приклад комплексного тестування.

Розробіть програму для роботи з банківськими транзакціями та протестуйте її
за допомогою фікстур, моків, скіпів та параметризації.

Напишіть клас BankAccount, який реалізує методи:

-   deposit(amount: float): поповнення рахунку;
-   withdraw(amount: float): зняття коштів (якщо достатньо коштів на рахунку).
-   get_balance() -> float: повертає поточний баланс.

Напишіть тести з використанням:

-   фікстур для створення об'єкта банківського рахунку перед тестами,
-   моків для тестування взаємодії із зовнішнім API (наприклад, для перевірки балансу),
-   скіпів для пропуску тестів зняття коштів, якщо рахунок порожній.

Використовуйте параметризацію для тестування різних сценаріїв поповнення та зняття коштів.
"""
from unittest import mock
import pytest


class BankAccount:
    """
    Represent a bank account with deposit, withdrawal, and balance inquiry functions.

    :var balance: The current balance of the account.
    :type balance: float
    """

    def __init__(self):
        """
        Initialize a bank account with an initial balance of 0.00.
        """
        self.balance = 0.00

    def deposit(self, amount):
        """
        Deposit an amount into the account.

        :param amount: The amount to be deposited.
        :type amount: float
        """
        self.balance += amount

    def withdraw(self, amount):
        """
        Withdraw an amount from the account if sufficient funds are available.

        :param amount: The amount to be withdrawn.
        :type amount: float
        :raises ValueError: If the balance is insufficient for the withdrawal.
        """
        if self.balance < amount:
            raise ValueError("Not enough funds!")
        self.balance -= amount

    def get_balance(self):
        """
        Get the current balance of the account.

        :return: The current balance.
        :rtype: float
        """
        return self.balance


# ---- Fixtures for testing ----

@pytest.fixture
def bank_account():
    """
    Create a bank account fixture with an initial deposit of 250.

    :return: BankAccount instance with a balance of 250.
    :rtype: BankAccount
    """
    test_acc = BankAccount()
    test_acc.deposit(250)
    return test_acc


@pytest.fixture
def empty_bank_account():
    """
    Create an empty bank account fixture.

    :return: BankAccount instance with a balance of 0.
    :rtype: BankAccount
    """
    empty_acc = BankAccount()
    return empty_acc


# ---- Test functions ----

def test_get_balance(bank_account):
    """
    Test the get_balance method to check if it returns the correct balance.
    """
    assert bank_account.get_balance() == 250


@pytest.mark.parametrize('deposit_amount, current_balance', [
    (100, 350),
    (50, 300),
    (0, 250)
])
def test_deposit(bank_account, deposit_amount, current_balance):
    """
    Test the deposit method with various deposit amounts.

    :param bank_account: BankAccount fixture for testing.
    :type bank_account: BankAccount
    :param deposit_amount: The amount to be deposited.
    :type deposit_amount: float
    :param current_balance: The expected balance after the deposit.
    :type current_balance: float
    """
    bank_account.deposit(deposit_amount)
    assert bank_account.get_balance() == current_balance


@pytest.mark.parametrize('withdraw_amount, current_balance', [
    (50, 200),
    (100, 150),
    (200, 50)
])
def test_withdraw(bank_account, withdraw_amount, current_balance):
    """
    Test the withdraw method with various withdrawal amounts.

    :param bank_account: BankAccount fixture for testing.
    :type bank_account: BankAccount
    :param withdraw_amount: The amount to be withdrawn.
    :type withdraw_amount: float
    :param current_balance: The expected balance after the withdrawal.
    :type current_balance: float
    """
    bank_account.withdraw(withdraw_amount)
    assert bank_account.get_balance() == current_balance


@pytest.mark.skipif(BankAccount().get_balance() == 0, reason="Account is empty.")
def test_withdraw_when_empty(empty_bank_account):
    """
    Test the withdraw method on an empty account and expect a skip if balance is zero.
    """
    empty_bank_account.withdraw(50)
    assert empty_bank_account.get_balance() == 200


def test_withdraw_with_skip_logic(bank_account):
    """
    Test withdrawal with conditional skip logic if the account is empty.
    """
    if bank_account.get_balance() == 0:
        pytest.skip("Account is empty")
    bank_account.withdraw(50)
    assert bank_account.get_balance() == 200


def test_get_balance_with_api_mock(bank_account):
    """
    Test the get_balance method by mocking the BankAccount.get_balance API.

    :param bank_account: BankAccount fixture for testing.
    :type bank_account: BankAccount
    """
    with mock.patch('hw_07_06.BankAccount.get_balance', return_value=500) as mock_get_balance:
        balance = bank_account.get_balance()
        mock_get_balance.assert_called_once()
        assert balance == 500
