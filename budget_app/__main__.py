from model   import Transaction
from service import TransactionService

transaction = Transaction(id=1, type='expense', date='2026-09-17', amount=5000, category='식비', memo='점심')
service = TransactionService()
service.add(transaction)