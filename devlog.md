2025-10-11 6pm:

The project will include three Python programs: a logger for writing timestamped messages, an encryption service that performs Vigenère cipher operations, and a driver that connects them using pipes and handles user interaction.

I understand that each process will communicate through standard input/output streams using the subprocess module. My main goal is to get each component working independently, then integrate them to ensure smooth communication and logging. Next step: test the encryption logic before wiring everything together.

2025-10-19 – 3:30 PM

a. Thoughts so far:
I completed the logger_service.py file today. It successfully takes log messages from standard input, timestamps them, and writes to the specified log file. Seeing it work made the system structure feel more tangible, and I now have a better idea of how the driver will communicate with the logger process.

b. Plan for this session:
My goal is to test the logger thoroughly and make sure it handles all expected inputs, including edge cases like empty lines and the QUIT command. Once verified, I plan to start working on the encryption_service.py file next, specifically implementing the Vigenère cipher logic and handling commands like PASS, ENCRYPT, and DECRYPT.
