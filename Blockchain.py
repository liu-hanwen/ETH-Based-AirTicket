from web3 import Web3, TestRPCProvider, HTTPProvider
from web3.contract import ConciseContract
import subprocess
import json
import Website
from jinja2 import Template

ETH_SERVER = 'http://localhost:8545'
SOL_TEMPLATE_PATH = './contract_template.sol'

w3 = Web3(HTTPProvider(ETH_SERVER))

MAIN_ACCOUNT = w3.eth.accounts[0]

def compile_source(src):
    print('Start to compile source...')
    filename = str(abs(hash(src)))+'.sol'
    files_before = subprocess.check_output('ls').decode('utf8').split('\n')
    with open(filename, 'w') as f:
        f.write(src)
    subprocess.check_call("solcjs --abi --bin %s \n exit 0" % filename, shell=True)
    ret = {}

    files_after = subprocess.check_output('ls').decode('utf8').split('\n')
    files_same = set(files_before) & set(files_after)

    targets = [file for file in files_after if file not in files_same]
    for target in targets:
        if '.abi' == target[-4:]:
            with open(target, 'r') as f:
                ret['abi'] = json.load(f)
        elif '.bin' == target[-4:]:
            with open(target, 'r') as f:
                ret['bin'] = f.read()
        else:
            continue

        subprocess.check_call('rm %s' % target, shell=True)

    subprocess.check_call('rm %s' % filename, shell=True)
    print('Compiled!\nThe return is:\n' , ret)
    return ret


def newFlight_submit(conn, args):

    no, comp, time, price, volume, addr, abi, from_, to = None

    '''Check args'''
    try:
        no = args['no']
        comp = args['comp']
        time = args['time']
        price = int(args['price'])
        volume = int(args['volume'])
        from_ = args['from']
        to = args['to']

    except KeyError as e:
        return str(e)


    '''New Contract Deployment'''
    src = None
    with open(SOL_TEMPLATE_PATH, 'r') as f:
        src = Template(f.read()).render(
            no = no,
            comp = comp,
            price = price,
            volume = volume,
            time = time,
            from_ = from_,
            to = to
        )

    contract_interface = compile_source(src)
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = contract.deploy(transaction={'from': MAIN_ACCOUNT})
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    addr = tx_receipt['contractAddress']
    abi = str(contract_interface['abi'])


    '''Update to database'''
    cmd = '''INSERT INTO flights VALUES (%s, %s, %s, %s, %s, %f, %d, %s, %s)''' % (no, comp, time, from_, to, price, volume, addr, abi)
    conn.execute(cmd)


    ret = None
    with open(Website.TEMPLATES_PATH + 'succeedPage.html', 'r') as f:
        ret = Template(f.read()).render(detail = cmd)
    return ret
