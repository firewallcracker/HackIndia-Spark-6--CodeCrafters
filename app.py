# app.py
from flask import Flask, render_template, request, jsonify
from traffic_monitor import monitor_blockchain_traffic
from node_security_checker import advanced_check_node_security
from contract_auditor import ContractAuditor
from vulnerability_scanner import scan_vulnerabilities

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/traffic', methods=['GET'])
def traffic_monitor():
    # Call the function from Member 1
    traffic_data = monitor_blockchain_traffic()
    return jsonify(traffic_data)

@app.route('/node-security', methods=['POST'])
def node_security():
    node_url = request.form['node_url']
    security_status = advanced_check_node_security(node_url)
    return jsonify(security_status)

@app.route('/contract-audit', methods=['POST'])
def contract_audit():
    contract_path = request.form['contract_path']
    audit_results = run_mythril_analysis(contract_path)
    return jsonify(audit_results)

@app.route('/vulnerability-scan', methods=['POST'])
def vulnerability_scan():
    endpoint = request.form['endpoint']
    scan_results = scan_vulnerabilities(endpoint)
    return jsonify(scan_results)

if __name__ == '__main__':
    app.run(debug=True)
