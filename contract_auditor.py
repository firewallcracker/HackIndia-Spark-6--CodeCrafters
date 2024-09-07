import subprocess
import logging
import os
import shlex

# Configure logging
logging.basicConfig(filename='contract_auditor.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ContractAuditor:
    def _init_(self, mythril_path='myth'):
        self.mythril_path = mythril_path
        self.default_timeout = 300  # 5 minutes

    def run_mythril_analysis(self, contract_path, options=None, timeout=None):
        """
        Runs Mythril analysis on the provided contract file.
        
        Parameters:
            contract_path (str): Path to the smart contract file.
            options (str): Optional Mythril command-line options (e.g., '--execution-timeout 60').
            timeout (int): Time limit for Mythril analysis execution in seconds.

        Returns:
            dict: Contains the status and either the analysis result or error information.
        """
        if not os.path.isfile(contract_path):
            logging.error(f"Contract file does not exist: {contract_path}")
            return {"status": "File not found", "error": f"File {contract_path} not found"}
        
        # Prepare command with optional parameters
        options = options if options else ''
        command = f"{self.mythril_path} analyze {contract_path} {options}"
        command = shlex.split(command)  # Safely parse the command
        
        logging.info(f"Running Mythril analysis on {contract_path} with options: {options}")
        timeout = timeout if timeout else self.default_timeout
        
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                    text=True, timeout=timeout)
            if result.returncode == 0:
                logging.info(f"Mythril analysis successful for {contract_path}")
                return {"status": "Analysis complete", "output": result.stdout}
            else:
                logging.error(f"Mythril analysis failed for {contract_path}: {result.stderr}")
                return {"status": "Analysis failed", "error": result.stderr}
        
        except subprocess.TimeoutExpired:
            logging.error(f"Mythril analysis timed out for {contract_path}")
            return {"status": "Error", "error": "Mythril analysis timed out"}
        
        except FileNotFoundError as e:
            logging.error(f"Mythril command not found: {e}")
            return {"status": "Error", "error": "Mythril tool not found"}
        
        except Exception as e:
            logging.exception(f"An error occurred while running Mythril analysis: {e}")
            return {"status": "Error", "error": str(e)}

# Example usage
if __name__ == "_main_":
    auditor = ContractAuditor()
    contract_path = "contracts/MySmartContract.sol"
    
    # Example with additional options
    options = "--execution-timeout 60 --solc-json solc.json"
    result = auditor.run_mythril_analysis(contract_path, options=options)
    print(result)
