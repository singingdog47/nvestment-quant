from datetime import datetime
from pathlib import Path

import pytest

from src.private_data_coherence import classify_private_inputs
from src.run_portfolio_risk import _build_latest_account_inputs
from src.private_account_import import parse_orders_file
from src.private_runtime_readiness import prepare_ledger


def pdf(path, text):
    import fitz
    doc=fitz.open(); page=doc.new_page()
    page.insert_text((35,40),text,fontname='japan',fontsize=10)
    doc.save(path);doc.close()


def test_pdf_document_provenance_reaches_normal_runner_without_zero_orders(tmp_path):
    path=tmp_path/'orders.pdf'
    pdf(path,'注文一覧\n約定\n2099/01/02 12:00\n1 / 2 ページ')
    snapshot=_build_latest_account_inputs(tmp_path,[(path,{'name':'orders.pdf','modifiedTime':'2099-01-03T12:00:00Z'})])
    orders=snapshot['inputs']['orders']
    assert orders['source_as_of']=='2099-01-02T12:00:00+09:00'
    assert orders['source_as_of_method']=='pdf_footer_explicit_year'
    assert orders['items'] is None and orders['orders_count'] is None
    assert orders['pdf_pages']==1 and orders['printed_page_count']==2
    assert snapshot['status']=='partial'
    assert snapshot['partial_input_types']==['orders']


def test_transaction_timestamp_cannot_date_order_pdf(tmp_path):
    path=tmp_path/'orders.pdf'
    pdf(path,'注文一覧\n2099/01/02 12:00\n約定\nページ末尾')
    with pytest.raises(ValueError,match='footer'):
        parse_orders_file(path)


def test_dated_but_partial_order_source_is_not_verified():
    stamp='2099-01-02T12:00:00+09:00'
    source={'status':'ok','source_as_of':stamp,'source_as_of_method':'pdf_footer_explicit_year'}
    inputs={k:dict(source) for k in ('account_summary','buying_power','orders')}
    inputs['orders'].update(status='partial',order_rows_verified=False)
    result=classify_private_inputs(source,{'inputs':inputs},now=datetime.fromisoformat(stamp))
    assert not result['decision_safe']
    assert 'ORDER_ROWS_UNVERIFIED' in result['inputs']['orders']['reasons']


def test_missing_documents_do_not_produce_a_verified_ledger(tmp_path):
    result=prepare_ledger([],{}, {},tmp_path)
    assert result['status']=='SOURCE_SET_INCOMPLETE'
    assert not Path(result['ledger_path']).exists()
