import pandas as pd
import threading
import os
import time
from logger import service_worker
from transactionQueue import generate_transactions
from appLogger import normal_app_logger
normLogger = normal_app_logger()


normLogger.info("Started")

NoOfTransactions = os.environ.get("NO_OF_TRANSACTIONS_PER_CYCLE")
NoOfTransactions = "10000" if NoOfTransactions==None else NoOfTransactions
normLogger.info("Number of transactions per cycle : {}".format(NoOfTransactions))


ThreadsPerLog = os.environ.get("NO_OF_THREADS_PER_CYCLE")
ThreadsPerLog = "5" if ThreadsPerLog==None else ThreadsPerLog


CSV_FILES = {
    "api_gateway": "./files/api_gateway_logs_10000.csv",
    "authentication_service": "./files/authentication_service_logs_10000.csv",
    "payment_processor": "./files/payment_processor_logs_10000.csv",
    "fraud_detection": "./files/fraud_detection_logs_10000.csv",
    "risk_engine": "./files/risk_engine_logs_10000.csv",
    "settlement_service": "./files/settlement_service_logs_10000.csv",
    "notification_service": "./files/notification_service_logs_10000.csv",
    "ledger_service": "./files/ledger_service_logs_10000.csv",
    "reporting_service": "./files/reporting_service_logs_10000.csv",
}

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

components = [
    "api_gateway",
    "payment_processor",
    "risk_engine",
    "settlement",
    "fraud_detection",
    "ledger_service",
    "authentication_service",
    "reporting_service",
    "notification_service"
]


cycle = 1

try:
    while True:
        normLogger.info(f"Starting cycle {cycle}")
        transactions = generate_transactions(int(100 if NoOfTransactions==None else NoOfTransactions))
        threads = []
        for comp in components:
            for i in range(0,int(ThreadsPerLog)):
                t = threading.Thread(
                    target=service_worker,
                    name=f"{comp}-thread-{cycle}-{i}",
                    args=(comp, transactions, cycle)
                )
                t.start()
                threads.append(t)
        
        for t in threads:
            t.join()
        cycle += 1
        time.sleep(1)

except KeyboardInterrupt:
    normLogger.info("Shutting down log generator gracefully...")

    
normLogger.info("Completed logs generation cycle {}".format(str(cycle)))
cycle = cycle+1




