import datetime
import hashlib
import json
from flask import Flask, jsonify, send_file
import shutil
import PyPDF2

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def print_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()

            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()
            ).hexdigest()

            if hash_operation[:5] != '00000':
                return False

            previous_block = block
            block_index += 1

        return True

    def store_file(self, file):
        if not os.path.exists('files'):
            os.makedirs('files')

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        filename = f'files/file_{timestamp}.pdf'

        shutil.copy(file, filename)
        self.write_to_pdf(filename)

        return filename

    def write_to_pdf(self, filename):
        existing_pdf = PyPDF2.PdfFileReader(open(filename, "rb"))
        output_pdf = PyPDF2.PdfFileWriter()
        page = output_pdf.addBlankPage(width=500, height=500)
        text = json.dumps(self.chain, indent=4)
        page.mergePage(existing_pdf.getPage(0))
        page.mergeTranslatedPage(existing_pdf.getPage(0), tx=0, ty=100)
        page.mergeTextData(text, tx=50, ty=200)

        new_filename = f"blockchain_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        with open(new_filename, "wb") as output_file:
            output_pdf.write(output_file)

        return new_filename
    
# Creating the Web
# App using flask
app = Flask(__name__)

# Create the object
# of the class blockchain
blockchain = Blockchain()

# Mining a new block


@app.route('/mine_block', methods=['GET'])
def mine_block():
	previous_block = blockchain.print_previous_block()
	previous_proof = previous_block['proof']
	proof = blockchain.proof_of_work(previous_proof)
	previous_hash = blockchain.hash(previous_block)
	block = blockchain.create_block(proof, previous_hash)

	response = {'message': 'A block is MINED',
				'index': block['index'],
				'timestamp': block['timestamp'],
				'proof': block['proof'],
				'previous_hash': block['previous_hash']}

	return jsonify(response), 200

# Display blockchain in json format


@app.route('/get_chain', methods=['GET'])
def display_chain():
	response = {'chain': blockchain.chain,
				'length': len(blockchain.chain)}
	return jsonify(response), 200

# Check validity of blockchain


@app.route('/valid', methods=['GET'])
def valid():
	valid = blockchain.chain_valid(blockchain.chain)

	if valid:
		response = {'message': 'The Blockchain is valid.'}
	else:
		response = {'message': 'The Blockchain is not valid.'}
	return jsonify(response), 200

@app.route('/write_pdf', methods=['GET'])
def write_pdf():
    filename = 'path/to/existing_pdf.pdf'  # Substitua pelo nome do seu arquivo PDF existente
    new_filename = blockchain.write_to_pdf(filename)

    response = {'message': 'PDF written successfully',
                'filename': new_filename}

    return jsonify(response), 200

@app.route('/download_pdf/<filename>', methods=['GET'])
def download_pdf(filename):
    return send_file(filename, as_attachment=True)

@app.route('/help', methods=['GET'])
def help():
    response = {
        'commands': {
            '/mine_block': 'Minera um novo bloco na blockchain.',
            '/get_chain': 'Exibe a cadeia de blocos em formato JSON.',
            '/valid': 'Verifica a validade da cadeia de blocos.',
            '/store_file': 'Armazena um arquivo PDF na blockchain.',
            '/write_pdf': 'Escreve os dados da cadeia de blocos em um arquivo PDF.',
            '/download_pdf/<filename>': 'Faz o download de um arquivo PDF.'
        }
    }
    return jsonify(response), 200

# Run the flask server locally
app.run(host='127.0.0.1', port=5000)
