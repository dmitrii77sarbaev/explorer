from annoying.decorators import render_to

from blockcypher import get_transactions_details


@render_to('transaction_overview.html')
def transaction_overview(request, coin_symbol, tx_hash):

    transaction_details = get_transactions_details(tx_hash=tx_hash, coin_symbol=coin_symbol)

    # FIXME: fails silently on pagination if there are > 20 inputs or outputs

    # import pprint; pprint.pprint(transaction_details, width=1)

    confidence = transaction_details.get('confidence')
    if confidence:
        confidence_pct = confidence * 100
    else:
        confidence_pct = None

    received_at = transaction_details['received']
    confirmed_at = transaction_details.get('confirmed')

    if received_at >= confirmed_at:
        diff = received_at - confirmed_at
    else:
        diff = confirmed_at - received_at

    if diff.seconds < 60*20:
        time_to_use = received_at
    else:
        time_to_use = confirmed_at

    return {
            'coin_symbol': coin_symbol,
            'tx_hash': tx_hash,
            'double_spend_detected': transaction_details['double_spend'],
            'received_at': received_at,
            'confirmed_at': confirmed_at,
            'time_to_use': time_to_use,
            'total_satoshis': transaction_details['total'],
            'sent_satoshis': 0,
            'recieved_satoshis': 0,
            'fee_in_satoshis': transaction_details['fees'],
            'block_height': transaction_details['block_height'],
            'block_hash': transaction_details.get('block_hash'),
            'inputs': transaction_details['inputs'],
            'outputs': transaction_details['outputs'],
            'num_confirmations': transaction_details['confirmations'],
            'relayed_by': transaction_details['relayed_by'],
            'num_inputs': transaction_details['vin_sz'],
            'num_outputs': transaction_details['vout_sz'],
            'confidence_pct': confidence_pct,
            'preference': transaction_details.get('preference'),
            'receive_cnt': transaction_details.get('receive_count'),
            }
