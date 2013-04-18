# -*- coding: utf-8 -*-

from email.errors import MessageError
from celery.task import task
from django.core.exceptions import ObjectDoesNotExist
from xlrd import open_workbook
from ffclub.settings import PRODUCT_INVENTORY_MAPPING, PRODUCT_INVENTORY_QTY_ROW_NAME, \
    PRODUCT_INVENTORY_PATH, PRODUCT_INVENTORY_SHEET_NAME
import logging
from ffclub.product.models import Product

log = logging.getLogger('ffclub')

@task()
def send_mail(mail):
    if mail is not None:
        try:
            mail.send()
        except MessageError as e:
            log.debug('Failed to send verification mail: ', e)
        except RuntimeError as e:
            log.debug('Unexpected error when sending verification mail: ', e)

@task()
def sync_inventory():
    book = open_workbook(PRODUCT_INVENTORY_PATH)
    sheet = book.sheet_by_name(PRODUCT_INVENTORY_SHEET_NAME)
    current_qty_row_index = 2
    for row_index in range(sheet.nrows):
        if sheet.cell(row_index, 1).value == PRODUCT_INVENTORY_QTY_ROW_NAME:
            current_qty_row_index = row_index
            print current_qty_row_index
    for col_index in range(sheet.ncols):
        col_name = sheet.cell(0, col_index).value
        if col_name in PRODUCT_INVENTORY_MAPPING.keys():
            product_id = PRODUCT_INVENTORY_MAPPING[col_name]
            quantity = sheet.cell(current_qty_row_index, col_index).value
            try:
                product = Product.objects.get(id=product_id)
                product.quantity = quantity
                product.save()
                log.debug(sheet.cell(0, col_index).value, '(', product_id, '): ', quantity)
            except ObjectDoesNotExist as e:
                log.error('Product with id %d does not exist.' % product_id, e)

