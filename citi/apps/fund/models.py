# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from libs.utils.sn import make_sn


class OrderManager(models.Manager):
    def get_user_order(self, user):
        return super(OrderManager, self).get_queryset().filter(user_id=user.pk)

    def add_order(self, user, order_type, order_content, pay_status, pay_way, sender_type, money, sender=None):
        """
        添加订单
        """
        if sender_type != Order.SENDER_TYPE_USER:
            sender_id = None
            sender_email = None
        else:
            sender_id = sender.pk
            sender_email = sender.email

        return super(OrderManager, self).create(
            sn=make_sn(),
            user_id=user.pk,
            user_email=user.email,
            order_type=order_type,
            order_status=0,
            order_content=order_content,
            pay_status=pay_status,
            pay_way=pay_way,
            sender_type=sender_type,
            sender_id=sender_id,
            sender_email=sender_email,
            money=money,
        )


class Order(models.Model):
    """
    订单信息表

    """
    # 订单类型
    ORDER_TYPE_RECHARGE = 0
    ORDER_TYPE_DRAW = 1
    ORDER_TYPE_SUPPORT = 2
    ORDER_TYPE_SUPPORT_BACK = 3
    ORDER_TYPE_SUPPORT_TRANSFER = 4
    ORDER_TYPE = (
        (ORDER_TYPE_RECHARGE, u'充值'),
        (ORDER_TYPE_DRAW, u'提现'),
        (ORDER_TYPE_SUPPORT, u'项目支持'),
        (ORDER_TYPE_SUPPORT_BACK, u'项目支持失败，资金退回'),
        (ORDER_TYPE_SUPPORT_TRANSFER, u'项目支持成功，资金转入发起人账户'),
    )

    # 订单状态
    ORDER_STATUS_CONFIRMED = 0
    ORDER_STATUS_CANCELED = 1
    ORDER_STATUS_INVALID = 2
    ORDER_STATUS = (
        (ORDER_STATUS_CONFIRMED, u'已确认'),
        (ORDER_STATUS_CANCELED, u'已取消'),
        (ORDER_STATUS_INVALID, u'无效订单'),
    )

    # 支付状态
    PAY_STATUS_NO = 0
    PAY_STATUS_YES = 1
    PAY_STATUS = (
        (PAY_STATUS_NO, u'未付款'),
        (PAY_STATUS_YES, u'已付款'),
    )

    # 支付方式
    PAY_WAY_ALIPAY = 0
    PAY_WAY = (
        (PAY_WAY_ALIPAY, u'支付宝'),
    )

    # 发送方类型
    SENDER_TYPE_ALIPAY = 0
    SENDER_TYPE_SYSTEM = 1
    SENDER_TYPE_USER = 2
    SENDER_TYPE = (
        (SENDER_TYPE_ALIPAY, u'支付宝'),
        (SENDER_TYPE_SYSTEM, u'系统'),
        (SENDER_TYPE_USER, u'用户'),
    )

    sn = models.CharField(u'订单编号', max_length=40, unique=True)
    user_id = models.IntegerField(u'用户ID')
    user_email = models.EmailField(u'用户电子邮件', max_length=255)
    order_type = models.IntegerField(u'订单类型', choices=ORDER_TYPE)
    order_status = models.IntegerField(u'订单状态', choices=ORDER_STATUS)
    order_content = models.TextField(u'订单内容', null=True, blank=True)
    pay_status = models.IntegerField(u'支付状态', choices=PAY_STATUS)
    pay_way = models.IntegerField(u'支付方式', choices=PAY_WAY)
    sender_type = models.IntegerField(u'发送方类型', choices=SENDER_TYPE)
    sender_id = models.IntegerField(u'发送方用户ID', blank=True, null=True)
    sender_email = models.EmailField(u'发送方电子邮件', max_length=255, blank=True, null=True)
    money = models.FloatField(u'总金额')
    add_datetime = models.DateTimeField(u'订单生成时间', auto_now_add=True)
    pay_datetime = models.DateTimeField(u'订单支付时间', blank=True, null=True)

    def confirm_payment(self):
        if self.pay_status == self.PAY_STATUS_NO:
            self.pay_status = self.PAY_STATUS_YES
            self.pay_datetime = timezone.now()
            self.save()

            Trade.manager.add_trade(
                order=self,
                user=get_user_model().objects.get(pk=self.user_id),
                money=self.money
            )
            if self.sender_type == self.SENDER_TYPE_USER:
                Trade.manager.add_trade(
                    order=self,
                    user=get_user_model().objects.get(pk=self.sender_id),
                    money=-self.money
                )

    class Meta:
        verbose_name = u'订单信息表'
        verbose_name_plural = u'订单信息表'
        permissions = (
            ('view_order', u'Can view 订单信息'),
        )

    objects = models.Manager()
    manager = OrderManager()


class TradeManager(models.Manager):
    def get_user_trade(self, user):
        return super(TradeManager, self).get_queryset().filter(user_id=user.pk)

    def add_trade(self, order, user, money):
        balance = user.balanceinfo.balance + money

        trade = super(TradeManager, self).create(
            order_id=order.pk,
            sn=order.sn,
            user_id=user.pk,
            user_email=user.email,
            money=money,
            balance=balance
        )

        user.balanceinfo.balance = balance
        user.balanceinfo.save()

        return trade


class Trade(models.Model):
    """
    交易记录表

    """
    order_id = models.IntegerField(u'所属订单ID')
    sn = models.CharField(u'订单编号', max_length=40, unique=True)
    user_id = models.IntegerField(u'用户ID')
    user_email = models.EmailField(u'用户电子邮件', max_length=255)
    money = models.FloatField(u'交易金额')
    balance = models.FloatField(u'交易后余额')
    datetime = models.DateTimeField(u'交易日期', auto_now_add=True)

    class Meta:
        verbose_name = u'交易记录表'
        verbose_name_plural = u'交易记录表'
        permissions = (
            ('view_trade', u'Can view 交易记录'),
        )

    objects = models.Manager()
    manager = TradeManager()