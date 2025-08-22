from django.db import models
from django.db.models import Count, Sum, Q, ExpressionWrapper, IntegerField, F
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from django.db import transaction


class Transaction(models.Model):

    CHARGE = 1
    PURCHASE = 2
    TRANSFER_RECEIVED = 3
    TRANSFER_SEND = 4

    TRANSACTION_TYPE_CHOICE = (
        (CHARGE, "Charge"),
        (PURCHASE, "Purchase"),
        (TRANSFER_RECEIVED, "Transfer-recive"),
        (TRANSFER_SEND, "Transfer-send"),
    )

    user = models.ForeignKey(
        User, related_name="transactions", on_delete=models.RESTRICT
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICE, default=CHARGE
    )
    amount = models.BigIntegerField()
    created_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.get_transaction_type_display()} - {self.amount}"

    @classmethod
    def get_report(cls):
        """Show all users and their balances"""
        positive_transactions = Sum(
            "transactions__amount", filter=Q(transactions__transaction_type__in=[cls.CHARGE, cls.TRANSFER_RECEIVED]),
        )

        negative_transactions = Sum(
            "transactions__amount",
            filter=Q(transactions__transaction_type__in=[cls.PURCHASE, cls.TRANSFER_SEND]),
        )

        return User.objects.annotate(
            tr_count=Count("transactions__id"),
            balance=ExpressionWrapper(
                Coalesce(positive_transactions, 0) - Coalesce(negative_transactions, 0),
                output_field=IntegerField(),
            ),
        )

    @classmethod
    def get_total_balance(cls):
        queryset = cls.get_report()
        return queryset.aggregate(Sum("balance"))

    @classmethod
    def user_balance(cls, user):
        posetive_transactions = Sum("amount", filter=Q(transaction_type__in=[1, 3]))
        negative_transactions = Sum("amount", filter=Q(transaction_type__in=[2, 4]))

        user_balance = user.transactions.all().aggregate(
            balance=Coalesce(posetive_transactions, 0)
            - Coalesce(negative_transactions, 0)
        )
        return user_balance.get("balance", 0)


class UserBalance(models.Model):
    user = models.ForeignKey(
        User, related_name="balance_recoard", on_delete=models.RESTRICT
    )
    balance = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.balance} - {self.created_time}"

    @classmethod
    def recored_user_balance(cls, user):
        balance = Transaction.user_balance(user)

        instance = cls.objects.create(user=user, balance=balance)
        return instance

    @classmethod
    def all_users_recored_balance(cls, user):
        for user in User.objects.all():
            cls.recored_user_balance(user)


class TransferTransaction(models.Model):
    sender_transaction = models.ForeignKey(
        Transaction, related_name="sender_transfer", on_delete=models.RESTRICT
    )
    receiver_transaction = models.ForeignKey(
        Transaction, related_name="receiver_transfer", on_delete=models.RESTRICT
    )

    def __str__(self):
        return f"{self.sender_transaction} >> {self.receiver_transaction}"

    @classmethod
    def transfer(cls, sender, receiver, amount):
        with transaction.atomic():
            sender = User.objects.select_for_update().get(id=sender.id)
            if Transaction.user_balance(sender) < amount:
                return "Transactio not allowed, insufficiet balance"

            sender_transaction = Transaction.objects.create(
                user=sender,
                amount=amount,
                transaction_type=Transaction.TRANSFER_SEND,
            )

            receiver_transaction = Transaction.objects.create(
                user=receiver,
                amount=amount,
                transaction_type=Transaction.TRANSFER_RECEIVED,
            )

            instanse = cls.objects.create(
                sender_transaction=sender_transaction,
                receiver_transaction=receiver_transaction,
        )

        return instanse


class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    @classmethod
    def change_score(cls, user, score):
        with transaction.atomic():
            instance = cls.objects.select_for_update().filter(user=user)
            if not instance.exsists():
                instance = cls.objects.create(user=user, score=0)
            else:
                instance = instance.first()

            instance.score += score
            instance.save()
