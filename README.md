

**How It Works:**

1. Transactions are generated centrally
	paymentId
	traceId
2. Each transaction fans out to all components
3. Each component:
4. Picks a log line from its CSV
5. Generates a new spanId
6. Writes to its own log file
7. Logs rotate automatically at 1 MB
8. The cycle repeats infinitely
