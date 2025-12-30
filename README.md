

** How It Works **
Transactions are generated centrally
paymentId
traceId
Each transaction fans out to all components
Each component:
Picks a log line from its CSV
Generates a new spanId
Writes to its own log file
Logs rotate automatically at 1 MB
The cycle repeats infinitely
